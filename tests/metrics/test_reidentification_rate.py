"""Tests for src/metrics/reidentification_rate.py (issue #21).

Definition-of-Done coverage:
    - Empty list → 0.0 (no targets evaluated).
    - All True → 1.0 (every target re-identified).
    - All False → 0.0 (no target re-identified).
    - Mixed list → correct fraction.
    - Single True → 1.0.
    - Single False → 0.0.
    - Large list → precise fraction.

reidentification_rate() is deterministic and seed-free.
"""

from __future__ import annotations

import pytest

from src.metrics.reidentification_rate import reidentification_rate

# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestReidentificationRateEdgeCases:
    """Boundary inputs that require special handling."""

    def test_empty_list_returns_zero(self) -> None:
        """Empty list has no re-identifications → rate is 0.0 by convention.

        An empty result set means no targets were evaluated; there is no
        successful re-identification to account for.
        """
        assert reidentification_rate([]) == 0.0

    def test_single_true(self) -> None:
        """One target evaluated and re-identified → rate is 1.0."""
        assert reidentification_rate([True]) == 1.0

    def test_single_false(self) -> None:
        """One target evaluated but not re-identified → rate is 0.0."""
        assert reidentification_rate([False]) == 0.0


# ---------------------------------------------------------------------------
# Uniform outcomes
# ---------------------------------------------------------------------------


class TestReidentificationRateUniform:
    """Uniform lists where all targets share the same outcome."""

    def test_all_true_returns_one(self) -> None:
        """Every target re-identified → rate is 1.0."""
        assert reidentification_rate([True, True, True]) == 1.0

    def test_all_false_returns_zero(self) -> None:
        """No target re-identified → rate is 0.0."""
        assert reidentification_rate([False, False, False]) == 0.0

    def test_all_true_large_list(self) -> None:
        """100 True values → rate is 1.0 regardless of list length."""
        assert reidentification_rate([True] * 100) == 1.0

    def test_all_false_large_list(self) -> None:
        """100 False values → rate is 0.0 regardless of list length."""
        assert reidentification_rate([False] * 100) == 0.0


# ---------------------------------------------------------------------------
# Mixed outcomes — correct fraction
# ---------------------------------------------------------------------------


class TestReidentificationRateMixed:
    """Mixed lists verify exact fractional arithmetic."""

    def test_half_identified(self) -> None:
        """2 True out of 4 total → rate is exactly 0.5."""
        result = reidentification_rate([True, False, True, False])
        assert result == pytest.approx(0.5)

    def test_one_third_identified(self) -> None:
        """1 True out of 3 total → rate is 1/3."""
        result = reidentification_rate([True, False, False])
        assert result == pytest.approx(1 / 3)

    def test_two_thirds_identified(self) -> None:
        """2 True out of 3 total → rate is 2/3."""
        result = reidentification_rate([True, True, False])
        assert result == pytest.approx(2 / 3)

    def test_one_out_of_ten(self) -> None:
        """1 True out of 10 → rate is 0.1."""
        results = [True] + [False] * 9
        assert reidentification_rate(results) == pytest.approx(0.1)

    def test_nine_out_of_ten(self) -> None:
        """9 True out of 10 → rate is 0.9."""
        results = [True] * 9 + [False]
        assert reidentification_rate(results) == pytest.approx(0.9)


# ---------------------------------------------------------------------------
# Return type and range
# ---------------------------------------------------------------------------


class TestReidentificationRateReturnType:
    """Ensure the function always returns a float in [0, 1]."""

    def test_returns_float_for_all_true(self) -> None:
        assert isinstance(reidentification_rate([True, True]), float)

    def test_returns_float_for_all_false(self) -> None:
        assert isinstance(reidentification_rate([False, False]), float)

    def test_returns_float_for_empty(self) -> None:
        assert isinstance(reidentification_rate([]), float)

    def test_result_in_unit_interval(self) -> None:
        """Rate must always be in [0.0, 1.0]."""
        for n_true in range(6):
            results = [True] * n_true + [False] * (5 - n_true)
            rate = reidentification_rate(results)
            assert 0.0 <= rate <= 1.0
