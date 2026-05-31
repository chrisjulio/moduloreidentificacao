"""Experiment runner: anonymization + attacks + metrics pipeline.

Orchestrates the full evaluation pipeline for one experiment configuration:

    load graph  →  anonymize (He et al. 2009)  →  validate k-anonymity
                →  run attacks (degree / subgraph)
                →  compute metrics (reidentification_rate, equivalence_group_size,
                                    ks_test_degree, clustering_variation)
                →  write structured JSONL log

Usage
-----
    python -m experiments.run --config experiments/configs/<name>.yml

Output
------
    experiments/logs/<name>/<name>.jsonl  — one JSONL entry per (k, seed)
    experiments/logs/<name>/summary.json  — aggregate summary
    Exit code 0 = all runs passed; 1 = at least one failure or error.

YAML schema
-----------
Required sections: ``experiment``, ``seeds``, ``dataset``, ``anonymization``.
Optional sections: ``attacks``, ``runtime``.
``anonymization.k`` accepts either a single integer or a list of integers.

Log entry schema (issue #22 / DL-01)
--------------------------------------
Each JSONL entry contains:

    {
      "experiment": "<name>",
      "k": <int>,
      "d": <int>,
      "seed": <int>,
      "timestamp": "<ISO-8601>",
      "partition_backend": "pymetis" | "networkx-kl",  # engine actually used (D-04)
      "validate_k_anonymity": { <full DL-01 dict> },
      "reidentification_rate": <float>,          # degree attack (primary)
      "reidentification_rate_degree": <float>,   # always present when degree enabled
      "reidentification_rate_subgraph": <float>, # present when subgraph enabled
      "equivalence_group_size": {"mean": <float>, "median": <int>},
      "ks_test_degree": {"D": <float>, "p": <float>},
      "clustering_variation": <float | null>,
      "verdict": "SUCCESS_FULL" | "SUCCESS_PARTIAL" | "FAILURE_FATAL"
                 | "FAILURE_LOW_COVERAGE" | "ERROR",
      "error": null | {"type": ..., "message": ..., "traceback": ...}
    }
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path

import networkx as nx
import yaml

from src.anonymization.he2009 import (
    _group_isomorphic,
    _modify_structure,
    _partition_neighborhoods,
    _reconnect_inter_edges,
)
from src.anonymization.validation import validate_k_anonymity
from src.attacks import degree_attack, subgraph_attack
from src.loaders.facebook_ego import load_facebook_egonet
from src.metrics import (
    clustering_variation,
    equivalence_group_size,
    ks_test_degree,
    reidentification_rate,
)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("experiments.run")


# ---------------------------------------------------------------------------
# Pre-processing
# ---------------------------------------------------------------------------


def preprocess_graph(
    g: nx.Graph,
    component: str = "lcc",
    min_nodes: int = 0,
) -> nx.Graph:
    """Extract and sanitise the graph before anonymisation.

    Parameters
    ----------
    g:
        Raw graph as loaded from the dataset.
    component:
        ``"lcc"`` to retain only the Largest Connected Component (default).
        Any other value keeps the graph unchanged.
    min_nodes:
        Minimum number of nodes after pre-processing. Raises ``ValueError``
        when the graph is smaller than this threshold.

    Returns
    -------
    nx.Graph
        Pre-processed graph with nodes relabelled ``0..n-1``.
    """
    if component == "lcc":
        lcc_nodes = max(nx.connected_components(g), key=len)
        g = g.subgraph(lcc_nodes).copy()
        logger.info("LCC retained: n=%d, m=%d", g.number_of_nodes(), g.number_of_edges())

    if min_nodes and g.number_of_nodes() < min_nodes:
        raise ValueError(
            f"Graph has {g.number_of_nodes()} nodes after pre-processing, "
            f"below min_nodes={min_nodes}."
        )

    return nx.convert_node_labels_to_integers(g)


# ---------------------------------------------------------------------------
# Dataset loader
# ---------------------------------------------------------------------------


def load_dataset(dataset_cfg: dict) -> nx.Graph:
    """Load the graph specified in the dataset config block.

    Parameters
    ----------
    dataset_cfg:
        The ``dataset:`` section of the experiment YAML.

    Returns
    -------
    nx.Graph
        Pre-processed graph ready for anonymisation.

    Raises
    ------
    ValueError
        If ``dataset_cfg["name"]`` is not a supported dataset.
    FileNotFoundError
        If the dataset files are not found on disk.
    """
    name = dataset_cfg["name"]
    if name == "facebook_ego_nets":
        data_dir = Path(dataset_cfg["data_path"])
        egonet_id = int(dataset_cfg["egonet_id"])
        g_raw = load_facebook_egonet(egonet_id, data_dir)
        logger.info(
            "Raw graph loaded: egonet_id=%d, n=%d, m=%d",
            egonet_id,
            g_raw.number_of_nodes(),
            g_raw.number_of_edges(),
        )
    else:
        raise ValueError(f"Unknown dataset name: {name!r}. Supported datasets: facebook_ego_nets")

    component = dataset_cfg.get("component", "lcc")
    min_nodes = int(dataset_cfg.get("min_nodes", 0))
    return preprocess_graph(g_raw, component=component, min_nodes=min_nodes)


# ---------------------------------------------------------------------------
# Per-(k, seed) pipeline
# ---------------------------------------------------------------------------


def run_one(
    g_orig: nx.Graph,
    *,
    k: int,
    d: int,
    sigma: float,
    seed: int,
    attacks_cfg: dict,
) -> dict:
    """Execute the full pipeline for a single (k, seed) combination.

    Pipeline steps:

    1. Partition G into Local Structures (He et al. §3.1).
    2. Group LSs via FSM + MF factor (§3.2).
    3. Make each group isomorphic (§3.2, Phases 1 & 2).
    4. Reconnect inter-partition edges → G' (§3.3).
    5. Independent k-anonymity audit (``validate_k_anonymity``).
    6. Structural attacks on every node in G' (degree and/or subgraph).
    7. Aggregate metrics: reidentification_rate, equivalence_group_size,
       ks_test_degree, clustering_variation.

    Parameters
    ----------
    g_orig:
        Pre-processed original graph (immutable; not modified in place).
    k:
        k-anonymity parameter for this run.
    d:
        Local Structure size (partition granularity).
    sigma:
        FSM minimum support fraction.
    seed:
        Random seed; must come from the experiment YAML, never hardcoded.
    attacks_cfg:
        The ``attacks:`` block from the experiment YAML, controlling which
        attacks are enabled and their hyper-parameters.

    Returns
    -------
    dict
        JSONL-ready result dict.  On any unrecoverable exception, the
        ``"error"`` key contains the serialised exception; the other metric
        keys may be absent.  The result is always serialisable with
        ``json.dumps(result, default=str)``.
    """
    result: dict = {
        "k": k,
        "d": d,
        "seed": seed,
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "error": None,
    }

    try:
        # ------------------------------------------------------------------
        # Step 1 — Partition into Local Structures (He et al. §3.1)
        # ------------------------------------------------------------------
        local_structures, partition_meta = _partition_neighborhoods(
            g_orig, d=d, seed=seed, backend="auto", return_meta=True
        )
        n_ls = len(local_structures)
        # Record the engine actually used so results are self-documenting:
        # pymetis (faithful to He et al., D-04) vs networkx-kl (fallback,
        # known sizing degradation for ck>2). See docs/algorithm_notes.md §7.
        result["partition_backend"] = partition_meta["backend_used"]
        logger.info(
            "  [k=%d, seed=%d] Local structures: %d (backend=%s)",
            k,
            seed,
            n_ls,
            partition_meta["backend_used"],
        )

        # ------------------------------------------------------------------
        # Step 2 — Group LSs via FSM + MF factor (§3.2)
        # ------------------------------------------------------------------
        groups = _group_isomorphic(local_structures, k=k, sigma=sigma, seed=seed)
        n_groups = len(groups)
        group_sizes = [len(grp) for grp in groups]
        complete = sum(1 for s in group_sizes if s >= k)
        logger.info(
            "  [k=%d, seed=%d] Groups: %d (%d complete, %d incomplete)",
            k,
            seed,
            n_groups,
            complete,
            n_groups - complete,
        )

        # ------------------------------------------------------------------
        # Step 3 — Make each group isomorphic (§3.2, Phases 1 & 2)
        # ------------------------------------------------------------------
        modified_groups = _modify_structure(groups, seed=seed, add_only=False)

        # ------------------------------------------------------------------
        # Step 4 — Reconnect inter-partition edges → G' (§3.3)
        # ------------------------------------------------------------------
        g_anon = _reconnect_inter_edges(g_orig, modified_groups)

        # ------------------------------------------------------------------
        # Step 5 — Independent k-anonymity audit
        # ------------------------------------------------------------------
        validation_result = validate_k_anonymity(modified_groups, k=k)
        result["validate_k_anonymity"] = validation_result
        logger.info(
            "  [k=%d, seed=%d] valid=%s, coverage=%.4f, structural=%s",
            k,
            seed,
            validation_result["valid"],
            validation_result["coverage_fraction"],
            validation_result["deficit_fully_structural"],
        )

        # ------------------------------------------------------------------
        # Step 6 — Attacks
        # ------------------------------------------------------------------
        nodes = list(g_orig.nodes())

        # Degree attack (primary, enabled by default)
        degree_cfg = attacks_cfg.get("degree", {})
        if degree_cfg.get("enabled", True):
            tolerance = int(degree_cfg.get("tolerance", 0))
            degree_results = [
                degree_attack(g_orig, g_anon, node, tolerance=tolerance) for node in nodes
            ]
            rr_degree = reidentification_rate(degree_results)
            result["reidentification_rate_degree"] = rr_degree
            logger.info(
                "  [k=%d, seed=%d] Degree attack: reidentification_rate=%.4f",
                k,
                seed,
                rr_degree,
            )

        # Subgraph attack (optional; disabled by default — O(n²·VF2) per run)
        subgraph_cfg = attacks_cfg.get("subgraph", {})
        if subgraph_cfg.get("enabled", False):
            hop = int(subgraph_cfg.get("hop", 1))
            timeout = subgraph_cfg.get("timeout", None)
            subgraph_results = [
                subgraph_attack(g_orig, g_anon, node, hop=hop, timeout=timeout) for node in nodes
            ]
            rr_subgraph = reidentification_rate(subgraph_results)
            result["reidentification_rate_subgraph"] = rr_subgraph
            logger.info(
                "  [k=%d, seed=%d] Subgraph attack: reidentification_rate=%.4f",
                k,
                seed,
                rr_subgraph,
            )

        # Canonical "reidentification_rate": subgraph if enabled, else degree.
        if "reidentification_rate_subgraph" in result:
            result["reidentification_rate"] = result["reidentification_rate_subgraph"]
        elif "reidentification_rate_degree" in result:
            result["reidentification_rate"] = result["reidentification_rate_degree"]

        # ------------------------------------------------------------------
        # Step 7 — Metrics
        # ------------------------------------------------------------------
        eg_mean, eg_median = equivalence_group_size(modified_groups)
        result["equivalence_group_size"] = {"mean": eg_mean, "median": eg_median}

        ks_d, ks_p = ks_test_degree(g_orig, g_anon)
        result["ks_test_degree"] = {"D": ks_d, "p": ks_p}

        try:
            cv = clustering_variation(g_orig, g_anon)
            result["clustering_variation"] = cv
        except ValueError as exc:
            logger.warning("  [k=%d, seed=%d] clustering_variation undefined: %s", k, seed, exc)
            result["clustering_variation"] = None
            result["clustering_variation_error"] = str(exc)

    except Exception as exc:
        logger.error("  [k=%d, seed=%d] Pipeline error: %s", k, seed, exc)
        result["error"] = {
            "type": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc(),
        }

    return result


# ---------------------------------------------------------------------------
# Verdict
# ---------------------------------------------------------------------------


def verdict_from_result(result: dict) -> str:
    """Classify a single (k, seed) result into a verdict string.

    Verdict hierarchy (DL-01):

    * ``"SUCCESS_FULL"`` — ``valid=True``, no violations.
    * ``"SUCCESS_PARTIAL"`` — only ``"incomplete_group"`` violations AND
      ``coverage_fraction >= 0.9`` AND ``deficit_fully_structural=True``
      (D-06 acceptable).
    * ``"FAILURE_FATAL"`` — any ``"non_isomorphic"`` or ``"non_disjoint"``
      violation (algorithm bug; experiment must be halted).
    * ``"FAILURE_LOW_COVERAGE"`` — ``coverage_fraction < 0.9`` with no fatal
      violations.
    * ``"ERROR"`` — unrecoverable exception during the pipeline.

    Parameters
    ----------
    result:
        Dict returned by :func:`run_one`.

    Returns
    -------
    str
        One of the five verdict strings above.
    """
    if result.get("error"):
        return "ERROR"

    validation = result.get("validate_k_anonymity")
    if not validation:
        return "ERROR"

    if validation.get("valid", False):
        return "SUCCESS_FULL"

    violations = validation.get("violations", [])
    violation_types = {v["type"] for v in violations}
    has_fatal = bool(violation_types & {"non_isomorphic", "non_disjoint"})

    if has_fatal:
        return "FAILURE_FATAL"

    coverage = validation.get("coverage_fraction", 0.0)
    structural = validation.get("deficit_fully_structural", False)

    if structural and coverage >= 0.9:
        return "SUCCESS_PARTIAL"

    return "FAILURE_LOW_COVERAGE"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(config_path: Path) -> int:
    """Load config, run all (k, seed) combinations, write logs.

    Parameters
    ----------
    config_path:
        Path to the experiment YAML.

    Returns
    -------
    int
        0 if every run reached SUCCESS_FULL or SUCCESS_PARTIAL;
        1 if any run returned FAILURE_* or ERROR.
    """
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    exp_cfg = config.get("experiment", {})
    exp_name = exp_cfg.get("name", config_path.stem)

    # --- Logging level ---
    runtime_cfg = config.get("runtime", {})
    log_level = runtime_cfg.get("log_level", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level.upper(), logging.INFO))

    logger.info("=" * 60)
    logger.info("Experiment: %s", exp_name)
    logger.info("Config:     %s", config_path)

    # --- Dataset ---
    g_orig = load_dataset(config["dataset"])
    logger.info("Graph ready: n=%d, m=%d", g_orig.number_of_nodes(), g_orig.number_of_edges())

    # --- Anonymization parameters ---
    anon_cfg = config["anonymization"]
    k_values_raw = anon_cfg["k"]
    k_values: list[int] = (
        [int(k_values_raw)]
        if isinstance(k_values_raw, (int, float))
        else [int(k) for k in k_values_raw]
    )
    d = int(anon_cfg["d"])
    sigma = float(anon_cfg.get("sigma", 0.5))

    # --- Attacks ---
    attacks_cfg: dict = config.get("attacks", {"degree": {"enabled": True, "tolerance": 0}})

    # --- Seeds ---
    seeds: list[int] = [int(s) for s in config["seeds"]]

    # --- Log directory ---
    base_log_dir = Path(runtime_cfg.get("log_dir", "experiments/logs/"))
    log_dir = base_log_dir / exp_name
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{exp_name}.jsonl"

    logger.info("k values: %s, d=%d, sigma=%.2f, seeds=%s", k_values, d, sigma, seeds)
    logger.info("Log file: %s", log_file)

    # --- Run pipeline ---
    all_results: list[dict] = []
    any_failure = False

    for k in k_values:
        for seed in seeds:
            logger.info("--- k=%d, seed=%d ---", k, seed)
            result = run_one(
                g_orig,
                k=k,
                d=d,
                sigma=sigma,
                seed=seed,
                attacks_cfg=attacks_cfg,
            )
            result["experiment"] = exp_name
            v = verdict_from_result(result)
            result["verdict"] = v

            if v not in {"SUCCESS_FULL", "SUCCESS_PARTIAL"}:
                any_failure = True
                logger.error("  FAILURE: k=%d, seed=%d → %s", k, seed, v)
            else:
                logger.info("  OK: k=%d, seed=%d → %s", k, seed, v)

            # Write to JSONL immediately — don't accumulate failures silently.
            with log_file.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(result, default=str) + "\n")

            all_results.append(result)

    # --- Summary ---
    summary = {
        "experiment": exp_name,
        "config": str(config_path),
        "k_values": k_values,
        "d": d,
        "sigma": sigma,
        "seeds": seeds,
        "n_runs": len(all_results),
        "any_failure": any_failure,
        "partition_backends": sorted(
            {r["partition_backend"] for r in all_results if "partition_backend" in r}
        ),
        "verdicts": {
            f"k={r['k']}_seed={r['seed']}": r.get("verdict", "UNKNOWN") for r in all_results
        },
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }
    summary_file = log_dir / "summary.json"
    summary_file.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    # --- Human-readable report ---
    print("\n" + "=" * 60)
    print(f"EXPERIMENT: {exp_name}")
    print("=" * 60)
    print(f"k values: {k_values}  d={d}  sigma={sigma}")
    print(f"Seeds:    {seeds}")
    backends_used = summary["partition_backends"]
    print(f"Backend:  {', '.join(backends_used) if backends_used else 'N/A'}")
    if "networkx-kl" in backends_used:
        print(
            "  WARNING: networkx-kl fallback in use (pymetis unavailable). "
            "Results are a KL approximation — see docs/algorithm_notes.md §7 (D-04)."
        )
    print()
    for r in all_results:
        validation = r.get("validate_k_anonymity", {})
        rr = r.get("reidentification_rate")
        cov = validation.get("coverage_fraction", "N/A")
        cov_str = f"{cov:.4f}" if isinstance(cov, float) else str(cov)
        rr_str = f"{rr:.4f}" if isinstance(rr, float) else str(rr)
        print(
            f"  k={r['k']:>2}, seed={r['seed']:>6}: "
            f"{r.get('verdict', 'UNKNOWN'):<25} "
            f"coverage={cov_str:<8} rr={rr_str}"
        )
    print()
    status = "[FAILED]" if any_failure else "[PASSED]"
    print(f"Status: {status}")
    print(f"Log:    {log_file}")
    print("=" * 60)

    return 1 if any_failure else 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Experiment runner: anonymization + attacks + metrics pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Example:\n  python -m experiments.run --config experiments/configs/he2009_facebook_full.yml",
    )
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the experiment YAML configuration file.",
    )
    args = parser.parse_args()
    sys.exit(main(args.config))
