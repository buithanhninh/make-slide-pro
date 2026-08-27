param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [Parameter(Mandatory = $true)][string]$JobContractPath,
  [Parameter(Mandatory = $true)][string]$Workspace,
  [ValidateSet('auto', 'audit', 'repair', 'redesign', 'rebuild', 'create', 'update_data', 'extend', 'merge', 'localize', 'motion', 'certify')]
  [string]$RequestedOperation = 'auto',
  [switch]$SkipPreflight
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

function Assert-InputPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  $resolved = Get-NormalizedFullPath -Path $Path
  if (-not (Test-Path -LiteralPath $resolved)) { throw "INPUT_NOT_FOUND:$resolved" }
  $item = Get-Item -LiteralPath $resolved -Force -ErrorAction Stop
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "INPUT_REPARSE_POINT_NOT_ALLOWED:$resolved" }
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolved))
  return $resolved
}

function Assert-JobContractPath {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$InputPath
  )
  $resolved = Assert-RegularFilePath -Path $Path -Label 'JOB_CONTRACT'
  if (Test-PathsEqual -FirstPath $resolved -SecondPath $InputPath) { throw 'JOB_CONTRACT_PATH_COLLISION_WITH_INPUT' }
  if ((Test-Path -LiteralPath $InputPath -PathType Container) -and (Test-PathInsideDirectory -Path $resolved -Directory $InputPath)) {
    throw 'JOB_CONTRACT_CANNOT_BE_INSIDE_INPUT_DIRECTORY'
  }
  return $resolved
}

function Get-PythonCommand {
  if ($env:RUNTIME_PYTHON) {
    $runtimePython = Get-NormalizedFullPath -Path $env:RUNTIME_PYTHON
    $runtimePython = Assert-RegularFilePath -Path $runtimePython -Label 'RUNTIME_PYTHON'
    $runtimeCommand = Get-Command -Name $runtimePython -CommandType Application -ErrorAction SilentlyContinue
    if (-not $runtimeCommand) { throw "RUNTIME_PYTHON_NOT_APPLICATION:$runtimePython" }
    $runtimeSource = Assert-RegularFilePath -Path $runtimeCommand.Source -Label 'RUNTIME_PYTHON_APPLICATION'
    if (-not (Test-PathsEqual -FirstPath $runtimeSource -SecondPath $runtimePython)) { throw "RUNTIME_PYTHON_RESOLUTION_MISMATCH:$runtimePython" }
    return $runtimeSource
  }
  foreach ($command in @(Get-Command python -CommandType Application -All -ErrorAction SilentlyContinue)) {
    try {
      $source = Assert-RegularFilePath -Path $command.Source -Label 'PYTHON_APPLICATION'
      return $source
    } catch {}
  }
  return $null
}

