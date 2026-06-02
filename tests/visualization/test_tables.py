"""Tests for src/visualization/tables.py.

Seeds are fixed in all fixtures because tests must be deterministic.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from src.visualization.tables import (
    CSV_COLUMNS,
    generate_tables,
    load_jsonl_records,
    record_to_row,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_record(
    k: int,
    seed: int,
    rr_degree: float = 0.1,
    rr_subgraph: float = 0.5,
    eq_mean: float = 3.5,
    ks_d: float = 0.12,
    ks_p: float = 0.45,
    clust_var: float = 0.07,
    d: int = 1,
    *,
    include_subgraph: bool = True,
) -> dict:
    """Build a minimal valid JSONL record with controllable metric values."""
    rec: dict = {
        "k": k,
        "d": d,
        "seed": seed,
        "reidentification_rate": rr_degree,
        "reidentification_rate_degree": rr_degree,
        "equivalence_group_size": {"mean": eq_mean, "median": int(k)},
        "ks_test_degree": {"D": ks_d, "p": ks_p},
        "clustering_variation": clust_var,
        "verdict": "SUCCESS_FULL",
    }
    if include_subgraph:
        rec["reidentification_rate_subgraph"] = rr_subgraph
    return rec


def _write_jsonl(path: Path, records: list[dict]) -> None:
    """Serialise *records* as one JSON line each to *path*."""
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sample_records() -> list[dict]:
    """12 records: k in {2,5,10,20} x 3 seeds with predictable metric values."""
    records = []
    for k in [2, 5, 10, 20]:
        for seed in [42, 1337, 2718]:
            records.append(
                _make_record(
                    k=k,
                    seed=seed,
                    rr_degree=0.1 / k,
                    rr_subgraph=0.8 / k,
                    eq_mean=float(k),
                    ks_d=0.05 * k,
                    ks_p=0.5,
                    clust_var=0.02 * k,
                )
            )
    return records


@pytest.fixture
def logs_dir(tmp_path: Path, sample_records: list[dict]) -> Path:
    """Temporary directory with a single JSONL file containing all records."""
    log_file = tmp_path / "run.jsonl"
    _write_jsonl(log_file, sample_records)
    return tmp_path


@pytest.fixture
def dsweep_records() -> list[dict]:
    """48 records: k in {2,5,10,20} x d in {1,2,5,10} x 3 seeds (the d-sweep grid)."""
    records = []
    for k in [2, 5, 10, 20]:
        for d in [1, 2, 5, 10]:
            for seed in [42, 1337, 2718]:
                records.append(
                    _make_record(
                        k=k,
                        seed=seed,
                        d=d,
                        # Make values depend on both k and d so cells are distinguishable.
                        rr_degree=0.1 / k + 0.001 * d,
                        rr_subgraph=0.8 / k + 0.001 * d,
                        eq_mean=float(k * d),
                        ks_d=0.05 * k,
                        ks_p=0.5,
                        clust_var=0.02 * k,
                    )
                )
    return records


# ---------------------------------------------------------------------------
# CSV_COLUMNS spec
# ---------------------------------------------------------------------------


class TestCsvColumnsSpec:
    def test_d_column_present(self) -> None:
        assert "d" in CSV_COLUMNS

    def test_d_immediately_follows_k(self) -> None:
        assert CSV_COLUMNS[0] == "k"
        assert CSV_COLUMNS[1] == "d"

    def test_full_column_order(self) -> None:
        assert CSV_COLUMNS == (
            "k",
            "d",
            "seed",
            "reid_rate",
            "eq_group_mean",
            "ks_D",
            "ks_p",
            "clustering_var",
        )


# ---------------------------------------------------------------------------
# load_jsonl_records
# ---------------------------------------------------------------------------


class TestLoadJsonlRecords:
    def test_loads_all_valid_records(self, logs_dir: Path, sample_records: list[dict]) -> None:
        records = load_jsonl_records(logs_dir)
        assert len(records) == len(sample_records)

    def test_raises_if_dir_missing(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="logs_dir not found"):
            load_jsonl_records(tmp_path / "nonexistent")

    def test_skips_invalid_json_lines(self, tmp_path: Path) -> None:
        log_file = tmp_path / "run.jsonl"
        with log_file.open("w", encoding="utf-8") as fh:
            fh.write('{"k": 5, "seed": 1}\n')
            fh.write("not-json\n")
            fh.write('{"k": 10, "seed": 2}\n')
        records = load_jsonl_records(tmp_path)
        assert len(records) == 2

    def test_skips_blank_lines(self, tmp_path: Path) -> None:
        log_file = tmp_path / "run.jsonl"
        with log_file.open("w", encoding="utf-8") as fh:
            fh.write('{"k": 5, "seed": 1}\n')
            fh.write("\n")
            fh.write("\n")
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_skips_records_without_k(self, tmp_path: Path) -> None:
        log_file = tmp_path / "run.jsonl"
        with log_file.open("w", encoding="utf-8") as fh:
            fh.write('{"seed": 1, "reidentification_rate_degree": 0.1}\n')
            fh.write('{"k": 5, "seed": 2}\n')
        records = load_jsonl_records(tmp_path)
        assert len(records) == 1

    def test_reads_multiple_jsonl_files(self, tmp_path: Path) -> None:
        for i in range(3):
            _write_jsonl(
                tmp_path / f"run_{i}.jsonl",
                [_make_record(k=5, seed=i)],
            )
        records = load_jsonl_records(tmp_path)
        assert len(records) == 3

    def test_reads_recursively(self, tmp_path: Path) -> None:
        sub = tmp_path / "sub"
        sub.mkdir()
        _write_jsonl(tmp_path / "a.jsonl", [_make_record(k=2, seed=0)])
        _write_jsonl(sub / "b.jsonl", [_make_record(k=5, seed=1)])
        records = load_jsonl_records(tmp_path)
        assert len(records) == 2

    def test_empty_directory_returns_empty_list(self, tmp_path: Path) -> None:
        records = load_jsonl_records(tmp_path)
        assert records == []


# ---------------------------------------------------------------------------
# record_to_row
# ---------------------------------------------------------------------------


class TestRecordToRow:
    def test_degree_row_has_all_columns(self) -> None:
        rec = _make_record(k=5, seed=42)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert set(row.keys()) == set(CSV_COLUMNS)

    def test_subgraph_row_has_all_columns(self) -> None:
        rec = _make_record(k=5, seed=42)
        row = record_to_row(rec, "subgraph")
        assert row is not None
        assert set(row.keys()) == set(CSV_COLUMNS)

    def test_degree_reid_rate_correct(self) -> None:
        rec = _make_record(k=5, seed=42, rr_degree=0.123)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert abs(row["reid_rate"] - 0.123) < 1e-9

    def test_subgraph_reid_rate_correct(self) -> None:
        rec = _make_record(k=5, seed=42, rr_subgraph=0.456)
        row = record_to_row(rec, "subgraph")
        assert row is not None
        assert abs(row["reid_rate"] - 0.456) < 1e-9

    def test_ks_fields_extracted(self) -> None:
        rec = _make_record(k=5, seed=42, ks_d=0.18, ks_p=0.03)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert abs(row["ks_D"] - 0.18) < 1e-9
        assert abs(row["ks_p"] - 0.03) < 1e-9

    def test_eq_group_mean_extracted(self) -> None:
        rec = _make_record(k=10, seed=42, eq_mean=7.25)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert abs(row["eq_group_mean"] - 7.25) < 1e-9

    def test_clustering_var_extracted(self) -> None:
        rec = _make_record(k=5, seed=42, clust_var=0.031)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert abs(row["clustering_var"] - 0.031) < 1e-9

    def test_k_and_seed_are_int(self) -> None:
        rec = _make_record(k=10, seed=1337)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert isinstance(row["k"], int)
        assert isinstance(row["seed"], int)

    def test_d_extracted(self) -> None:
        rec = _make_record(k=10, seed=1337, d=5)
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["d"] == 5
        assert isinstance(row["d"], int)

    def test_d_defaults_to_one_when_absent(self) -> None:
        rec = _make_record(k=5, seed=42)
        del rec["d"]
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["d"] == 1

    def test_returns_none_if_attack_absent(self) -> None:
        rec = _make_record(k=5, seed=42, include_subgraph=False)
        row = record_to_row(rec, "subgraph")
        assert row is None

    def test_returns_none_if_degree_absent(self) -> None:
        rec = {"k": 5, "seed": 42}
        row = record_to_row(rec, "degree")
        assert row is None

    def test_raises_on_unknown_attack(self) -> None:
        rec = _make_record(k=5, seed=42)
        with pytest.raises(ValueError, match="Unknown attack"):
            record_to_row(rec, "entropy")  # type: ignore[arg-type]

    def test_ks_none_when_field_absent(self) -> None:
        rec = _make_record(k=5, seed=42)
        del rec["ks_test_degree"]
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["ks_D"] is None
        assert row["ks_p"] is None

    def test_eq_group_mean_none_when_field_absent(self) -> None:
        rec = _make_record(k=5, seed=42)
        del rec["equivalence_group_size"]
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["eq_group_mean"] is None

    def test_clustering_var_none_when_null(self) -> None:
        rec = _make_record(k=5, seed=42)
        rec["clustering_variation"] = None
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["clustering_var"] is None

    def test_default_seed_when_absent(self) -> None:
        rec = _make_record(k=5, seed=99)
        del rec["seed"]
        row = record_to_row(rec, "degree")
        assert row is not None
        assert row["seed"] == -1


# ---------------------------------------------------------------------------
# generate_tables
# ---------------------------------------------------------------------------


class TestGenerateTables:
    def test_produces_two_csv_files(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        assert set(produced.keys()) == {"degree", "subgraph"}

    def test_csv_files_exist(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        for path in produced.values():
            assert path.exists()

    def test_filename_convention(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        assert produced["degree"].name == "facebook_degree.csv"
        assert produced["subgraph"].name == "facebook_subgraph.csv"

    def test_custom_dataset_name(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="enron")
        assert produced["degree"].name == "enron_degree.csv"

    def test_csv_has_correct_columns(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert tuple(reader.fieldnames or []) == CSV_COLUMNS

    def test_csv_row_count_matches_records(
        self, tmp_path: Path, sample_records: list[dict]
    ) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        # 4 k values * 3 seeds = 12 rows
        assert len(rows) == 12

    def test_rows_sorted_by_k_then_seed(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        pairs = [(int(r["k"]), int(r["seed"])) for r in rows]
        assert pairs == sorted(pairs)

    def test_k_values_correct(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            k_values = {int(r["k"]) for r in csv.DictReader(fh)}
        assert k_values == {2, 5, 10, 20}

    def test_reid_rate_values_correct(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        for row in rows:
            k = int(row["k"])
            expected = 0.1 / k
            assert abs(float(row["reid_rate"]) - expected) < 1e-9

    def test_subgraph_reid_rate_values_correct(
        self, tmp_path: Path, sample_records: list[dict]
    ) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["subgraph"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        for row in rows:
            k = int(row["k"])
            expected = 0.8 / k
            assert abs(float(row["reid_rate"]) - expected) < 1e-9

    def test_output_dir_created(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "deep" / "nested" / "tables"
        generate_tables(sample_records, out, dataset="facebook")
        assert out.is_dir()

    def test_raises_on_empty_records(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="No records"):
            generate_tables([], tmp_path, dataset="facebook")

    def test_raises_on_empty_attacks(self, tmp_path: Path, sample_records: list[dict]) -> None:
        with pytest.raises(ValueError, match="attacks"):
            generate_tables(sample_records, tmp_path, dataset="facebook", attacks=())

    def test_single_attack_filter(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook", attacks=("degree",))
        assert set(produced.keys()) == {"degree"}
        assert not (out / "facebook_subgraph.csv").exists()

    def test_skips_attack_absent_from_all_records(self, tmp_path: Path) -> None:
        records = [_make_record(k=5, seed=i, include_subgraph=False) for i in range(3)]
        out = tmp_path / "tables"
        produced = generate_tables(records, out, dataset="facebook")
        assert "degree" in produced
        assert "subgraph" not in produced

    def test_overwrite_existing_csv(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        generate_tables(sample_records, out, dataset="facebook")
        # Run again — should overwrite without error
        produced = generate_tables(sample_records, out, dataset="facebook")
        assert produced["degree"].exists()

    def test_ks_fields_in_csv(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            row = next(csv.DictReader(fh))
        assert float(row["ks_D"]) > 0
        assert float(row["ks_p"]) > 0

    def test_eq_group_mean_in_csv(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            row = next(csv.DictReader(fh))
        # eq_mean == float(k) in sample_records; k=2 is the first after sort
        assert float(row["eq_group_mean"]) == pytest.approx(2.0)

    def test_clustering_var_in_csv(self, tmp_path: Path, sample_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(sample_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            row = next(csv.DictReader(fh))
        # clust_var == 0.02 * k; k=2 → 0.04
        assert float(row["clustering_var"]) == pytest.approx(0.04)

    def test_none_values_written_as_empty_string(self, tmp_path: Path) -> None:
        records = [
            {
                "k": 5,
                "seed": 0,
                "reidentification_rate_degree": 0.1,
                # no ks_test_degree, no equivalence_group_size, clustering_variation=None
                "clustering_variation": None,
            }
        ]
        out = tmp_path / "tables"
        produced = generate_tables(records, out, dataset="facebook", attacks=("degree",))
        with produced["degree"].open(encoding="utf-8") as fh:
            row = next(csv.DictReader(fh))
        assert row["ks_D"] == ""
        assert row["ks_p"] == ""
        assert row["eq_group_mean"] == ""
        assert row["clustering_var"] == ""


# ---------------------------------------------------------------------------
# generate_tables — d-sweep (d as a first-class dimension)
# ---------------------------------------------------------------------------


class TestGenerateTablesDSweep:
    def test_csv_has_d_column(self, tmp_path: Path, dsweep_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(dsweep_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            assert "d" in (reader.fieldnames or [])

    def test_row_count_is_full_grid(self, tmp_path: Path, dsweep_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(dsweep_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        # 4 k * 4 d * 3 seeds = 48 rows
        assert len(rows) == 48

    def test_sixteen_distinct_k_d_cells(self, tmp_path: Path, dsweep_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(dsweep_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            cells = {(int(r["k"]), int(r["d"])) for r in csv.DictReader(fh)}
        assert len(cells) == 16
        assert cells == {(k, d) for k in [2, 5, 10, 20] for d in [1, 2, 5, 10]}

    def test_rows_sorted_by_k_d_seed(self, tmp_path: Path, dsweep_records: list[dict]) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(dsweep_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        triples = [(int(r["k"]), int(r["d"]), int(r["seed"])) for r in rows]
        assert triples == sorted(triples)

    def test_d_values_distinguish_same_k_seed(
        self, tmp_path: Path, dsweep_records: list[dict]
    ) -> None:
        out = tmp_path / "tables"
        produced = generate_tables(dsweep_records, out, dataset="facebook")
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh) if int(r["k"]) == 2 and int(r["seed"]) == 42]
        # Same (k, seed) but four distinct d → four distinct rows.
        assert sorted(int(r["d"]) for r in rows) == [1, 2, 5, 10]

    def test_fallback_d_one_for_records_without_d(self, tmp_path: Path) -> None:
        records = []
        for seed in range(3):
            rec = _make_record(k=5, seed=seed)
            del rec["d"]
            records.append(rec)
        out = tmp_path / "tables"
        produced = generate_tables(records, out, dataset="facebook", attacks=("degree",))
        with produced["degree"].open(encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert all(int(r["d"]) == 1 for r in rows)
