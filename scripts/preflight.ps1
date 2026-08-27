param(
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [ValidateSet('CERTIFIED', 'CREATE', 'EDIT', 'AUDIT', 'CERTIFY', 'MEDIA')]
  [string]$Mode = 'CERTIFIED',
  [string]$TargetPath = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

function Test-CommandAvailable {
  param([string]$Name, [string]$PreferredPath)
  if ($PreferredPath) {
    $fullPath = [System.IO.Path]::GetFullPath($PreferredPath)
    return [ordered]@{ available = Test-Path -LiteralPath $fullPath -PathType Leaf; path = if (Test-Path -LiteralPath $fullPath -PathType Leaf) { $fullPath } else { $null }; source = 'RUNTIME_ENV' }
  }
  $command = Get-Command $Name -ErrorAction SilentlyContinue
  return [ordered]@{ available = $null -ne $command; path = if ($command) { $command.Source } else { $null }; source = if ($command) { 'SYSTEM_PATH' } else { 'NONE' } }
}

function Test-ComAvailable {
  param([string]$ProgId)
  $application = $null
  try {
    $application = New-Object -ComObject $ProgId
    if ($ProgId -eq 'PowerPoint.Application') { Set-PowerPointSafeAutomation -Application $application }
    $version = [string]$application.Version
    $application.Quit()
    return [ordered]@{ available = $true; version = $version }
  } catch {
    return [ordered]@{ available = $false; version = $null; error = $_.Exception.Message }
  } finally {
    Release-ComObject -Object $application
  }
}

function Test-ArtifactToolRuntime {
  param(
    [Parameter(Mandatory = $true)][object]$Node,
    [string]$RuntimeModules
  )
  $result = [ordered]@{
    available = $false
    directory_present = $false
    importable = $false
    path = $null
    runtime_modules = $RuntimeModules
  }
  if (-not $Node.available) {
    $result.error = 'NODE_RUNTIME_UNAVAILABLE'
    return $result
  }
  if ([string]::IsNullOrWhiteSpace($RuntimeModules)) {
    $result.error = 'RUNTIME_NODE_MODULES_UNRESOLVED'
    return $result
  }
  try {
    $resolvedModules = Get-NormalizedFullPath -Path $RuntimeModules
    Assert-NoReparseAncestors -Path $resolvedModules
    $artifactPath = Get-NormalizedFullPath -Path (Join-Path $resolvedModules '@oai\artifact-tool')
    Assert-NoReparseAncestors -Path $artifactPath
    $result.path = $artifactPath
    if (-not (Test-Path -LiteralPath $artifactPath -PathType Container)) {
      $result.error = 'ARTIFACT_TOOL_DIRECTORY_MISSING'
      return $result
    }
    $result.directory_present = $true
    $entryPath = Get-NormalizedFullPath -Path (Join-Path $artifactPath 'dist\artifact_tool.mjs')
    if (-not (Test-PathInsideDirectory -Path $entryPath -Directory $artifactPath) -or -not (Test-Path -LiteralPath $entryPath -PathType Leaf)) {
      $result.error = 'ARTIFACT_TOOL_ENTRYPOINT_MISSING'
      return $result
    }
    Assert-NoReparseAncestors -Path $entryPath
    $probeScript = "import { pathToFileURL } from 'node:url'; import(pathToFileURL(process.argv[1]).href).then(() => process.exit(0)).catch((error) => { console.error(String(error?.message || error)); process.exit(1); });"
    $probeOutput = @(& $Node.path --input-type=module -e $probeScript -- $entryPath 2>&1)
    $probeExitCode = $LASTEXITCODE
    $result.import_exit_code = $probeExitCode
    if ($probeExitCode -eq 0) {
      $result.importable = $true
      $result.available = $true
    } else {
      $errorText = ((@($probeOutput | ForEach-Object { [string]$_ })) -join ' ').Trim()
      $result.error = if ($errorText) { $errorText.Substring(0, [Math]::Min(500, $errorText.Length)) } else { 'ARTIFACT_TOOL_IMPORT_FAILED' }
    }
  } catch {
    $result.error = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  }
  return $result
}

$resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
try {
  $resolvedTarget = Get-NormalizedFullPath -Path $TargetPath
  if (Test-Path -LiteralPath $resolvedTarget) { Assert-NoReparseAncestors -Path $resolvedTarget }
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedTarget) -Label 'PREFLIGHT_OUTPUT')
} catch {
  [Console]::Error.WriteLine(($_.Exception.Message -replace '[\r\n]+', ' ').Trim())
  exit 2
}
$powerPoint = Test-ComAvailable -ProgId 'PowerPoint.Application'
$word = Test-ComAvailable -ProgId 'Word.Application'
$excel = Test-ComAvailable -ProgId 'Excel.Application'
$node = Test-CommandAvailable -Name 'node' -PreferredPath $env:RUNTIME_NODE
$python = Test-CommandAvailable -Name 'python'
$runtimeBin = if ($env:RUNTIME_BIN_DIR) { [System.IO.Path]::GetFullPath($env:RUNTIME_BIN_DIR) } else { $null }
$ffmpegPreferred = if ($runtimeBin) { Join-Path $runtimeBin 'ffmpeg.exe' } else { $null }
$ffprobePreferred = if ($runtimeBin) { Join-Path $runtimeBin 'ffprobe.exe' } else { $null }
$ffmpeg = Test-CommandAvailable -Name 'ffmpeg' -PreferredPath $ffmpegPreferred
if (-not $ffmpeg.available -and $ffmpegPreferred) { $ffmpeg = Test-CommandAvailable -Name 'ffmpeg' }
$ffprobe = Test-CommandAvailable -Name 'ffprobe' -PreferredPath $ffprobePreferred
if (-not $ffprobe.available -and $ffprobePreferred) { $ffprobe = Test-CommandAvailable -Name 'ffprobe' }
$tesseract = Test-CommandAvailable -Name 'tesseract'

