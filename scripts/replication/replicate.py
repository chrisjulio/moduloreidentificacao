"""Independent, IDE-free replication driver for the He et al. (2009) pipeline.

This module is the single source of truth for terminal-based replication. The
``.ps1`` and ``.sh`` wrappers in this directory are thin shells that forward to
the stage subcommands defined here, so the orchestration logic lives in one
place (issue #184).

Pipeline mirrored from README.md §3.3 (canonical pipeline):

    check-env  ->  prepare-data  ->  run  ->  results

Subcommands
-----------
    check-env       Validate Python version, required packages and expected
                    directories. Reports the partition backend in use.
    prepare-data    Ensure the input dataset is present (downloads Facebook
                    Ego-Nets via the versioned loader when missing) and create
                    the predictable output directories.
    run             Execute one experiment config through ``experiments.run``.
    results         Regenerate plots and CSV tables from the structured JSONL
                    logs of a finished run.
    all             check-env -> prepare-data -> run -> results, end to end.

Design constraints (issue #184)
-------------------------------
* Relative/configurable paths only; never user-local absolutes. All paths are
  resolved against the repository root (the parent of ``scripts/``).
* Fails explicitly (non-zero exit, clear message) when dependencies, data or
  directories are missing.
* Every stage appends to a structured run log under
  ``experiments/logs/replication/`` for auditability.
* Operates only on the academically controlled SNAP datasets already wired
  into the project; it never identifies individuals and invents no results.

Usage
-----
Run from the repository root (the shell wrappers do this for you):

    python scripts/replication/replicate.py check-env
    python scripts/replication/replicate.py prepare-data --dataset facebook
    python scripts/replication/replicate.py run \\
        --config experiments/configs/he2009_facebook_baseline.yml
    python scripts/replication/replicate.py results \\
        --logs experiments/logs/he2009_facebook_baseline --dataset facebook
    python scripts/replication/replicate.py all \\
        --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook

Exit codes: 0 = stage succeeded; non-zero = explicit failure (see message).
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
import json
import logging
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

# Repository root = two levels up from this file (scripts/replication/replicate.py).
REPO_ROOT = Path(__file__).resolve().parents[2]

# Ensure ``import src.*`` works when this file is invoked by path (not -m),
# regardless of the caller's CWD — the backend probe in check-env needs it.
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Predictable, version-controlled-by-convention locations (all relative to root).
LOG_ROOT = REPO_ROOT / "experiments" / "logs"
REPLICATION_LOG_DIR = LOG_ROOT / "replication"
PLOTS_DIR = REPO_ROOT / "results" / "plots"
TABLES_DIR = REPO_ROOT / "results" / "tables"

# Minimum interpreter required by pyproject.toml (Python 3.11+).
MIN_PYTHON = (3, 11)

# Runtime packages the pipeline imports (see requirements.txt). pymetis is
# intentionally excluded: its absence is a documented soft fallback (D-04).
REQUIRED_PACKAGES = ("networkx", "numpy", "scipy", "matplotlib", "pandas", "yaml", "tqdm")

# Datasets the project knows how to fetch, mapped to their loader module and the
# directory the configs expect under data/raw/.
DATASETS = {
    "facebook": {
        "download_module": "src.loaders.download",
        "data_subdir": Path("data") / "raw" / "facebook",
    },
    "enron": {
        "download_module": "src.loaders.download_enron",
        "data_subdir": Path("data") / "raw" / "enron",
    },
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] replicate: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("scripts.replication.replicate")


# ---------------------------------------------------------------------------
# Structured audit log
# ---------------------------------------------------------------------------


def _append_audit(stage: str, status: str, details: dict) -> None:
    """Append one structured JSONL entry to the replication audit log.

    The log lets a reviewer reconstruct, after the fact, which stages ran with
    which parameters and how each finished (issue #184 auditability requirement).
    """
    REPLICATION_LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(tz=UTC).isoformat(),
        "stage": stage,
        "status": status,
        "python": sys.version.split()[0],
        "repo_root": str(REPO_ROOT),
        **details,
    }
    audit_file = REPLICATION_LOG_DIR / "replication_audit.jsonl"
    with audit_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, default=str) + "\n")
    logger.info("Audit: stage=%s status=%s -> %s", stage, status, audit_file)


class ReplicationError(RuntimeError):
    """Raised when a stage cannot proceed (missing deps/data/dirs/config)."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_module(module: str, args: list[str]) -> None:
    """Invoke ``python -m <module> <args>`` from the repo root, raising on failure.

    Reuses the existing project entrypoints rather than re-implementing them,
    so the replication path and the documented manual path stay identical.
    """
    cmd = [sys.executable, "-m", module, *args]
    logger.info("Running: %s", " ".join(cmd))
    completed = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    if completed.returncode != 0:
        raise ReplicationError(f"Command failed (exit {completed.returncode}): {' '.join(cmd)}")


def _resolve_in_repo(path_str: str) -> Path:
    """Resolve a possibly-relative path against the repo root.

    Absolute paths are honoured as-is so a reviewer may point at an external
    log directory, but the project's own configs always use relative paths.
    """
    p = Path(path_str)
    return p if p.is_absolute() else (REPO_ROOT / p)


# ---------------------------------------------------------------------------
# Stage: check-env
# ---------------------------------------------------------------------------


def stage_check_env() -> int:
    """Validate interpreter, packages and expected directories. Fail explicitly."""
    problems: list[str] = []

    # Python version.
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        problems.append(
            f"Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ required, found {current[0]}.{current[1]}."
        )
    else:
        logger.info("Python %d.%d OK (>= %d.%d).", *current, *MIN_PYTHON)

    # Required packages.
    missing = [pkg for pkg in REQUIRED_PACKAGES if importlib.util.find_spec(pkg) is None]
    if missing:
        problems.append(
            "Missing packages: "
            + ", ".join(missing)
            + ". Install with: pip install -r requirements.txt -r requirements-dev.txt"
        )
    else:
        logger.info("Required packages present: %s", ", ".join(REQUIRED_PACKAGES))

    # Expected project directories (must exist in a valid checkout).
    for rel in ("src", "experiments", "experiments/configs"):
        if not (REPO_ROOT / rel).is_dir():
            problems.append(f"Expected directory missing: {rel}")

    # Partition backend — informational, never fatal (D-04 fallback is valid).
    backend = "unknown"
    if not missing:
        try:
            mod = importlib.import_module("src.anonymization._partition_backend")
            backend = "pymetis" if mod.pymetis_available() else "networkx-kl (fallback, D-04)"
            logger.info("Partition backend: %s", backend)
        except Exception as exc:  # pragma: no cover - diagnostic only
            logger.warning("Could not determine partition backend: %s", exc)

    if problems:
        for p in problems:
            logger.error("ENV CHECK FAILED: %s", p)
        _append_audit("check-env", "FAILED", {"problems": problems, "backend": backend})
        raise ReplicationError(
            f"Environment check failed with {len(problems)} problem(s); see messages above."
        )

    logger.info("Environment check passed.")
    _append_audit("check-env", "OK", {"backend": backend})
    return 0


# ---------------------------------------------------------------------------
# Stage: prepare-data
# ---------------------------------------------------------------------------


def stage_prepare_data(dataset: str, *, skip_download: bool = False) -> int:
    """Ensure the input dataset exists and create predictable output dirs."""
    if dataset not in DATASETS:
        raise ReplicationError(
            f"Unknown dataset {dataset!r}. Supported: {', '.join(sorted(DATASETS))}."
        )

    spec = DATASETS[dataset]
    data_dir = REPO_ROOT / spec["data_subdir"]

    # Create predictable output directories up front so later stages never
    # fail on a missing parent.
    for d in (LOG_ROOT, REPLICATION_LOG_DIR, PLOTS_DIR, TABLES_DIR):
        d.mkdir(parents=True, exist_ok=True)

    present = data_dir.is_dir() and any(data_dir.iterdir())
    if present:
        logger.info("Dataset %s already present at %s", dataset, data_dir)
    elif skip_download:
        raise ReplicationError(
            f"Dataset {dataset!r} not found at {data_dir} and --skip-download was set. "
            f"Run the loader manually: python -m {spec['download_module']}"
        )
    else:
        logger.info("Dataset %s missing — invoking versioned loader.", dataset)
        _run_module(spec["download_module"], [])
        if not (data_dir.is_dir() and any(data_dir.iterdir())):
            raise ReplicationError(
                f"Loader ran but {data_dir} is still empty. Check network access "
                f"and the loader's output above."
            )

    _append_audit(
        "prepare-data",
        "OK",
        {"dataset": dataset, "data_dir": str(data_dir), "downloaded": not present},
    )
    logger.info("Data preparation complete for %s.", dataset)
    return 0


# ---------------------------------------------------------------------------
# Stage: run
# ---------------------------------------------------------------------------


def stage_run(config: str) -> int:
    """Execute one experiment config through the canonical runner."""
    config_path = _resolve_in_repo(config)
    if not config_path.is_file():
        raise ReplicationError(
            f"Config not found: {config_path}. Pass --config with a path relative to "
            f"the repo root, e.g. experiments/configs/he2009_facebook_baseline.yml"
        )

    rel_config = (
        config_path.relative_to(REPO_ROOT) if config_path.is_relative_to(REPO_ROOT) else config_path
    )
    _run_module("experiments.run", ["--config", str(rel_config)])

    _append_audit("run", "OK", {"config": str(rel_config)})
    logger.info("Experiment run complete for %s.", rel_config)
    return 0


# ---------------------------------------------------------------------------
# Stage: results
# ---------------------------------------------------------------------------


def stage_results(logs: str, dataset: str) -> int:
    """Regenerate plots and CSV tables from a finished run's JSONL logs."""
    logs_dir = _resolve_in_repo(logs)
    if not logs_dir.is_dir():
        raise ReplicationError(
            f"Logs directory not found: {logs_dir}. Run the experiment first (subcommand 'run')."
        )
    if not any(logs_dir.rglob("*.jsonl")):
        raise ReplicationError(
            f"No .jsonl logs under {logs_dir}. Did the experiment finish? "
            f"Run the experiment first (subcommand 'run')."
        )

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    rel_logs = logs_dir.relative_to(REPO_ROOT) if logs_dir.is_relative_to(REPO_ROOT) else logs_dir

    # NB: the two generators take different flags — privacy_utility labels output
    # via --stem (no --dataset), tables uses --dataset for its filenames. We feed
    # the dataset label to each in the form it accepts so artifacts stay tagged.
    _run_module(
        "src.visualization.privacy_utility",
        ["--logs", str(rel_logs), "--out", "results/plots", "--stem", f"privacy_utility_{dataset}"],
    )
    _run_module(
        "src.visualization.tables",
        ["--logs", str(rel_logs), "--dataset", dataset, "--out", "results/tables"],
    )

    _append_audit(
        "results",
        "OK",
        {
            "logs": str(rel_logs),
            "dataset": dataset,
            "plots": str(PLOTS_DIR),
            "tables": str(TABLES_DIR),
        },
    )
    logger.info("Results regenerated: plots -> %s, tables -> %s", PLOTS_DIR, TABLES_DIR)
    return 0


# ---------------------------------------------------------------------------
# Stage: all
# ---------------------------------------------------------------------------


def _default_logs_for_config(config: str) -> str:
    """Derive the experiment's log directory from its config stem.

    ``experiments.run`` writes to ``experiments/logs/<experiment.name>/``; the
    name defaults to the config file stem, which is also the convention used by
    every shipped config, so the stem is a safe default for the results stage.
    """
    stem = Path(config).stem
    return str(Path("experiments") / "logs" / stem)


def stage_all(config: str, dataset: str, *, skip_download: bool, logs: str | None) -> int:
    """End-to-end replication: check-env -> prepare-data -> run -> results."""
    stage_check_env()
    stage_prepare_data(dataset, skip_download=skip_download)
    stage_run(config)
    logs_dir = logs or _default_logs_for_config(config)
    stage_results(logs_dir, dataset)
    logger.info("Full replication finished successfully.")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="replicate",
        description="IDE-free replication driver for the He et al. (2009) pipeline.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="stage", required=True)

    sub.add_parser("check-env", help="Validate Python, packages and directories.")

    p_data = sub.add_parser("prepare-data", help="Ensure dataset present; make output dirs.")
    p_data.add_argument("--dataset", choices=sorted(DATASETS), default="facebook")
    p_data.add_argument(
        "--skip-download",
        action="store_true",
        help="Fail instead of downloading when the dataset is absent.",
    )

    p_run = sub.add_parser("run", help="Run one experiment config via experiments.run.")
    p_run.add_argument(
        "--config",
        required=True,
        help="Path to an experiment YAML (relative to repo root).",
    )

    p_res = sub.add_parser("results", help="Regenerate plots and tables from logs.")
    p_res.add_argument(
        "--logs",
        required=True,
        help="Logs directory of a finished run (relative to repo root).",
    )
    p_res.add_argument("--dataset", default="facebook", help="Dataset label for output naming.")

    p_all = sub.add_parser("all", help="check-env -> prepare-data -> run -> results.")
    p_all.add_argument("--config", required=True, help="Experiment YAML (relative to repo root).")
    p_all.add_argument("--dataset", choices=sorted(DATASETS), default="facebook")
    p_all.add_argument("--skip-download", action="store_true", help="Do not auto-download data.")
    p_all.add_argument(
        "--logs",
        default=None,
        help="Override the logs directory passed to the results stage "
        "(default: derived from the config file name).",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.stage == "check-env":
            return stage_check_env()
        if args.stage == "prepare-data":
            return stage_prepare_data(args.dataset, skip_download=args.skip_download)
        if args.stage == "run":
            return stage_run(args.config)
        if args.stage == "results":
            return stage_results(args.logs, args.dataset)
        if args.stage == "all":
            return stage_all(
                args.config,
                args.dataset,
                skip_download=args.skip_download,
                logs=args.logs,
            )
    except ReplicationError as exc:
        logger.error("%s", exc)
        return 2

    parser.error(f"Unknown stage: {args.stage}")
    return 2  # unreachable; parser.error exits


if __name__ == "__main__":
    sys.exit(main())
