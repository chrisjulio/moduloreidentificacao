"""k-Sweep — Sanidade k∈{2,10,20} sobre ego-rede 3437 do Facebook.

Estende o marco 29/05 (k=5) para os demais valores de k do escopo Mínimo.
Cada k roda 3 sementes independentes com os mesmos parâmetros de base
(d=1, sigma=0.5, egonet_id=3437).

Uso:
    python -m experiments.run_k_sweep
    python -m experiments.run_k_sweep --configs <yaml1> <yaml2> ...

Saída:
    experiments/logs/k_sweep/k<N>/seed_<seed>.jsonl   — resultado por semente
    experiments/logs/k_sweep/k<N>/summary.json         — resumo por k
    experiments/logs/k_sweep/sweep_summary.json        — resumo geral do sweep
    Código de saída 0 → todos os k aprovados; 1 → ao menos um k falhou.

Referência: issue #17, DL-01, docs/decision_log.md.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

# Re-use core pipeline functions from the milestone script.
from experiments.run_milestone_29_05 import (
    evaluate_milestone,
    preprocess_graph,
    run_seed,
)
from src.loaders.facebook_ego import load_facebook_egonet

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("run_k_sweep")

# ---------------------------------------------------------------------------
# Default configs (one per k value required by issue #17)
# ---------------------------------------------------------------------------

_DEFAULT_CONFIGS = [
    Path("experiments/configs/he2009_facebook_k_sweep_k2.yml"),
    Path("experiments/configs/he2009_facebook_k_sweep_k10.yml"),
    Path("experiments/configs/he2009_facebook_k_sweep_k20.yml"),
]


# ---------------------------------------------------------------------------
# Per-config run
# ---------------------------------------------------------------------------


def run_config(config_path: Path) -> tuple[int, dict]:
    """Run full anonymize + validate pipeline for one k-sweep config.

    Parameters
    ----------
    config_path:
        Path to the YAML configuration file for this k value.

    Returns
    -------
    tuple[int, dict]
        (exit_code, per_k_summary) where exit_code is 0 for pass, 1 for fail.
    """
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
    log_dir = Path(val_cfg.get("log_dir", f"experiments/logs/k_sweep/k{k}/"))

    # --- Seeds ---
    seeds: list[int] = [int(s) for s in config["seeds"]]
    logger.info(
        "Running k-sweep config: k=%d, d=%d, seeds=%s, egonet=%d",
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

    # --- Per-k summary ---
    passed, reason = evaluate_milestone(results)

    per_k_summary = {
        "config": str(config_path),
        "graph": graph_info,
        "k": k,
        "d": d,
        "sigma": sigma,
        "seeds": seeds,
        "verdicts": {str(r["seed"]): r["verdict"] for r in results},
        "satisfied_fractions": {
            str(r["seed"]): r["validation"]["satisfied_fraction"] for r in results
        },
        "passed": passed,
        "reason": reason,
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }

    summary_file = log_dir / "summary.json"
    log_dir.mkdir(parents=True, exist_ok=True)
    summary_file.write_text(json.dumps(per_k_summary, indent=2, default=str), encoding="utf-8")
    logger.info("Per-k summary written: %s", summary_file)

    return (0 if passed else 1), per_k_summary


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(config_paths: list[Path]) -> int:
    """Run k-sweep over all provided config files; return exit code."""
    sweep_results: list[dict] = []
    any_failed = False

    print("\n" + "=" * 70)
    print("k-SWEEP — SANIDADE He et al. (2009) — Issue #17")
    print("=" * 70)

    for config_path in config_paths:
        if not config_path.exists():
            logger.error("Config not found: %s", config_path)
            sys.exit(1)

        logger.info("=== Config: %s ===", config_path)
        exit_code, per_k = run_config(config_path)
        sweep_results.append(per_k)

        k = per_k["k"]
        status = "[APROVADO]" if per_k["passed"] else "[REPROVADO]"
        print(f"\n  k={k:>2}  {status}")
        print(f"        Razão: {per_k['reason']}")
        for seed_str, verdict in per_k["verdicts"].items():
            sf = per_k["satisfied_fractions"][seed_str]
            print(f"        seed={seed_str:>6}: {verdict:<25} satisfied_fraction={sf:.4f}")

        if exit_code != 0:
            any_failed = True

    # --- Global sweep summary ---
    sweep_dir = Path("experiments/logs/k_sweep")
    sweep_dir.mkdir(parents=True, exist_ok=True)
    sweep_summary = {
        "sweep": "k_sweep_issue_17",
        "k_values": [r["k"] for r in sweep_results],
        "results": {str(r["k"]): r for r in sweep_results},
        "all_passed": not any_failed,
        "timestamp": datetime.now(tz=UTC).isoformat(),
    }
    sweep_file = sweep_dir / "sweep_summary.json"
    sweep_file.write_text(json.dumps(sweep_summary, indent=2, default=str), encoding="utf-8")

    print("\n" + "=" * 70)
    overall = "[TODOS APROVADOS]" if not any_failed else "[AO MENOS UM REPROVADO]"
    print(f"RESULTADO GERAL: {overall}")
    print(f"Sweep summary:   {sweep_file}")
    print("=" * 70)

    return 1 if any_failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="k-Sweep — validação He et al. (2009)")
    parser.add_argument(
        "--configs",
        nargs="+",
        type=Path,
        default=_DEFAULT_CONFIGS,
        help="Lista de YAMLs de configuração a executar (default: k=2, k=10, k=20).",
    )
    args = parser.parse_args()
    sys.exit(main(args.configs))
