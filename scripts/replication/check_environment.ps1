# Validate Python, dependencies and expected directories (issue #184).
# Usage: ./scripts/replication/check_environment.ps1
. (Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) '_common.ps1')
Invoke-Stage check-env @args
