"""Marco 29/05 — Sanidade k=5, d=1 sobre ego-rede 3437 do Facebook.

Verifica empiricamente (3 sementes) que anonymize(G, k=5, d=1, seed)
produz grupos com k-anonimato estrutural válido ou parcialmente válido
conforme o critério D-06 / DL-01 (docs/decision_log.md).

Uso:
    python -m experiments.run_milestone_29_05
    python -m experiments.run_milestone_29_05 --config experiments/configs/milestone_29_05.yml

Saída:
    experiments/logs/milestone_29_05/<seed>.jsonl  — resultado por semente
    experiments/logs/milestone_29_05/summary.json  — resumo geral
    Código de saída 0 → aprovado; 1 → reprovado.

Referência: issue #16, DL-01, docs/decision_log.md.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

import networkx as nx
import yaml

from src.anonymization.he2009 import (
    _group_isomorphic,
    _modify_structure,
    _partition_neighborhoods,
)
from src.anonymization.validation import validate_k_anonymity
from src.loaders.facebook_ego import load_facebook_egonet

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("milestone_29_05")


# ---------------------------------------------------------------------------
# Pre-processing
# ---------------------------------------------------------------------------


def preprocess_graph(
    g: nx.Graph,
    component: str = "lcc",
    min_nodes: int = 0,
) -> nx.Graph:
    """Extract the pre-processed graph from a raw ego-network.

    Parameters
    ----------
    g:
        Raw ego-network loaded by load_facebook_egonet.
    component:
        ``"lcc"`` to retain only the largest connected component (default).
        Any other value keeps the graph as-is.
    min_nodes:
        Minimum number of nodes in the processed graph. Raises ValueError
        if the graph is smaller than this threshold after pre-processing.

    Returns
    -------
    nx.Graph
        Pre-processed graph (relabeled 0..n-1 for clean integer node IDs).
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

    # Relabel nodes 0..n-1 for consistent integer IDs.
    g = nx.convert_node_labels_to_integers(g)
    return g


# ---------------------------------------------------------------------------
# Per-seed run
# ---------------------------------------------------------------------------


def run_seed(
    g: nx.Graph,
    *,
    k: int,
    d: int,
    sigma: float,
    seed: int,
    log_dir: Path,
) -> dict:
    """Run the full anonymize + validate pipeline for one seed.

    Parameters
    ----------
    g:
        Pre-processed input graph.
    k:
        k-anonymity parameter.
    d:
        Local Structure size (partition granularity).
    sigma:
        FSM minimum support fraction.
    seed:
        Random seed for this run.
    log_dir:
        Directory where the per-seed JSONL log is written.

    Returns
    -------
    dict
        Per-seed result with keys:
        ``seed``, ``n_nodes``, ``n_edges``, ``k``, ``d``,
        ``n_local_structures``, ``n_groups``, ``validation``,
        ``verdict``, ``timestamp``.
    """
    logger.info("--- Seed %d ---", seed)

    # Step 1: Partition into Local Structures.
    local_structures = _partition_neighborhoods(g, d=d, seed=seed, backend="auto")
    n_ls = len(local_structures)
    logger.info("  Local structures: %d (d=%d, n=%d)", n_ls, d, g.number_of_nodes())

    # Step 2: Group LSs via FSM + MF.
    groups = _group_isomorphic(local_structures, k=k, sigma=sigma, seed=seed)
    n_groups = len(groups)
    group_sizes = [len(grp) for grp in groups]
    complete = sum(1 for s in group_sizes if s >= k)
    incomplete = n_groups - complete
    logger.info(
        "  Groups: %d total (%d complete, %d incomplete/D-06)",
        n_groups,
        complete,
        incomplete,
    )

    # Step 3: Make each group isomorphic.
    modified = _modify_structure(groups, seed=seed, add_only=False)

    # Step 4: Independent k-anonymity audit.
    validation = validate_k_anonymity(modified, k=k)

    # Determine verdict per DL-01 criteria.
    violation_types = {v["type"] for v in validation["violations"]}
    has_fatal = bool(violation_types & {"non_isomorphic", "non_disjoint"})
    sf = validation["satisfied_fraction"]

    if validation["valid"]:
        verdict = "SUCCESS_FULL"
    elif not has_fatal and sf >= 0.9:
        verdict = "SUCCESS_PARTIAL"  # D-06 acceptable
    elif has_fatal:
        verdict = "FAILURE_FATAL"
    else:
        verdict = "FAILURE_LOW_COVERAGE"

    logger.info(
        "  valid=%s, satisfied_fraction=%.4f, violations=%s → %s",
        validation["valid"],
        sf,
        [v["type"] for v in validation["violations"]],
        verdict,
    )

    result = {
        "seed": seed,
        "n_nodes": g.number_of_nodes(),
        "n_edges": g.number_of_edges(),
        "k": k,
        "d": d,
        "sigma": sigma,
        "n_local_structures": n_ls,
        "n_groups": n_groups,
        "group_sizes": {
            "min": min(group_sizes),
            "max": max(group_sizes),
            "complete": complete,
            "incomplete": incomplete,
        },
        "validation": validation,
        "verdict": verdict,
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }

    # Write per-seed log.
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"seed_{seed}.jsonl"
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(result, default=str) + "\n")
    logger.info("  Log written: %s", log_file)

    return result


