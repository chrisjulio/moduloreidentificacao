#!/usr/bin/env bash
# Full end-to-end replication orchestrator: check-env -> prepare-data -> run -> results.
# (issue #184)
#
# Full pipeline (default):
#   ./scripts/replication/run_experiment.sh \
#       --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook
#
# Single experiment stage only (skip env/data/results):
#   ./scripts/replication/run_experiment.sh --only-run \
#       --config experiments/configs/he2009_facebook_baseline.yml
source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

# --only-run forwards just the experiment stage; otherwise run the full flow.
if [[ "${1:-}" == "--only-run" ]]; then
  shift
  run_stage run "$@"
else
  run_stage all "$@"
fi
