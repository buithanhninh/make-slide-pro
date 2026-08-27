param(
  [Parameter(Mandatory = $true)][ValidateSet('init', 'status', 'next', 'submit', 'skip', 'invalidate', 'recover')][string]$Action,
  [Parameter(Mandatory = $true)][string]$Workspace,
  [Parameter(Mandatory = $true)][string]$RegistryPath,
  [string]$PayloadPath,
  [string]$OwnerId = 'make-slide-pro-manager',
  [string]$LeaseToken,
  [int]$LeaseDurationSeconds = 300,
  [switch]$RecoverExpired
)

$ErrorActionPreference = 'Stop'
$python = $null
if ($env:RUNTIME_PYTHON) {
  $runtimeCandidates = @($env:RUNTIME_PYTHON -split '[\r\n;]+') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
  foreach ($candidate in $runtimeCandidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { $python = $candidate; break }
  }
}
if (-not $python) {
  $pythonCommand = @(Get-Command python -CommandType Application -ErrorAction Stop | Where-Object { $_.Source -and (Test-Path -LiteralPath $_.Source -PathType Leaf) } | Select-Object -First 1)
  if ($pythonCommand.Count -eq 0) { throw 'PYTHON_RUNTIME_UNAVAILABLE' }
  $python = [string]$pythonCommand[0].Source
}
$core = Join-Path $PSScriptRoot 'orchestrator_core.py'
$arguments = @($core, '--action', $Action, '--workspace', $Workspace, '--registry', $RegistryPath, '--owner-id', $OwnerId, '--lease-duration-seconds', $LeaseDurationSeconds)
if ($PayloadPath) { $arguments += @('--payload', $PayloadPath) }
if ($LeaseToken) { $arguments += @('--lease-token', $LeaseToken) }
if ($RecoverExpired) { $arguments += '--recover-expired' }
& $python @arguments
exit $LASTEXITCODE