function Assert-WorkspacePath {
  param([Parameter(Mandatory = $true)][string]$Path, [string]$InputPath)
  $resolved = Get-NormalizedFullPath -Path $Path
  if (Test-PathsEqual -FirstPath $resolved -SecondPath $InputPath) { throw 'WORKSPACE_PATH_COLLISION_WITH_INPUT' }
  if ((Test-Path -LiteralPath $InputPath -PathType Container) -and (Test-PathInsideDirectory -Path $resolved -Directory $InputPath)) { throw 'WORKSPACE_CANNOT_BE_INSIDE_INPUT_DIRECTORY' }
  $parent = [System.IO.Path]::GetDirectoryName($resolved)
  Assert-NoReparseAncestors -Path $parent
  if (Test-Path -LiteralPath $resolved) {
    throw "WORKSPACE_ALREADY_EXISTS:$resolved"
  }
  [System.IO.Directory]::CreateDirectory($parent) | Out-Null
  $staging = Join-Path $parent ('.' + [System.IO.Path]::GetFileName($resolved) + '.tmp-' + [guid]::NewGuid().ToString('N'))
  try {
    [System.IO.Directory]::CreateDirectory($staging) | Out-Null
    $stagingItem = Get-Item -LiteralPath $staging -Force -ErrorAction Stop
    if (($stagingItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "WORKSPACE_STAGING_REPARSE_POINT_NOT_ALLOWED:$staging" }
    [System.IO.Directory]::Move($staging, $resolved)
  } finally {
    if (Test-Path -LiteralPath $staging -PathType Container) { try { [System.IO.Directory]::Delete($staging, $false) } catch {} }
  }
  return $resolved
}

function Get-CurrentSourceHashes {
  param([object[]]$Sources)
  $seenIds = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  $seenPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  $result = [System.Collections.Generic.List[object]]::new()
  foreach ($source in @($Sources)) {
    if ($null -eq $source) { throw 'SOURCE_RECORD_NULL' }
    $sourceId = [string]$source.source_id
    $path = [string]$source.path
    if ([string]::IsNullOrWhiteSpace($sourceId) -or [string]::IsNullOrWhiteSpace($path)) { throw 'SOURCE_RECORD_BINDING_INVALID' }
    if (-not $seenIds.Add($sourceId)) { throw "DUPLICATE_SOURCE_ID:$sourceId" }
    $resolvedPath = Assert-RegularFilePath -Path $path -Label "SOURCE_$sourceId"
    if (-not $seenPaths.Add($resolvedPath)) { throw "DUPLICATE_SOURCE_PATH:$resolvedPath" }
    $actualHash = (Get-FileHash -LiteralPath $resolvedPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $inventoryHash = [string](Get-StrictPropertyValue -Object $source -Name 'sha256')
    if ($inventoryHash -notmatch '^[0-9a-fA-F]{64}$') { throw "SOURCE_INVENTORY_HASH_INVALID:$sourceId" }
    if ($inventoryHash.ToLowerInvariant() -ne $actualHash) { throw "SOURCE_INVENTORY_HASH_MISMATCH:$sourceId" }
    $result.Add([ordered]@{ source_id = $sourceId; path = $resolvedPath; sha256 = $actualHash })
  }
  return @($result)
}

function Assert-JobContractUnchanged {
  param([Parameter(Mandatory = $true)][string]$Stage)
  $recheckedPath = Assert-RegularFilePath -Path $resolvedJobContract -Label "JOB_CONTRACT_RECHECK_$Stage"
  if (-not (Test-PathsEqual -FirstPath $recheckedPath -SecondPath $resolvedJobContract)) { throw "JOB_CONTRACT_PATH_CHANGED_AFTER_STAGE:$Stage" }
  $currentHash = (Get-FileHash -LiteralPath $recheckedPath -Algorithm SHA256).Hash.ToLowerInvariant()
  $run.job_contract_hash_after = $currentHash
  $run.job_contract_hash_unchanged = $currentHash -eq $run.job_contract_hash_before
  $run.job_contract_hash_checkpoints.Add([ordered]@{
    stage = $Stage
    captured_at = (Get-Date).ToUniversalTime().ToString('o')
    sha256 = $currentHash
  })
  if (-not $run.job_contract_hash_unchanged) { throw "JOB_CONTRACT_CHANGED_AFTER_STAGE:$Stage" }
  return $currentHash
}

function Get-SourceSnapshotHash {
  param([Parameter(Mandatory = $true)][object[]]$Sources)
  if ($Sources.Count -eq 1) { return [string]$Sources[0].sha256.ToLowerInvariant() }
  $records = [System.Collections.Generic.List[string]]::new()
  foreach ($source in $Sources) {
    $normalizedPath = (Get-NormalizedFullPath -Path ([string]$source.path)).ToLowerInvariant()
    $records.Add(([string]$source.source_id + [char]0x1F + $normalizedPath + [char]0x1F + ([string]$source.sha256).ToLowerInvariant()))
  }
  $canonical = [string]::Join("`n", @($records | Sort-Object -CaseSensitive))
  $sha = [Security.Cryptography.SHA256]::Create()
  try {
    return ([Convert]::ToHexString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($canonical)))).ToLowerInvariant()
  } finally {
    $sha.Dispose()
  }
}

