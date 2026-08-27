param(
  [string]$CacheRoot,
  [string]$PythonPath,
  [switch]$ProbeOnly,
  [switch]$Force,
  [ValidateRange(0, 600)][int]$LockTimeoutSeconds = 30
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

if (-not $CacheRoot) { $CacheRoot = Get-DefaultCacheRoot }

function Resolve-PythonExecutable {
  param([string]$Requested)
  if ($Requested) {
    $candidate = (Resolve-Path -LiteralPath $Requested -ErrorAction Stop).Path
    return $candidate
  }
  $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
  if ($pyLauncher) {
    try {
      $candidate = & $pyLauncher.Source -3.11 -c "import sys; print(sys.executable)" 2>$null
      if ($LASTEXITCODE -eq 0 -and $candidate) { return ([string]$candidate).Trim() }
    } catch {}
  }
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) { return $python.Source }
  return $null
}

function Write-Receipt {
  param([object]$Value, [string]$Path)
  if ($Value -is [System.Collections.IDictionary] -and -not $Value.Contains('generated_at')) {
    $Value['generated_at'] = (Get-Date).ToUniversalTime().ToString('o')
  }
  Write-JsonFileMutable -Value $Value -Path $Path
  $Value | ConvertTo-Json -Depth 20
}

function Get-PlatformLockStatus {
  $platformIsWindows = $PSVersionTable.Platform -eq 'Win32NT' -or $env:OS -eq 'Windows_NT'
  $architecture = if ($env:PROCESSOR_ARCHITEW6432) { $env:PROCESSOR_ARCHITEW6432 } else { $env:PROCESSOR_ARCHITECTURE }
  $isAmd64 = $architecture -in @('AMD64', 'x86_64')
  return [ordered]@{ supported = $platformIsWindows -and [Environment]::Is64BitOperatingSystem -and $isAmd64; os = if ($platformIsWindows) { 'Windows' } else { [string]$PSVersionTable.OS }; architecture = $architecture; is_64_bit = [Environment]::Is64BitOperatingSystem }
}

function Assert-SafeCacheRoot {
  param([Parameter(Mandatory = $true)][string]$Path)
  $fullPath = [System.IO.Path]::GetFullPath($Path).TrimEnd('\', '/')
  $rootPath = [System.IO.Path]::GetPathRoot($fullPath).TrimEnd('\', '/')
  if (-not $fullPath -or $fullPath -eq $rootPath) { throw 'ASR_CACHE_ROOT_UNSAFE' }
  return $fullPath
}

function Assert-PathWithinCache {
  param(
    [Parameter(Mandatory = $true)][string]$CachePath,
    [Parameter(Mandatory = $true)][string]$CandidatePath
  )
  $cachePrefix = [System.IO.Path]::GetFullPath($CachePath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
  $candidate = [System.IO.Path]::GetFullPath($CandidatePath)
  if (-not $candidate.StartsWith($cachePrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "ASR_PATH_ESCAPES_CACHE:$candidate"
  }
  Assert-NoReparseAncestors -Path $CachePath
  Assert-NoReparseAncestors -Path $candidate
  return $candidate
}

function Get-AsrMutexName {
  param([Parameter(Mandatory = $true)][string]$Path)
  $normalized = [System.IO.Path]::GetFullPath($Path).TrimEnd('\', '/').ToLowerInvariant()
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($normalized)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    $hash = [System.Convert]::ToHexString($sha.ComputeHash($bytes)).ToLowerInvariant()
  } finally {
    $sha.Dispose()
  }
  return "Local\MakeSlidePro-ASR-$hash"
}

function Release-AsrMutex {
  param([object]$Mutex, [bool]$Acquired)
  if ($Mutex) {
    if ($Acquired) { try { $Mutex.ReleaseMutex() } catch {} }
    $Mutex.Dispose()
  }
}

$cache = Assert-SafeCacheRoot -Path $CacheRoot
$mutex = $null
$mutexAcquired = $false
$mutexName = Get-AsrMutexName -Path $cache
try {
  $mutex = [System.Threading.Mutex]::new($false, $mutexName)
  try {
    $mutexAcquired = $mutex.WaitOne([TimeSpan]::FromSeconds($LockTimeoutSeconds))
  } catch [System.Threading.AbandonedMutexException] {
    $mutexAcquired = $true
  }
} catch {
  $busyReceipt = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); status = 'UNVERIFIED'; reason = 'ASR_MUTEX_UNAVAILABLE'; cache_root = $cache; mutex = $mutexName; error = $_.Exception.Message }
  $busyReceipt | ConvertTo-Json -Depth 20
  exit 3
}
if (-not $mutexAcquired) {
  $busyReceipt = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); status = 'UNVERIFIED'; reason = 'ASR_INSTALL_BUSY'; cache_root = $cache; mutex = $mutexName; lock_timeout_seconds = $LockTimeoutSeconds }
  $busyReceipt | ConvertTo-Json -Depth 20
  Release-AsrMutex -Mutex $mutex -Acquired $false
  exit 3
}
$asrDirectory = $null
$venv = $null
$receiptPath = $null
$probePath = $null
try {
  Assert-NoReparseAncestors -Path $cache
  [System.IO.Directory]::CreateDirectory($cache) | Out-Null
  Assert-NoReparseAncestors -Path $cache
  $asrDirectory = Assert-PathWithinCache -CachePath $cache -CandidatePath (Join-Path $cache 'asr')
  if (Test-Path -LiteralPath $asrDirectory) {
    $asrDirectoryItem = Get-Item -LiteralPath $asrDirectory -Force -ErrorAction Stop
    if (-not $asrDirectoryItem.PSIsContainer) { throw 'ASR_DIRECTORY_IS_NOT_DIRECTORY' }
    if (($asrDirectoryItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'ASR_DIRECTORY_REPARSE_POINT_NOT_ALLOWED' }
  } else {
    [System.IO.Directory]::CreateDirectory($asrDirectory) | Out-Null
  }
  Assert-NoReparseAncestors -Path $asrDirectory
  $venv = Assert-PathWithinCache -CachePath $cache -CandidatePath (Join-Path $asrDirectory 'venv')
  $receiptPath = Join-Path $asrDirectory 'install-receipt.json'
  $probePath = Join-Path $asrDirectory 'capability-report.json'
} catch {
  $pathFailure = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = 'BLOCKED'
    reason = 'ASR_CACHE_PATH_UNSAFE'
    cache_root = $cache
    error = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  }
  $pathFailure | ConvertTo-Json -Depth 20
  [Console]::Error.WriteLine($pathFailure.error)
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 2
}
$lockPath = Join-Path $PSScriptRoot '..\assets\asr\requirements-asr.lock'
$python = Resolve-PythonExecutable -Requested $PythonPath
$pythonVersion = $null
if ($python) {
  try { $pythonVersion = (& $python -c "import sys; print(sys.version.split()[0])" 2>$null).Trim() } catch {}
}
$platformLock = Get-PlatformLockStatus

