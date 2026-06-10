#!/usr/bin/env bash
# Ensure the input dataset is present and create predictable output dirs (issue #184).
# Usage: ./scripts/replication/prepare_data.sh [--dataset facebook|enron] [--skip-download]
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"
run_stage prepare-data "$@"
