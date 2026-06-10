#!/usr/bin/env bash
# Regenerate plots and CSV tables from a finished run's JSONL logs (issue #184).
# Usage:
#   ./scripts/replication/generate_results.sh \
#       --logs experiments/logs/he2009_facebook_baseline --dataset facebook
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run_stage results "$@"
