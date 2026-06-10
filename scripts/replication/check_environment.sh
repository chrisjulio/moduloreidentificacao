#!/usr/bin/env bash
# Validate Python, dependencies and expected directories (issue #184).
# Usage: ./scripts/replication/check_environment.sh
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run_stage check-env "$@"
