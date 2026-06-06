"""Entropy attack — adversarial reading of the entropy privacy metric.

This module is a **cross-reference pointer**, not an autonomous structural
attack.  Decision D-17 (docs/decision_log.md) classifies the "entropy attack"
of the operational plan (Section 4.4) as the *adversarial reading* of a
**privacy metric** whose primary home is ``src/metrics/entropy.py``:

* Unlike ``degree_attack`` / ``subgraph_attack``, it uses **no** background
  knowledge about the original graph ``G_orig`` — it is derived purely from
  the equivalence partition produced by the He et al. (2009) pipeline.
* It is grounded in the entropy-as-anonymity literature (Serjantov & Danezis
  2002; Díaz et al. 2002), which frames Shannon entropy as a *metric of
  anonymity*, not an attack procedure.

The adversarial reading: ``H(v) = log2(n_r)`` is the residual uncertainty (in
bits) an adversary faces after narrowing target ``v`` to its equivalence
group of ``n_r`` nodes; ``reidentification_rate_entropy`` (fraction of nodes
with ``H(v) <= tau``) is the metric's attack-side summary.

Use :func:`src.metrics.entropy.entropy_metrics` directly; it is re-exported
here for callers reaching for ``src.attacks`` by analogy with the other
attacks.  See docs/metrics_definitions.md (§ entropy) and D-17.
"""

from __future__ import annotations

from src.metrics.entropy import entropy_metrics

__all__ = ["entropy_metrics"]
