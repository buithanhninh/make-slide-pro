# Make Slide Pro V8.6.0 - 1-Click Sync to VPS (PowerShell)
param (
    [switch]$Watch,
    [switch]$NoRestart
)

$script = Join-Path $PSScriptRoot "scripts\sync_to_vps.py"
$argsList = @()
if ($Watch) { $argsList += "--watch" }
if ($NoRestart) { $argsList += "--no-restart" }

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "   MAKE SLIDE PRO V8.6.0 - SYNC TO VPS (hmu-vm-makeslidepro)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

python $script @argsList