$runtimeModules = $env:RUNTIME_NODE_MODULES
$artifactTool = Test-ArtifactToolRuntime -Node $node -RuntimeModules $runtimeModules
$runtimeBinReport = [ordered]@{ available = $runtimeBin -and (Test-Path -LiteralPath $runtimeBin -PathType Container); path = $runtimeBin }

$pythonProbe = [ordered]@{ available = $false; version = $null; faster_whisper = $false; pytesseract = $false; jsonschema = $false }
if ($python.available) {
  try {
    $probe = & $python.path -c "import sys, importlib.util; print(sys.version.split()[0]); print(bool(importlib.util.find_spec('faster_whisper'))); print(bool(importlib.util.find_spec('pytesseract'))); print(bool(importlib.util.find_spec('jsonschema')))" 2>$null
    if ($probe.Count -ge 4) {
      $pythonProbe.available = $true
      $pythonProbe.version = [string]$probe[0]
      $pythonProbe.faster_whisper = [System.Convert]::ToBoolean([string]$probe[1])
      $pythonProbe.pytesseract = [System.Convert]::ToBoolean([string]$probe[2])
      $pythonProbe.jsonschema = [System.Convert]::ToBoolean([string]$probe[3])
    }
  } catch {}
}

$drive = [System.IO.Path]::GetPathRoot($resolvedTarget)
$driveInfo = [System.IO.DriveInfo]::new($drive)
$nvidia = Test-CommandAvailable -Name 'nvidia-smi'
$issues = [System.Collections.Generic.List[object]]::new()
$authoringRequired = $Mode -in @('CERTIFIED', 'CREATE', 'EDIT')
$mediaRequired = $Mode -eq 'MEDIA'

if (-not $powerPoint.available) { $issues.Add([ordered]@{ code = 'POWERPOINT_NATIVE_MISSING'; severity = 'BLOCK'; status = 'fail' }) }
if ($authoringRequired -and -not $node.available) { $issues.Add([ordered]@{ code = 'RUNTIME_NODE_MISSING'; severity = 'BLOCK'; status = 'fail' }) }
if ($authoringRequired -and -not $artifactTool.available) {
  $artifactIssueCode = if ($artifactTool.directory_present) { 'ARTIFACT_TOOL_IMPORT_FAILED' } else { 'ARTIFACT_TOOL_UNRESOLVED' }
  $issues.Add([ordered]@{ code = $artifactIssueCode; severity = 'BLOCK'; status = 'fail'; detail = [string]$artifactTool.error })
}
if ($authoringRequired -and -not $runtimeBinReport.available) { $issues.Add([ordered]@{ code = 'RUNTIME_BIN_DIR_UNRESOLVED'; severity = 'BLOCK'; status = 'fail' }) }
if (-not $python.available) { $issues.Add([ordered]@{ code = 'PYTHON_MISSING'; severity = 'WARN'; status = 'unknown' }) }
elseif (-not $pythonProbe.available) { $issues.Add([ordered]@{ code = 'PYTHON_PROBE_FAILED'; severity = 'WARN'; status = 'unknown' }) }
elseif (-not $pythonProbe.jsonschema) { $issues.Add([ordered]@{ code = 'JSONSCHEMA_RUNTIME_MISSING'; severity = 'WARN'; status = 'unknown' }) }
if (($mediaRequired -or $Mode -eq 'CERTIFIED') -and (-not $ffmpeg.available -or -not $ffprobe.available)) { $issues.Add([ordered]@{ code = 'FFMPEG_MISSING'; severity = if ($mediaRequired) { 'BLOCK' } else { 'WARN' }; status = if ($mediaRequired) { 'fail' } else { 'unknown' } }) }
if ($driveInfo.AvailableFreeSpace -lt 5GB) { $issues.Add([ordered]@{ code = 'LOW_DISK_SPACE'; severity = 'BLOCK'; status = 'fail' }) }