function Test-SourceSnapshotsEqual {
  param([object[]]$Expected, [object[]]$Actual)
  if (@($Expected).Count -ne @($Actual).Count) { return $false }
  $actualById = @{}
  foreach ($item in @($Actual)) { $actualById[[string]$item.source_id] = $item }
  foreach ($item in @($Expected)) {
    $id = [string]$item.source_id
    if (-not $actualById.ContainsKey($id)) { return $false }
    $actualItem = $actualById[$id]
    if (-not (Test-PathsEqual -FirstPath ([string]$item.path) -SecondPath ([string]$actualItem.path))) { return $false }
    if ([string]$item.sha256 -ine [string]$actualItem.sha256) { return $false }
  }
  return $true
}

function Assert-SourcesUnchanged {
  param([string]$Stage)
  $current = Get-CurrentSourceHashes -Sources @($inventory.sources)
  $run.source_hash_checkpoints.Add([ordered]@{ stage = $Stage; captured_at = (Get-Date).ToUniversalTime().ToString('o'); sources = @($current) })
  if (-not (Test-SourceSnapshotsEqual -Expected @($run.source_hashes_before) -Actual @($current))) { throw "SOURCE_CHANGED_AFTER_STAGE:$Stage" }
  return $current
}

function Assert-GateArtifact {
  param([string]$Path, [string]$ExpectedStatus, [int]$ExitCode, [string]$Gate)
  $resolved = Assert-RegularFilePath -Path $Path -Label "${Gate}_ARTIFACT"
  $payload = Read-JsonFile -Path $resolved
  if ($null -eq $payload -or $payload -is [System.Array] -or $payload -is [string] -or $payload -is [ValueType]) { throw "${Gate}_ARTIFACT_MUST_BE_OBJECT" }
  $actualStatus = [string]$payload.status
  if ($actualStatus -ne $ExpectedStatus) { throw "${Gate}_STATUS_MISMATCH:exit=$ExitCode;artifact=$actualStatus;expected=$ExpectedStatus" }
  return $resolved
}

function Assert-RoutingPayload {
  param([object]$Route, [int]$ExpectedSourceCount, [object]$JobContract)
  if ($null -eq $Route -or $Route -is [System.Array] -or $Route -is [string] -or $Route -is [ValueType]) { throw 'ROUTE_PAYLOAD_MUST_BE_OBJECT' }
  foreach ($name in @('schema_version', 'status', 'input_class', 'maturity', 'primary_operation', 'modifiers', 'preservation_mode', 'visual_route', 'required_adapters', 'certification_mode', 'job_contract_path', 'job_contract_sha256', 'source_count', 'blocking_reasons', 'unverified_reasons')) {
    if ($null -eq $Route.PSObject.Properties[$name]) { throw "ROUTE_PROPERTY_MISSING:$name" }
  }
  if ([string]$Route.schema_version -ne '1.0') { throw 'ROUTE_SCHEMA_VERSION_INVALID' }
  if ([string]$Route.status -notin @('PASS', 'UNVERIFIED', 'BLOCKED')) { throw 'ROUTE_STATUS_INVALID' }
  if ([int]$Route.source_count -ne $ExpectedSourceCount) { throw 'ROUTE_SOURCE_COUNT_MISMATCH' }
  if (-not (Test-PathsEqual -FirstPath ([string]$Route.job_contract_path) -SecondPath $resolvedJobContract)) { throw 'ROUTE_JOB_CONTRACT_PATH_MISMATCH' }
  if ([string]$Route.job_contract_sha256 -ine [string]$run.job_contract_hash_before) { throw 'ROUTE_JOB_CONTRACT_HASH_MISMATCH' }
  if ([string]$Route.primary_operation -ne [string]$JobContract.primary_operation) { throw 'ROUTE_JOB_CONTRACT_OPERATION_MISMATCH' }
  if ([string]$Route.preservation_mode -ne [string]$JobContract.preservation_mode) { throw 'ROUTE_JOB_CONTRACT_PRESERVATION_MISMATCH' }
  if ([string]$Route.certification_mode -ne [string]$JobContract.certification_mode) { throw 'ROUTE_JOB_CONTRACT_CERTIFICATION_MISMATCH' }
  if ($Route.modifiers -isnot [System.Array] -or $Route.required_adapters -isnot [System.Array] -or $Route.blocking_reasons -isnot [System.Array] -or $Route.unverified_reasons -isnot [System.Array]) { throw 'ROUTE_COLLECTION_INVALID' }
  $contractModifiers = @($JobContract.modifiers)
  $routeModifiers = @($Route.modifiers)
  if ($routeModifiers.Count -ne $contractModifiers.Count) { throw 'ROUTE_JOB_CONTRACT_MODIFIERS_MISMATCH' }
  for ($index = 0; $index -lt $contractModifiers.Count; $index++) {
    if ([string]$routeModifiers[$index] -cne [string]$contractModifiers[$index]) { throw 'ROUTE_JOB_CONTRACT_MODIFIERS_MISMATCH' }
  }
  $operations = @('AUDIT', 'REPAIR', 'REDESIGN', 'REBUILD', 'CREATE', 'UPDATE_DATA', 'EXTEND', 'MERGE', 'LOCALIZE', 'MOTION', 'CERTIFY')
  if ([string]$Route.primary_operation -notin $operations) { throw 'ROUTE_OPERATION_INVALID' }
  $adapterKeys = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  foreach ($adapter in @($Route.required_adapters)) {
    if ($null -eq $adapter -or $adapter -is [string] -or $adapter -is [ValueType] -or $null -eq $adapter.PSObject.Properties['format'] -or $null -eq $adapter.PSObject.Properties['adapter']) { throw 'ROUTE_ADAPTER_RECORD_INVALID' }
    if (-not $adapterKeys.Add([string]$adapter.format)) { throw "ROUTE_DUPLICATE_ADAPTER:$($adapter.format)" }
    if ([string]$adapter.adapter -notin @('POWERPOINT', 'DOCUMENT', 'PDF', 'DATA', 'AUDIO', 'VIDEO', 'IMAGE', 'ARCHIVE', 'UNKNOWN')) { throw 'ROUTE_ADAPTER_INVALID' }
  }
}