if (-not $python) {
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = 'PYTHON_NOT_FOUND'; cache_root = $cache }
  Write-Receipt -Value $receipt -Path $receiptPath
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 3
}

if (-not $platformLock.supported) {
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = 'PLATFORM_LOCK_IS_CP311_WINDOWS_AMD64'; python = $python; python_version = $pythonVersion; cache_root = $cache; lock = $lockPath; platform = $platformLock }
  Write-Receipt -Value $receipt -Path $receiptPath
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 3
}

$venvPython = Join-Path $venv 'Scripts\python.exe'
$existingRuntimeProbeFailed = $false
if ((Test-Path -LiteralPath $venvPython) -and -not $Force) {
  try {
    & $venvPython $PSScriptRoot\probe-asr-runtime.py --output $probePath
    $probeExit = $LASTEXITCODE
  } catch {
    $probeExit = 3
  }
  if ($probeExit -eq 0) {
    $receipt = [ordered]@{ schema_version = '1.0'; status = 'PASS'; python = $venvPython; python_version = $pythonVersion; cache_root = $cache; probe = $probePath; reused = $true; rollback_restored = $false }
    Write-Receipt -Value $receipt -Path $receiptPath
    Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
    exit 0
  }
  $existingRuntimeProbeFailed = $true
  if ($ProbeOnly) {
    $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = 'ASR_EXISTING_RUNTIME_PROBE_FAILED'; python = $venvPython; python_version = $pythonVersion; cache_root = $cache; probe = $probePath; reused = $true; rollback_restored = $false }
    Write-Receipt -Value $receipt -Path $receiptPath
    Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
    exit 3
  }
}

if ($ProbeOnly) {
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = 'ASR_RUNTIME_NOT_INSTALLED'; python = $python; python_version = $pythonVersion; cache_root = $cache; lock = $lockPath }
  Write-Receipt -Value $receipt -Path $receiptPath
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 3
}

if (-not (Test-Path -LiteralPath $lockPath -PathType Leaf)) { throw "ASR lock not found: $lockPath" }
if ($pythonVersion -notlike '3.11.*') {
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = 'PYTHON_VERSION_NOT_SUPPORTED'; python = $python; python_version = $pythonVersion; lock = $lockPath; platform = $platformLock }
  Write-Receipt -Value $receipt -Path $receiptPath
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 3
}

