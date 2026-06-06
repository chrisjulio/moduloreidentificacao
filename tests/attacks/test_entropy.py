"""Tests for src/attacks/entropy.py (issue #30 / D-17).

src/attacks/entropy.py is a cross-reference pointer: per decision D-17 the
"entropy attack" is the adversarial reading of the entropy **metric**, whose
implementation lives in src/metrics/entropy.py. These tests assert that the
pointer re-exports the canonical function (same object), so callers reaching
for ``src.attacks`` get the metric defined once — no divergent copy.
"""

from __future__ import annotations

import networkx as nx

from src.attacks import entropy_metrics as attacks_entropy_metrics
from src.attacks.entropy import entropy_metrics as attacks_module_entropy_metrics
from src.metrics.entropy import entropy_metrics as metrics_entropy_metrics


def test_attacks_pointer_is_metric_function() -> None:
    """The attacks re-export is the very same object as the metric (no copy)."""
    assert attacks_module_entropy_metrics is metrics_entropy_metrics
    assert attacks_entropy_metrics is metrics_entropy_metrics


def test_pointer_computes_same_result() -> None:
    """Sanity: invoking via the attacks pointer yields the metric's output."""
    group = [nx.path_graph(2), nx.relabel_nodes(nx.path_graph(2), {0: 2, 1: 3})]
    via_attack = attacks_module_entropy_metrics([group])
    via_metric = metrics_entropy_metrics([group])
    assert via_attack == via_metric