function Add-GateReceipt {
  param([string]$Gate, [string]$Status, [int]$ExitCode, [string]$ArtifactPath, [string]$StartedAt, [string]$Reason)
  $artifactHash = $null
  if (Test-Path -LiteralPath $ArtifactPath -PathType Leaf) {
    $artifactItem = Get-Item -LiteralPath $ArtifactPath -Force -ErrorAction Stop
    if (($artifactItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) { $artifactHash = (Get-FileHash -LiteralPath $ArtifactPath -Algorithm SHA256).Hash.ToLowerInvariant() }
  }
  $receipt = [ordered]@{ gate = $Gate; status = $Status; exit_code = $ExitCode; artifact_path = $ArtifactPath; artifact_sha256 = $artifactHash; started_at = $StartedAt; completed_at = (Get-Date).ToUniversalTime().ToString('o') }
  if (-not [string]::IsNullOrWhiteSpace($Reason)) { $receipt.reason = $Reason }
  $run.gates.Add($receipt)
}

function Add-ValidatedGateReceipt {
  param(
    [string]$Gate,
    [string]$Status,
    [int]$ExitCode,
    [string]$ArtifactPath,
    [string]$StartedAt,
    [switch]$RequireArtifact
  )
  try {
    if (Test-Path -LiteralPath $ArtifactPath -PathType Leaf) {
      [void](Assert-GateArtifact -Path $ArtifactPath -ExpectedStatus $Status -ExitCode $ExitCode -Gate $Gate)
    } elseif ($RequireArtifact -or $ExitCode -eq 0) {
      throw "${Gate}_ARTIFACT_MISSING"
    }
  } catch {
    $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
    Add-GateReceipt -Gate $Gate -Status 'BLOCKED' -ExitCode 2 -ArtifactPath $ArtifactPath -StartedAt $StartedAt -Reason "ARTIFACT_VALIDATION_FAILED:$message"
    throw
  }
  Add-GateReceipt -Gate $Gate -Status $Status -ExitCode $ExitCode -ArtifactPath $ArtifactPath -StartedAt $StartedAt
}

function Invoke-JsonSchemaGate {
  param(
    [Parameter(Mandatory = $true)][string]$InputPath,
    [Parameter(Mandatory = $true)][string]$Schema,
    [Parameter(Mandatory = $true)][string]$ReportPath,
    [Parameter(Mandatory = $true)][string]$StdoutPath,
    [Parameter(Mandatory = $true)][string]$Gate
  )
  $startedAt = (Get-Date).ToUniversalTime().ToString('o')
  $stdout = @(& $python (Join-Path $PSScriptRoot 'validate-json.py') --input $InputPath --schema $Schema --output $ReportPath)
  $exitCode = $LASTEXITCODE
  Write-TextFileNew -Text ((@($stdout | ForEach-Object { [string]$_ })) -join [Environment]::NewLine) -Path $StdoutPath
  $status = if ($exitCode -eq 0) { 'PASS' } elseif ($exitCode -eq 3) { 'UNVERIFIED' } else { 'BLOCKED' }
  Add-ValidatedGateReceipt -Gate $Gate -Status $status -ExitCode $exitCode -ArtifactPath $ReportPath -StartedAt $startedAt
  return [pscustomobject]@{ status = $status; exit_code = $exitCode }
}

function Complete-Run {
  param([string]$State, [int]$ExitCode)
  $run.state = $State
  $run.completed_at = (Get-Date).ToUniversalTime().ToString('o')
  Write-JsonFileMutable -Value $run -Path (Join-Path $resolvedWorkspace 'run-manifest.json')
  $run | ConvertTo-Json -Depth 30
  exit $ExitCode
}

$resolvedInput = $null
$resolvedJobContract = $null
$resolvedWorkspace = $null
$run = $null
$inventory = $null
$jobContract = $null
try {
  $resolvedInput = Assert-InputPath -Path $InputPath
  $resolvedJobContract = Assert-JobContractPath -Path $JobContractPath -InputPath $resolvedInput
  $jobContractHashBefore = (Get-FileHash -LiteralPath $resolvedJobContract -Algorithm SHA256).Hash.ToLowerInvariant()
  $resolvedWorkspace = Assert-WorkspacePath -Path $Workspace -InputPath $resolvedInput
  $run = [ordered]@{
    run_id = [guid]::NewGuid().ToString('N')
    started_at = (Get-Date).ToUniversalTime().ToString('o')
    input_path = $resolvedInput
    job_contract_path = $resolvedJobContract
    job_contract_hash_before = $jobContractHashBefore
    job_contract_hash_after = $null
    job_contract_hash_unchanged = $false
    job_contract_hash_checkpoints = [System.Collections.Generic.List[object]]::new()
    workspace = $resolvedWorkspace
    requested_operation = $RequestedOperation
    pipeline_scope = 'INTAKE_BOOTSTRAP_ONLY'
    terminal_gate = 'G2_ROUTING_DECISION'
    next_gate = 'G3_FORMAT_ADAPTERS'
    release_certified = $false
    preflight_skipped = [bool]$SkipPreflight
    source_hash_formula = 'SOURCE_FILE_SHA256_OR_SET_V1'
    state = 'STARTED'
    source_hash_before = $null
    source_hash_after = $null
    source_hashes_before = @()
    source_hashes_after = @()
    source_hash_unchanged = $false
    source_hash_checkpoints = [System.Collections.Generic.List[object]]::new()
    inventory_hash_before_routing = $null
    inventory_hash_after_routing = $null
    inventory_hash_unchanged = $false
    routing_hash_before_validation = $null
    routing_hash_after_validation = $null
    routing_hash_unchanged = $false
    gates = [System.Collections.Generic.List[object]]::new()
  }
  Write-JsonFileNew -Value $run -Path (Join-Path $resolvedWorkspace 'run-manifest.json')
  $pwsh = (Get-Command pwsh -ErrorAction Stop).Source

  $jobContractValidationPath = Join-Path $resolvedWorkspace 'job-contract-validation.json'
  $jobContractStdoutPath = Join-Path $resolvedWorkspace 'job-contract.stdout.txt'
  $startedAt = (Get-Date).ToUniversalTime().ToString('o')
  $python = Get-PythonCommand
  if (-not $python) {
    Write-TextFileNew -Text 'PYTHON_RUNTIME_UNAVAILABLE' -Path $jobContractStdoutPath
    $timestamp = (Get-Date).ToUniversalTime().ToString('o')
    $run.gates.Add([ordered]@{
      gate = 'G0_JOB_CONTRACT'
      status = 'UNVERIFIED'
      exit_code = 3
      artifact_path = $null
      artifact_sha256 = $null
      started_at = $startedAt
      completed_at = $timestamp
      reason = 'PYTHON_RUNTIME_UNAVAILABLE'
    })
    [void](Assert-JobContractUnchanged -Stage 'G0_JOB_CONTRACT')
    Complete-Run -State 'UNVERIFIED' -ExitCode 3
  }
  $stdout = @(& $python (Join-Path $PSScriptRoot 'validate-job-contract.py') --input $resolvedJobContract --output $jobContractValidationPath)
  $exitCode = $LASTEXITCODE
  Write-TextFileNew -Text ((@($stdout | ForEach-Object { [string]$_ })) -join [Environment]::NewLine) -Path $jobContractStdoutPath
  $status = if ($exitCode -eq 0) { 'PASS' } elseif ($exitCode -eq 3) { 'UNVERIFIED' } else { 'BLOCKED' }
  Add-ValidatedGateReceipt -Gate 'G0_JOB_CONTRACT' -Status $status -ExitCode $exitCode -ArtifactPath $jobContractValidationPath -StartedAt $startedAt
  [void](Assert-JobContractUnchanged -Stage 'G0_JOB_CONTRACT')
  if ($exitCode -eq 3) { Complete-Run -State 'UNVERIFIED' -ExitCode 3 }
  if ($exitCode -ne 0) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  $jobContract = Read-JsonFile -Path $resolvedJobContract
  $contractOperation = [string](Get-StrictPropertyValue -Object $jobContract -Name 'primary_operation')
  if ($RequestedOperation -ne 'auto' -and $RequestedOperation.ToUpperInvariant() -ne $contractOperation) {
    throw "REQUESTED_OPERATION_JOB_CONTRACT_MISMATCH:requested=$($RequestedOperation.ToUpperInvariant());contract=$contractOperation"
  }
  $run.effective_operation = $contractOperation

  if ($SkipPreflight) {
    $timestamp = (Get-Date).ToUniversalTime().ToString('o')
    $run.gates.Add([ordered]@{
      gate = 'G1_CAPABILITY'
      status = 'UNVERIFIED'
      exit_code = 3
      artifact_path = $null
      artifact_sha256 = $null
      started_at = $timestamp
      completed_at = $timestamp
      reason = 'PREFLIGHT_SKIPPED'
    })
    [void](Assert-JobContractUnchanged -Stage 'G1_CAPABILITY')
  } else {
    $artifactPath = Join-Path $resolvedWorkspace 'capability-report.json'
    $stdoutPath = Join-Path $resolvedWorkspace 'preflight.stdout.txt'
    $startedAt = (Get-Date).ToUniversalTime().ToString('o')
    $stdout = @(& $pwsh -NoLogo -NoProfile -File (Join-Path $PSScriptRoot 'preflight.ps1') -OutputPath $artifactPath -TargetPath $resolvedWorkspace)
    $exitCode = $LASTEXITCODE
    Write-TextFileNew -Text ((@($stdout | ForEach-Object { [string]$_ })) -join [Environment]::NewLine) -Path $stdoutPath
    $status = if ($exitCode -eq 0) { 'PASS' } elseif ($exitCode -eq 3) { 'UNVERIFIED' } else { 'BLOCKED' }
    Add-ValidatedGateReceipt -Gate 'G1_CAPABILITY' -Status $status -ExitCode $exitCode -ArtifactPath $artifactPath -StartedAt $startedAt
    [void](Assert-JobContractUnchanged -Stage 'G1_CAPABILITY')
    if ($exitCode -eq 3) { Complete-Run -State 'UNVERIFIED' -ExitCode 3 }
    if ($exitCode -ne 0) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  }

  $inventoryPath = Join-Path $resolvedWorkspace 'source-inventory.json'
  $startedAt = (Get-Date).ToUniversalTime().ToString('o')
  $inventoryStdoutPath = Join-Path $resolvedWorkspace 'inventory.stdout.txt'
  $stdout = @(& $pwsh -NoLogo -NoProfile -File (Join-Path $PSScriptRoot 'inventory-inputs.ps1') -InputPath $resolvedInput -OutputPath $inventoryPath)
  $exitCode = $LASTEXITCODE
  Write-TextFileNew -Text ((@($stdout | ForEach-Object { [string]$_ })) -join [Environment]::NewLine) -Path $inventoryStdoutPath
  $status = if ($exitCode -eq 0) { 'PASS' } elseif ($exitCode -eq 3) { 'UNVERIFIED' } else { 'BLOCKED' }
  Add-ValidatedGateReceipt -Gate 'G2_SOURCE_INVENTORY' -Status $status -ExitCode $exitCode -ArtifactPath $inventoryPath -StartedAt $startedAt
  if (Test-Path -LiteralPath $inventoryPath -PathType Leaf) {
    $inventorySchemaGate = Invoke-JsonSchemaGate -InputPath $inventoryPath -Schema 'source-manifest' -ReportPath (Join-Path $resolvedWorkspace 'source-inventory.validation.json') -StdoutPath (Join-Path $resolvedWorkspace 'source-inventory.validation.stdout.txt') -Gate 'G2_SOURCE_INVENTORY_SCHEMA'
    if ($inventorySchemaGate.exit_code -eq 3) { Complete-Run -State 'UNVERIFIED' -ExitCode 3 }
    if ($inventorySchemaGate.exit_code -ne 0) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  }
  [void](Assert-JobContractUnchanged -Stage 'G2_SOURCE_INVENTORY')
  if ($exitCode -ne 0) { Complete-Run -State $status -ExitCode $(if ($exitCode -eq 3) { 3 } else { 2 }) }

  $inventoryPath = Assert-RegularFilePath -Path $inventoryPath -Label 'SOURCE_INVENTORY_RECHECK'
  $run.inventory_hash_before_routing = (Get-FileHash -LiteralPath $inventoryPath -Algorithm SHA256).Hash.ToLowerInvariant()
  $inventory = Read-JsonFile -Path $inventoryPath
  if ($null -eq $inventory.sources -or $inventory.sources -isnot [System.Array] -or $inventory.sources.Count -lt 1) { throw 'INVENTORY_SOURCES_INVALID' }
  $inventorySourceCount = Get-StrictPropertyValue -Object $inventory -Name 'source_count'
  if ($inventorySourceCount -is [bool] -or $inventorySourceCount -is [string] -or $inventorySourceCount -isnot [ValueType]) { throw 'INVENTORY_SOURCE_COUNT_INVALID' }
  $inventorySourceCountNumber = [double]$inventorySourceCount
  if ([double]::IsNaN($inventorySourceCountNumber) -or [double]::IsInfinity($inventorySourceCountNumber) -or [Math]::Truncate($inventorySourceCountNumber) -ne $inventorySourceCountNumber -or $inventorySourceCountNumber -lt 1) { throw 'INVENTORY_SOURCE_COUNT_INVALID' }
  if ([int64]$inventorySourceCountNumber -ne [int64]$inventory.sources.Count) { throw 'INVENTORY_SOURCE_COUNT_MISMATCH' }
  $run.source_hashes_before = @(Get-CurrentSourceHashes -Sources @($inventory.sources))
  $run.source_hash_before = Get-SourceSnapshotHash -Sources @($run.source_hashes_before)
  [void](Assert-SourcesUnchanged -Stage 'G2_SOURCE_INVENTORY')

  $routingPath = Join-Path $resolvedWorkspace 'routing-decision.json'
  $startedAt = (Get-Date).ToUniversalTime().ToString('o')
  $routeStdoutPath = Join-Path $resolvedWorkspace 'route.stdout.txt'
  $stdout = @(& $pwsh -NoLogo -NoProfile -File (Join-Path $PSScriptRoot 'route-job.ps1') -InventoryPath $inventoryPath -JobContractPath $resolvedJobContract -RequestedOperation $contractOperation.ToLowerInvariant() -OutputPath $routingPath)
  $exitCode = $LASTEXITCODE
  Write-TextFileNew -Text ((@($stdout | ForEach-Object { [string]$_ })) -join [Environment]::NewLine) -Path $routeStdoutPath
  $status = if ($exitCode -eq 0) { 'PASS' } elseif ($exitCode -eq 3) { 'UNVERIFIED' } else { 'BLOCKED' }
  try {
    [void](Assert-GateArtifact -Path $routingPath -ExpectedStatus $status -ExitCode $exitCode -Gate 'G2_ROUTING_DECISION')
    $inventoryPath = Assert-RegularFilePath -Path $inventoryPath -Label 'SOURCE_INVENTORY_POST_ROUTING'
    $run.inventory_hash_after_routing = (Get-FileHash -LiteralPath $inventoryPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $run.inventory_hash_unchanged = $run.inventory_hash_after_routing -eq $run.inventory_hash_before_routing
    if (-not $run.inventory_hash_unchanged) { throw 'SOURCE_INVENTORY_CHANGED_DURING_ROUTING' }
    $routingPath = Assert-RegularFilePath -Path $routingPath -Label 'ROUTING_ARTIFACT_RECHECK'
    $run.routing_hash_before_validation = (Get-FileHash -LiteralPath $routingPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $route = Read-JsonFile -Path $routingPath
    Assert-RoutingPayload -Route $route -ExpectedSourceCount $run.source_hashes_before.Count -JobContract $jobContract
    if ([string]$route.status -ne $status) { throw "ROUTING_STATUS_EXIT_MISMATCH:exit=$exitCode;artifact=$($route.status);expected=$status" }
  } catch {
    $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
    Add-GateReceipt -Gate 'G2_ROUTING_DECISION' -Status 'BLOCKED' -ExitCode 2 -ArtifactPath $routingPath -StartedAt $startedAt -Reason "ARTIFACT_VALIDATION_FAILED:$message"
    throw
  }
  Add-GateReceipt -Gate 'G2_ROUTING_DECISION' -Status $status -ExitCode $exitCode -ArtifactPath $routingPath -StartedAt $startedAt
  $routingSchemaGate = Invoke-JsonSchemaGate -InputPath $routingPath -Schema 'routing-decision' -ReportPath (Join-Path $resolvedWorkspace 'routing-decision.validation.json') -StdoutPath (Join-Path $resolvedWorkspace 'routing-decision.validation.stdout.txt') -Gate 'G2_ROUTING_DECISION_SCHEMA'
  $routingPath = Assert-RegularFilePath -Path $routingPath -Label 'ROUTING_ARTIFACT_POST_VALIDATION'
  $run.routing_hash_after_validation = (Get-FileHash -LiteralPath $routingPath -Algorithm SHA256).Hash.ToLowerInvariant()
  $run.routing_hash_unchanged = $run.routing_hash_after_validation -eq $run.routing_hash_before_validation
  if (-not $run.routing_hash_unchanged) { throw 'ROUTING_ARTIFACT_CHANGED_DURING_VALIDATION' }
  [void](Assert-SourcesUnchanged -Stage 'G2_ROUTING_DECISION')
  [void](Assert-JobContractUnchanged -Stage 'G2_ROUTING_DECISION')
  $run.source_hashes_after = @($run.source_hash_checkpoints[$run.source_hash_checkpoints.Count - 1].sources)
  $run.source_hash_after = Get-SourceSnapshotHash -Sources @($run.source_hashes_after)
  $run.source_hash_unchanged = Test-SourceSnapshotsEqual -Expected @($run.source_hashes_before) -Actual @($run.source_hashes_after)
  if (-not $run.source_hash_unchanged) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  if ($routingSchemaGate.exit_code -eq 3) { Complete-Run -State 'UNVERIFIED' -ExitCode 3 }
  if ($routingSchemaGate.exit_code -ne 0) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  if ($exitCode -eq 3) { Complete-Run -State 'UNVERIFIED' -ExitCode 3 }
  if ($exitCode -ne 0) { Complete-Run -State 'BLOCKED' -ExitCode 2 }
  if ($SkipPreflight) { Complete-Run -State 'INTAKE_UNVERIFIED' -ExitCode 3 }
  Complete-Run -State 'INTAKE_PASS' -ExitCode 0
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  if ($run) {
    $run.state = 'BLOCKED'
    $run.error = $message
    $run.completed_at = (Get-Date).ToUniversalTime().ToString('o')
    try { Write-JsonFileMutable -Value $run -Path (Join-Path $resolvedWorkspace 'run-manifest.json') } catch {}
  }
  [Console]::Error.WriteLine($message)
  exit 2
}