# ---------------------------------------------------------------------------
# Summary evaluation (DL-01)
# ---------------------------------------------------------------------------


def evaluate_milestone(results: list[dict]) -> tuple[bool, str]:
    """Evaluate the milestone pass/fail criterion (DL-01).

    Parameters
    ----------
    results:
        List of per-seed results from run_seed.

    Returns
    -------
    tuple[bool, str]
        (passed, reason) where reason is a human-readable explanation.
    """
    verdicts = [r["verdict"] for r in results]

    # All seeds must reach SUCCESS_FULL or SUCCESS_PARTIAL.
    passing = {"SUCCESS_FULL", "SUCCESS_PARTIAL"}
    failing = [v for v in verdicts if v not in passing]

    if not failing:
        if all(v == "SUCCESS_FULL" for v in verdicts):
            return True, "Sucesso pleno: valid=True em todas as sementes."
        else:
            frac_min = min(r["validation"]["satisfied_fraction"] for r in results)
            return (
                True,
                (
                    f"Sucesso parcial aceitável (D-06): apenas incomplete_group, "
                    f"satisfied_fraction mínimo={frac_min:.4f} >= 0.9."
                ),
            )
    else:
        details = "; ".join(
            f"seed={r['seed']} → {r['verdict']}" for r in results if r["verdict"] not in passing
        )
        return False, f"FALHA: {details}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(config_path: Path) -> int:
    """Run the milestone validation; return exit code (0=pass, 1=fail)."""
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    # --- Dataset ---
    ds = config["dataset"]
    data_dir = Path(ds["data_path"])
    egonet_id = int(ds["egonet_id"])
    component = ds.get("component", "lcc")
    min_nodes = int(ds.get("min_nodes", 0))

    logger.info("Loading egonet_id=%d from %s", egonet_id, data_dir)
    g_raw = load_facebook_egonet(egonet_id, data_dir)
    logger.info("Raw graph: n=%d, m=%d", g_raw.number_of_nodes(), g_raw.number_of_edges())

    g = preprocess_graph(g_raw, component=component, min_nodes=min_nodes)
    graph_info = {
        "egonet_id": egonet_id,
        "n_nodes": g.number_of_nodes(),
        "n_edges": g.number_of_edges(),
    }
    logger.info("Pre-processed: n=%d, m=%d", g.number_of_nodes(), g.number_of_edges())

    # --- Anonymization parameters ---
    anon = config["anonymization"]
    k = int(anon["k"])
    d = int(anon["d"])
    sigma = float(anon.get("sigma", 0.5))

    # --- Log directory ---
    val_cfg = config.get("validation", {})
    log_dir = Path(val_cfg.get("log_dir", "experiments/logs/milestone_29_05/"))

    # --- Seeds ---
    seeds: list[int] = [int(s) for s in config["seeds"]]
    logger.info(
        "Running milestone: k=%d, d=%d, seeds=%s, egonet=%d",
        k,
        d,
        seeds,
        egonet_id,
    )

    # --- Per-seed runs ---
    results: list[dict] = []
    for seed in seeds:
        result = run_seed(g, k=k, d=d, sigma=sigma, seed=seed, log_dir=log_dir)
        results.append(result)

    # --- Summary ---
    passed, reason = evaluate_milestone(results)

    summary = {
        "milestone": "marco_29_05",
        "graph": graph_info,
        "k": k,
        "d": d,
        "sigma": sigma,
        "seeds": seeds,
        "verdicts": {str(r["seed"]): r["verdict"] for r in results},
        "satisfied_fractions": {
            str(r["seed"]): r["validation"]["satisfied_fraction"] for r in results
        },
        "milestone_passed": passed,
        "reason": reason,
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }

    summary_file = log_dir / "summary.json"
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_file.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

    # --- Report ---
    print("\n" + "=" * 60)
    print("MARCO 29/05 — RESULTADO")
    print("=" * 60)
    print(f"Grafo: egonet_id={egonet_id}, n={graph_info['n_nodes']}, m={graph_info['n_edges']}")
    print(f"Parâmetros: k={k}, d={d}, sigma={sigma}")
    print(f"Sementes: {seeds}")
    print()
    for r in results:
        v = r["validation"]
        print(
            f"  seed={r['seed']:>6}: {r['verdict']:<25} "
            f"valid={v['valid']!s:<5} "
            f"satisfied_fraction={v['satisfied_fraction']:.4f} "
            f"n_violators={v['n_violators']}"
        )
    print()
    status = "[APROVADO]" if passed else "[REPROVADO]"
    print(f"Status: {status}")
    print(f"Razão:  {reason}")
    print(f"Log:    {summary_file}")
    print("=" * 60)

    return 0 if passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Marco 29/05 — validação k-anonimato")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/configs/milestone_29_05.yml"),
        help="Caminho para o YAML de configuração.",
    )
    args = parser.parse_args()
    sys.exit(main(args.config))
