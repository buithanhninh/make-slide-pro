param(
  [Parameter(Mandatory = $true)][string]$AssetsPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [double]$MinimumPpi = 150,
  [double]$HeroMinimumPpi = 180,
  [string]$PythonPath
)

$ErrorActionPreference = 'Stop'
$python = if ($PythonPath) { (Resolve-Path -LiteralPath $PythonPath).Path } else { (Get-Command python -ErrorAction Stop).Source }
& $python (Join-Path $PSScriptRoot 'audit-images.py') --assets $AssetsPath --output $OutputPath --minimum-ppi $MinimumPpi --hero-minimum-ppi $HeroMinimumPpi
exit $LASTEXITCODE
