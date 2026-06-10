# Full end-to-end replication orchestrator: check-env -> prepare-data -> run -> results.
# (issue #184)
#
# Full pipeline (default):
#   ./scripts/replication/run_experiment.ps1 `
#       --config experiments/configs/he2009_facebook_baseline.yml --dataset facebook
#
# Single experiment stage only (skip env/data/results):
#   ./scripts/replication/run_experiment.ps1 --only-run `
#       --config experiments/configs/he2009_facebook_baseline.yml
. (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '_common.ps1')

if ($args.Count -gt 0 -and $args[0] -eq '--only-run') {
    $rest = $args[1..($args.Count - 1)]
    Invoke-Stage run @rest
}
else {
    Invoke-Stage all @args
}
