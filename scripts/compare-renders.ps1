param(
  [Parameter(Mandatory = $true)][string]$BaselineDirectory,
  [Parameter(Mandatory = $true)][string]$CandidateDirectory,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [double]$MaximumDifferentRatio = 0.0,
  [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$python = if ($PythonPath) { $PythonPath } else { (Get-Command python -ErrorAction Stop).Source }
& $python (Join-Path $PSScriptRoot 'compare-renders.py') --baseline-dir $BaselineDirectory --candidate-dir $CandidateDirectory --output $OutputPath --max-different-ratio $MaximumDifferentRatio
exit $LASTEXITCODE
