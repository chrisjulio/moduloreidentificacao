# Regenerate plots and CSV tables from a finished run's JSONL logs (issue #184).
# Usage:
#   ./scripts/replication/generate_results.ps1 `
#       --logs experiments/logs/he2009_facebook_baseline --dataset facebook
. (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '_common.ps1')
Invoke-Stage results @args