$staging = Assert-PathWithinCache -CachePath $cache -CandidatePath (Join-Path $cache ("asr\venv.staging-" + [guid]::NewGuid().ToString('N')))
$logPath = Join-Path $cache 'asr\install.log'
$stagingPython = Join-Path $staging 'Scripts\python.exe'
$backup = $null
$publishedNewRuntime = $false
try {
  & $python -m venv $staging 2>&1 | Tee-Object -FilePath $logPath
  if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $stagingPython)) { throw 'VIRTUALENV_CREATE_FAILED' }
  & $stagingPython -m pip install --disable-pip-version-check --no-input --require-hashes --only-binary=:all: --index-url https://pypi.org/simple -r $lockPath 2>&1 | Tee-Object -FilePath $logPath -Append
  if ($LASTEXITCODE -ne 0) { throw 'ASR_PACKAGE_INSTALL_FAILED' }
  & $stagingPython -m pip check 2>&1 | Tee-Object -FilePath $logPath -Append
  if ($LASTEXITCODE -ne 0) { throw 'ASR_PIP_CHECK_FAILED' }
  & $stagingPython -c "from faster_whisper import WhisperModel; import ctranslate2, av; print('smoke-ok')" 2>&1 | Tee-Object -FilePath $logPath -Append
  if ($LASTEXITCODE -ne 0) { throw 'ASR_IMPORT_SMOKE_FAILED' }
  if (Test-Path -LiteralPath $venv) {
    $backup = Assert-PathWithinCache -CachePath $cache -CandidatePath (Join-Path $cache ("asr\venv.previous-" + (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 8)))
    Move-Item -LiteralPath $venv -Destination $backup
  }
  Move-Item -LiteralPath $staging -Destination $venv
  $publishedNewRuntime = $true
  try {
    & $venvPython $PSScriptRoot\probe-asr-runtime.py --output $probePath
    $probeExit = $LASTEXITCODE
  } catch {
    $probeExit = 3
  }
  if ($probeExit -ne 0) { throw 'ASR_POST_INSTALL_PROBE_FAILED' }
  $freeze = @(& $venvPython -m pip freeze 2>$null)
  $backupCleanupPending = [bool]($backup -and (Test-Path -LiteralPath $backup))
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'PASS'; python = $venvPython; python_version = $pythonVersion; cache_root = $cache; lock = $lockPath; install_log = $logPath; probe = $probePath; reused = $false; refreshed_after_failed_probe = $existingRuntimeProbeFailed; rollback_restored = $false; backup_cleanup_pending = $backupCleanupPending; backup_cleanup_status = if ($backupCleanupPending) { 'PENDING' } else { 'NOT_REQUIRED' }; packages = $freeze }
  Write-Receipt -Value $receipt -Path $receiptPath
  $publishedNewRuntime = $false
  if ($backup -and (Test-Path -LiteralPath $backup)) {
    try {
      [void](Assert-PathWithinCache -CachePath $cache -CandidatePath $backup)
      Remove-Item -LiteralPath $backup -Recurse -Force
      $backup = $null
      $receipt['backup_cleanup_pending'] = $false
      $receipt['backup_cleanup_status'] = 'REMOVED'
    } catch {
      $receipt['backup_cleanup_pending'] = $true
      $receipt['backup_cleanup_status'] = 'RETAINED'
      $receipt['backup_cleanup_error'] = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
    }
    try { Write-JsonFileMutable -Value $receipt -Path $receiptPath } catch {}
  }
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 0
} catch {
  $failureReason = $_.Exception.Message
  $rollbackRestored = $false
  $rollbackErrors = [System.Collections.Generic.List[string]]::new()
  if (Test-Path -LiteralPath $staging) {
    try {
      [void](Assert-PathWithinCache -CachePath $cache -CandidatePath $staging)
      Remove-Item -LiteralPath $staging -Recurse -Force
    } catch {
      $rollbackErrors.Add("STAGING_REMOVE_FAILED:$($_.Exception.Message)")
    }
  }
  if ($publishedNewRuntime -and (Test-Path -LiteralPath $venv)) {
    try {
      [void](Assert-PathWithinCache -CachePath $cache -CandidatePath $venv)
      Remove-Item -LiteralPath $venv -Recurse -Force
    } catch {
      $rollbackErrors.Add("PUBLISHED_RUNTIME_REMOVE_FAILED:$($_.Exception.Message)")
    }
  }
  if ($backup -and (Test-Path -LiteralPath $backup) -and -not (Test-Path -LiteralPath $venv)) {
    try {
      [void](Assert-PathWithinCache -CachePath $cache -CandidatePath $backup)
      [void](Assert-PathWithinCache -CachePath $cache -CandidatePath $venv)
      Move-Item -LiteralPath $backup -Destination $venv
      $rollbackRestored = $true
    } catch {
      $rollbackErrors.Add("BACKUP_RESTORE_FAILED:$($_.Exception.Message)")
    }
  }
  $receipt = [ordered]@{ schema_version = '1.0'; status = 'UNVERIFIED'; reason = $failureReason; python = $python; python_version = $pythonVersion; cache_root = $cache; lock = $lockPath; install_log = $logPath; refreshed_after_failed_probe = $existingRuntimeProbeFailed; rollback_restored = $rollbackRestored; rollback_errors = @($rollbackErrors) }
  Write-Receipt -Value $receipt -Path $receiptPath
  [Console]::Error.WriteLine(($failureReason -replace '[\r\n]+', ' ').Trim())
  Release-AsrMutex -Mutex $mutex -Acquired $mutexAcquired
  exit 3
}
