"""Re-identification rate metric.

Measures the fraction of target nodes successfully re-identified by a
structural attack (``degree_attack`` or ``subgraph_attack``).

Privacy interpretation
----------------------
* Rate = 0.0 → no target was uniquely identified; anonymisation fully
  defeats the attack on this sample.
* Rate = 1.0 → every target was uniquely identified; anonymisation
  provides no protection against the tested attack.

Reference: He et al. (2009), Section 1-2 (threat model).
"""

from __future__ import annotations


def reidentification_rate(attack_results: list[bool]) -> float:
    """Compute the fraction of targets successfully re-identified.

    Parameters
    ----------
    attack_results:
        Boolean outcomes from a structural attack (e.g., ``degree_attack``
        or ``subgraph_attack``). Each element is ``True`` if the
        corresponding target was uniquely re-identified in the anonymised
        graph, ``False`` otherwise (zero or multiple candidates).

    Returns
    -------
    float
        Fraction of ``True`` values in ``attack_results``, in [0.0, 1.0].
        Returns ``0.0`` when the list is empty (no targets evaluated →
        no successful re-identification by definition).

    Notes
    -----
    * The rate is computed over all targets in ``attack_results`` regardless
      of which attack produced them; it is the caller's responsibility to
      pass results from a single, consistent attack.
    * A higher rate indicates weaker privacy; a lower rate indicates stronger
      protection against the particular attack modelled.
    * Complexity: O(n) where n = ``len(attack_results)``.
    """
    if not attack_results:
        return 0.0
    return sum(attack_results) / len(attack_results)
