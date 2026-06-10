# Ensure the input dataset is present and create predictable output dirs (issue #184).
# Usage: ./scripts/replication/prepare_data.ps1 [-- --dataset facebook|enron] [--skip-download]
. (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '_common.ps1')
Invoke-Stage prepare-data @args
