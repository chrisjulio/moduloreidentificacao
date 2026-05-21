"""Auditor independente de k-anonimato estrutural (He et al., 2009).

Este modulo implementa a verificacao empirica de k-anonimato conforme a
Definicao 2 de He et al. (2009) e as decisoes D-05 e D-06 documentadas em
docs/algorithm_notes.md §7.

O verificador e completamente independente do anonimizador -- nao reutiliza
nenhum codigo de src/anonymization/he2009.py.  Isso garante que violacoes
causadas por bugs no algoritmo sejam detetaveis pelo auditor externo.

Condicoes verificadas (docs/metrics_definitions.md §k-anonymity-verifier §4):

1. **Disjuncao global** -- cada no pertence a exatamente uma LS.
2. **Cardinalidade minima** -- cada grupo tem pelo menos k LSs.
3. **Isomorfismo mutuo** -- todas as LSs de um grupo completo sao
   mutualmente isomorfas (Def. 2, He et al. 2009, p. 649).

Referencia: docs/metrics_definitions.md §k-anonymity-verifier.
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path

import networkx as nx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Log destination
# ---------------------------------------------------------------------------

_LOG_DIR = Path("experiments/logs")
_LOG_FILE = _LOG_DIR / "validate_k_anonymity.jsonl"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def validate_k_anonymity(
    groups: list[list[nx.Graph]],
    k: int,
) -> dict:
    """Verify structure-aware k-anonymity independently of the anonymizer.

    Applies the three mandatory validation conditions defined in
    docs/metrics_definitions.md §k-anonymity-verifier §4.

    Parameters
    ----------
    groups : list[list[nx.Graph]]
        Partition of Local Structures (LSs) into equivalence groups, as
        produced by _group_isomorphic followed by _modify_structure.
        ``groups[r][j]`` is the j-th LS in group r; each LS carries the
        original node IDs from the anonymized graph G'.
    k : int
        Target anonymity level. A group is *complete* if ``len(group) >= k``.

    Returns
    -------
    dict
        Structured validation report with the following keys:

        ``valid`` : bool
            ``True`` iff there are **no** violations of any kind.
        ``satisfied_fraction`` : float
            Fraction of nodes (in [0, 1]) that satisfy Def. 2.
        ``n_violators`` : int
            Number of nodes that do *not* satisfy Def. 2.
        ``violators`` : list
            Sorted list of violating node IDs.
        ``violations`` : list[dict]
            One entry per violation; each dict has keys:

            * ``type``: ``"non_disjoint"`` | ``"incomplete_group"``
              | ``"non_isomorphic"``
            * ``status``: ``"unprotected"`` | ``"partially_unprotected"``
            * ``nodes``: sorted list of affected node IDs

    Notes
    -----
    * **Auditor independence**: does not import anything from he2009.py.
    * **Deterministic**: same input always produces the same output.
    * Appends one JSONL entry to ``experiments/logs/validate_k_anonymity.jsonl``
      on every call. Write failures are silently caught and emitted as
      ``logging.WARNING`` so that the audit result is never withheld due to
      I/O errors.

    References
    ----------
    He et al. (2009) Def. 2, p. 649.
    docs/metrics_definitions.md §k-anonymity-verifier.
    D-05 and D-06 in docs/algorithm_notes.md §7.
    """
    violations: list[dict] = []
    violating_nodes: set = set()

    # ------------------------------------------------------------------
    # Build node → LS-location index.
    # node_occurrences[node] = list of (r, j) for every LS that contains it.
    # ------------------------------------------------------------------
    node_occurrences: dict[object, list[tuple[int, int]]] = {}
    for r, group in enumerate(groups):
        for j, ls in enumerate(group):
            for node in ls.nodes():
                node_occurrences.setdefault(node, []).append((r, j))

    all_nodes: set = set(node_occurrences)
    n_total = len(all_nodes)

    # ------------------------------------------------------------------
    # Condition 1 — Global disjunction.
    # Each node must appear in exactly one LS across all groups.
    # ------------------------------------------------------------------
    non_disjoint = sorted(node for node, locs in node_occurrences.items() if len(locs) > 1)
    if non_disjoint:
        violations.append(
            {
                "type": "non_disjoint",
                "status": "unprotected",
                "nodes": list(non_disjoint),
            }
        )
        violating_nodes.update(non_disjoint)

    # ------------------------------------------------------------------
    # Conditions 2 & 3 — Cardinality and mutual isomorphism per group.
    # ------------------------------------------------------------------
    for _r, group in enumerate(groups):
        n_ls = len(group)

        # Condition 2: cardinality (D-06 case)
        if n_ls < k:
            group_nodes: list = []
            for ls in group:
                group_nodes.extend(ls.nodes())
            violations.append(
                {
                    "type": "incomplete_group",
                    "status": "partially_unprotected",
                    "nodes": sorted(group_nodes),
                }
            )
            violating_nodes.update(group_nodes)
            continue  # no isomorphism check for incomplete groups

        # Condition 3: mutual isomorphism — O(k(k-1)/2) VF2 calls per group.
        non_iso_nodes: set = set()
        for i in range(n_ls):
            for j in range(i + 1, n_ls):
                if not nx.is_isomorphic(group[i], group[j]):
                    non_iso_nodes.update(group[i].nodes())
                    non_iso_nodes.update(group[j].nodes())

        if non_iso_nodes:
            violations.append(
                {
                    "type": "non_isomorphic",
                    "status": "unprotected",
                    "nodes": sorted(non_iso_nodes),
                }
            )
            violating_nodes.update(non_iso_nodes)

    # ------------------------------------------------------------------
    # Aggregate statistics.
    # ------------------------------------------------------------------
    n_violators = len(violating_nodes)
    valid = len(violations) == 0
    satisfied_fraction = (n_total - n_violators) / n_total if n_total > 0 else 1.0

    report: dict = {
        "valid": valid,
        "satisfied_fraction": round(satisfied_fraction, 6),
        "n_violators": n_violators,
        "violators": sorted(violating_nodes),
        "violations": violations,
    }

    _append_log(report, k=k)
    return report


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _append_log(report: dict, *, k: int) -> None:
    """Append one JSONL entry to the validation log.

    Non-fatal: silently warns via logging if the file cannot be written.
    """
    try:
        _LOG_DIR.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "k": k,
            **report,
        }
        with _LOG_FILE.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str) + "\n")
    except OSError as exc:
        logger.warning("validate_k_anonymity: could not write log entry: %s", exc)
