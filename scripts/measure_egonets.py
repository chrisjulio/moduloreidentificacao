"""Measure all Facebook ego-networks and select the median-sized one.

Applies the full preprocessing pipeline defined in preprocessing_decision.md:
  1. Remove the ego node (if present).
  2. Retain only the largest connected component (LCC).
  3. Convert to a simple graph (remove self-loops and parallel edges).

Outputs:
  - A metrics table (sorted by n_lcc) printed to stdout.
  - A JSON results file at data/processed/facebook/egonet_metrics.json.
  - The recommended egonet_id printed at the end.

Usage
-----
    python scripts/measure_egonets.py [--data-dir data/raw/facebook]
"""

import argparse
import json
import logging
from pathlib import Path

import networkx as nx

from src.loaders.facebook_ego import load_facebook_egonet

log = logging.getLogger(__name__)

# Ego-node IDs present in the SNAP Facebook archive.
EGO_IDS: list[int] = [0, 107, 348, 414, 686, 698, 1684, 1912, 3437, 3980]

MIN_NODES: int = 200  # Seção 3.3 of preprocessing_decision.md; 10 * k_max


def preprocess(raw: nx.Graph, egonet_id: int) -> nx.Graph:
    """Apply preprocessing pipeline: remove ego → LCC → simple graph."""
    g = raw.copy()
    # 1. Remove ego node if present.
    if egonet_id in g:
        g.remove_node(egonet_id)
    # 2. Largest connected component.
    largest_cc = max(nx.connected_components(g), key=len)
    g = g.subgraph(largest_cc).copy()
    # 3. Simple graph (removes self-loops; parallel edges not present in
    #    undirected graphs built from edge lists, but included for safety).
    g = nx.Graph(g)
    g.remove_edges_from(nx.selfloop_edges(g))
    return g


def measure_all(data_dir: Path, min_nodes: int = MIN_NODES) -> list[dict]:
    """Return a list of metric dicts, one per ego-network."""
    results = []
    for ego_id in EGO_IDS:
        raw = load_facebook_egonet(ego_id, data_dir)
        n_raw = raw.number_of_nodes()
        m_raw = raw.number_of_edges()
        n_components = nx.number_connected_components(raw)

        g = preprocess(raw, ego_id)
        n_lcc = g.number_of_nodes()
        m_lcc = g.number_of_edges()
        density = (2 * m_lcc / (n_lcc * (n_lcc - 1))) if n_lcc > 1 else 0.0
        passes = n_lcc >= min_nodes

        results.append(
            {
                "egonet_id": ego_id,
                "n_raw": n_raw,
                "m_raw": m_raw,
                "n_components": n_components,
                "n_lcc": n_lcc,
                "m_lcc": m_lcc,
                "density": round(density, 6),
                "passes_filter": passes,
            }
        )
        log.info(
            "ego=%d  n_raw=%d  m_raw=%d  comps=%d  n_lcc=%d  passes=%s",
            ego_id,
            n_raw,
            m_raw,
            n_components,
            n_lcc,
            passes,
        )

    return results


def select_median(results: list[dict]) -> dict | None:
    """Return the entry closest to the median n_lcc among those passing the filter."""
    passing = [r for r in results if r["passes_filter"]]
    if not passing:
        return None
    passing_sorted = sorted(passing, key=lambda r: r["n_lcc"])
    idx = (len(passing_sorted) - 1) // 2  # lower median for even-length lists
    return passing_sorted[idx]


def print_table(results: list[dict], min_nodes: int) -> None:
    """Print a formatted Markdown table of metrics."""
    header = (
        f"{'egonet_id':>10} | {'n_raw':>7} | {'m_raw':>8} | {'comps':>5} | "
        f"{'n_lcc':>6} | {'m_lcc':>7} | {'density':>9} | {('>=' + str(min_nodes) + '?'):>8}"
    )
    sep = "-" * len(header)
    print()
    print("## Ego-network metrics")
    print()
    print(header)
    print(sep)
    for r in sorted(results, key=lambda x: x["n_lcc"]):
        print(
            f"{r['egonet_id']:>10} | {r['n_raw']:>7} | {r['m_raw']:>8} | "
            f"{r['n_components']:>5} | {r['n_lcc']:>6} | {r['m_lcc']:>7} | "
            f"{r['density']:>9.6f} | {'yes' if r['passes_filter'] else 'no':>8}"
        )
    print()


def fallback_check(results: list[dict], min_nodes: int) -> str:
    """Return the fallback status as a string."""
    n_passing = sum(1 for r in results if r["passes_filter"])
    if n_passing >= 5:
        return f"CONFIRMED: {n_passing} ego-networks pass n >= {min_nodes} (>= 5 required)"
    elif n_passing >= 3:
        return (
            f"CONFIRMED with limitation note: {n_passing} ego-networks pass n >= {min_nodes} "
            f"(3-4 range)"
        )
    else:
        return (
            f"FALLBACK TRIGGERED: only {n_passing} ego-network(s) pass n >= {min_nodes}. "
            f"Revise threshold to n >= 100."
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/raw/facebook"),
        help="Directory containing downloaded ego-network subdirectories.",
    )
    parser.add_argument(
        "--min-nodes",
        type=int,
        default=MIN_NODES,
        help="Minimum n_lcc to pass the size filter.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("data/processed/facebook/egonet_metrics.json"),
        help="Path to write JSON results.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )

    results = measure_all(args.data_dir, args.min_nodes)
    print_table(results, args.min_nodes)

    fb_status = fallback_check(results, args.min_nodes)
    print(f"## Fallback check\n{fb_status}\n")

    selected = select_median(results)
    if selected is not None:
        print(
            f"## Selected ego-network\n"
            f"egonet_id = {selected['egonet_id']}  "
            f"(n_lcc={selected['n_lcc']}, m_lcc={selected['m_lcc']}, "
            f"density={selected['density']:.6f})\n"
            f"Median index among {sum(1 for r in results if r['passes_filter'])} "
            f"passing networks.\n"
        )
    else:
        print("## Selected ego-network\nNone passed the filter — trigger fallback.\n")

    # Write JSON output
    args.out.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "min_nodes_threshold": args.min_nodes,
        "fallback_status": fb_status,
        "selected_egonet_id": selected["egonet_id"] if selected else None,
        "ego_networks": results,
    }
    args.out.write_text(json.dumps(output, indent=2))
    log.info("Results written to %s", args.out)


if __name__ == "__main__":
    main()
