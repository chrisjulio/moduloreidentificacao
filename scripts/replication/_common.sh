#!/usr/bin/env bash
# Shared helpers for the Bash replication wrappers (issue #184).
# Resolves the repository root from this file's location and picks a Python
# interpreter, so the wrappers work regardless of the caller's CWD and never
# depend on an IDE or a user-local absolute path.
set -euo pipefail

# Directory of the script that sourced us, then repo root (../../).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[1]:-${BASH_SOURCE[0]}}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DRIVER="${SCRIPT_DIR}/replicate.py"

# Prefer an activated virtualenv, then python3, then python. Fail explicitly.
pick_python() {
  if [[ -n "${VIRTUAL_ENV:-}" && -x "${VIRTUAL_ENV}/bin/python" ]]; then
    echo "${VIRTUAL_ENV}/bin/python"
  elif command -v python3 >/dev/null 2>&1; then
    command -v python3
  elif command -v python >/dev/null 2>&1; then
    command -v python
  else
    echo "ERROR: no python/python3 interpreter found on PATH." >&2
    exit 3
  fi
}

PYTHON="$(pick_python)"

run_stage() {
  # Always invoke from the repo root so the driver's relative paths resolve.
  cd "${REPO_ROOT}"
  exec "${PYTHON}" "${DRIVER}" "$@"
}
