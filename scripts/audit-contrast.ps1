param(
  [Parameter(Mandatory = $true)][string]$ManifestPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$python = if ($PythonPath) { (Resolve-Path -LiteralPath $PythonPath).Path } else { (Get-Command python -ErrorAction Stop).Source }
& $python (Join-Path $PSScriptRoot 'audit-contrast.py') --manifest $ManifestPath --output $OutputPath
exit $LASTEXITCODE