$mandatoryReady = $powerPoint.available -and ($driveInfo.AvailableFreeSpace -ge 5GB)
$mandatoryReady = $mandatoryReady -and $python.available -and $pythonProbe.available -and $pythonProbe.jsonschema
if ($authoringRequired) { $mandatoryReady = $mandatoryReady -and $node.available -and $artifactTool.available -and $runtimeBinReport.available }
if ($mediaRequired) { $mandatoryReady = $mandatoryReady -and $ffmpeg.available -and $ffprobe.available }
$profile = if ($nvidia.available) { 'GPU_CANDIDATE' } else { 'CPU_ONLY' }
$probeId = [guid]::NewGuid().ToString('N')
$ttlMinutes = 60
$ttlExpiresAt = (Get-Date).ToUniversalTime().AddMinutes($ttlMinutes).ToString('o')

$capabilityStatus = if ($mandatoryReady) { 'PASS' } else { 'UNVERIFIED' }

$capabilities = [ordered]@{
  powerpoint = [ordered]@{ available = [bool]$powerPoint.available; evidence = if ($powerPoint.available) { "COM probe version=$($powerPoint.version)" } else { 'COM unavailable' } }
  python = [ordered]@{ available = [bool]$python.available; evidence = if ($pythonProbe.available) { "version=$($pythonProbe.version) jsonschema=$($pythonProbe.jsonschema)" } else { 'python unavailable or probe failed' }; version = $pythonProbe.version; path = $python.path }
  node = [ordered]@{ available = [bool]$node.available; evidence = if ($node.available) { "path=$($node.path)" } else { 'node unavailable' }; path = $node.path }
  artifact_tool = [ordered]@{ available = [bool]$artifactTool.available; evidence = if ($artifactTool.available) { "importable path=$($artifactTool.path)" } else { [string]$artifactTool.error }; path = $artifactTool.path }
  jsonschema = [ordered]@{ available = [bool]$pythonProbe.jsonschema; evidence = if ($pythonProbe.jsonschema) { 'importlib.find_spec passed' } else { 'jsonschema import missing' } }
  ffmpeg = [ordered]@{ available = [bool]$ffmpeg.available; evidence = if ($ffmpeg.available) { "path=$($ffmpeg.path)" } else { 'ffmpeg unavailable' }; path = $ffmpeg.path }
  ffprobe = [ordered]@{ available = [bool]$ffprobe.available; evidence = if ($ffprobe.available) { "path=$($ffprobe.path)" } else { 'ffprobe unavailable' }; path = $ffprobe.path }
  tesseract = [ordered]@{ available = [bool]$tesseract.available; evidence = if ($tesseract.available) { "path=$($tesseract.path)" } else { 'tesseract unavailable' }; path = $tesseract.path }
}

$fingerprintParts = @(
  "ppt=$($powerPoint.version)",
  "py=$($pythonProbe.version)",
  "node=$(if($node.available){(& $node.path --version 2>$null) -replace '\r?\n',''}else{'none'})",
  "os=$([System.Runtime.InteropServices.RuntimeInformation]::OSDescription)"
)
$fingerprintString = $fingerprintParts -join ';'
$sha = [Security.Cryptography.SHA256]::Create()
try { $fingerprint = ([Convert]::ToHexString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($fingerprintString)))).ToLowerInvariant() }
finally { $sha.Dispose() }

$payload = [ordered]@{
  schema_version = '1.0'
  generated_at = (Get-Date).ToUniversalTime().ToString('o')
  status = $capabilityStatus
  probe_id = $probeId
  capabilities = $capabilities
  fingerprint = $fingerprint
  ttl_expires_at = $ttlExpiresAt
  target_path = $resolvedTarget
  mode = $Mode
  profile = $profile
  mandatory_ready = $mandatoryReady
  certification_ceiling = $capabilityStatus
  office = [ordered]@{ powerpoint = $powerPoint; word = $word; excel = $excel }
  runtimes = [ordered]@{ node = $node; node_modules = [ordered]@{ available = [bool]$runtimeModules; path = $runtimeModules }; bin_dir = $runtimeBinReport; python = $python; python_probe = $pythonProbe; artifact_tool = $artifactTool; ffmpeg = $ffmpeg; ffprobe = $ffprobe; tesseract = $tesseract }
  hardware = [ordered]@{ nvidia_smi = $nvidia; cuda_verified = $false; selected_asr_device = 'cpu'; selected_asr_compute_type = 'int8'; asr_selection_source = 'SAFE_DEFAULT_PENDING_RUNTIME_PROBE' }
  disk = [ordered]@{ root = $drive; free_bytes = [long]$driveInfo.AvailableFreeSpace; free_gb = [math]::Round($driveInfo.AvailableFreeSpace / 1GB, 2) }
  issues = @($issues)
}
Write-JsonFileNew -Value $payload -Path $resolvedOutput
$payload | ConvertTo-Json -Depth 20
if (-not $mandatoryReady) { exit 3 }
