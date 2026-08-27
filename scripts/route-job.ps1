param(
  [Parameter(Mandatory = $true)][string]$InventoryPath,
  [string]$JobContractPath,
  [ValidateSet('auto', 'audit', 'repair', 'redesign', 'rebuild', 'create', 'update_data', 'extend', 'merge', 'localize', 'motion', 'certify')]
  [string]$RequestedOperation = 'auto',
  [Parameter(Mandatory = $true)][string]$OutputPath
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$deckFormats = @('PPTX', 'PPTM', 'PPT', 'ODP')
$documentFormats = @('DOCX', 'DOCM', 'DOC', 'TEXT', 'MARKDOWN', 'HTML')
$pdfFormats = @('PDF')
$dataFormats = @('XLSX', 'XLSM', 'XLS', 'ODS', 'CSV', 'TSV', 'JSON', 'XML')
$audioFormats = @('MP3', 'WAV', 'M4A', 'AAC', 'FLAC', 'OGG')
$videoFormats = @('MP4', 'MKV', 'AVI', 'WEBM')
$imageFormats = @('PNG', 'JPEG', 'GIF', 'TIFF', 'BMP', 'WEBP', 'SVG')
$archiveFormats = @('ZIP', '7Z', 'RAR', 'ZIP_CORRUPT')
$knownFormats = @($deckFormats + $documentFormats + $pdfFormats + $dataFormats + $audioFormats + $videoFormats + $imageFormats + $archiveFormats)
$operations = @('AUDIT', 'REPAIR', 'REDESIGN', 'REBUILD', 'CREATE', 'UPDATE_DATA', 'EXTEND', 'MERGE', 'LOCALIZE', 'MOTION', 'CERTIFY')
$modifierValues = @('REPAIR', 'UPDATE_DATA', 'TRANSCRIBE_MEDIA', 'EXTRACT_ARCHIVE', 'RECONCILE_SOURCES', 'CERTIFY')
$preservationModes = @('LOCKED', 'CONTROLLED', 'EDITORIAL', 'CREATIVE')
$certificationModes = @('DRAFT', 'STANDARD', 'CERTIFIED')
$resolvedInventoryPath = Assert-RegularFilePath -Path $InventoryPath -Label 'ROUTE_INVENTORY'
$resolvedOutputPath = Get-NormalizedFullPath -Path $OutputPath
$resolvedJobContractPath = if ($JobContractPath) { Get-NormalizedFullPath -Path $JobContractPath } else { $null }
$jobContract = $null
$jobContractHashBefore = $null
$outputIsSafe = $false

if (Test-PathsEqual -FirstPath $resolvedInventoryPath -SecondPath $resolvedOutputPath) {
  [Console]::Error.WriteLine("ROUTE_OUTPUT_PATH_COLLISION:$resolvedOutputPath")
  exit 2
}
if ($resolvedJobContractPath -and (Test-PathsEqual -FirstPath $resolvedJobContractPath -SecondPath $resolvedOutputPath)) {
  [Console]::Error.WriteLine('ROUTE_JOB_CONTRACT_COLLIDES_WITH_OUTPUT')
  exit 2
}
try {
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutputPath))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutputPath -ProtectedPaths @($resolvedInventoryPath, $resolvedJobContractPath) -Label 'ROUTE_OUTPUT')
  $outputIsSafe = $true
} catch {
  [Console]::Error.WriteLine(($_.Exception.Message -replace '[\r\n]+', ' ').Trim())
  exit 2
}

function Has-Property {
  param([Parameter(Mandatory = $true)][object]$Object, [Parameter(Mandatory = $true)][string]$Name)
  return $null -ne $Object.PSObject.Properties[$Name]
}

function New-FallbackRoute {
  param([Parameter(Mandatory = $true)][string]$Reason)
  return [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = 'BLOCKED'
    input_class = 'UNKNOWN_SOURCE'
    maturity = 'S0'
    primary_operation = if ($jobContract) { [string]$jobContract.primary_operation } elseif ($RequestedOperation -eq 'auto') { 'CREATE' } else { $RequestedOperation.ToUpperInvariant() }
    modifiers = [object[]]$(if ($jobContract) { @($jobContract.modifiers) } else { @('CERTIFY') })
    preservation_mode = if ($jobContract) { [string]$jobContract.preservation_mode } else { 'EDITORIAL' }
    visual_route = 'CUSTOM'
    data_authority = $null
    required_adapters = @()
    certification_mode = if ($jobContract) { [string]$jobContract.certification_mode } else { 'CERTIFIED' }
    job_contract_path = if ($jobContractHashBefore) { $resolvedJobContractPath } else { $null }
    job_contract_sha256 = if ($jobContractHashBefore) { $jobContractHashBefore } else { $null }
    source_count = 0
    blocking_reasons = @($Reason)
    unverified_reasons = @()
  }
}

if ($JobContractPath) {
  try {
    if (Test-PathsEqual -FirstPath $resolvedJobContractPath -SecondPath $resolvedInventoryPath) { throw 'ROUTE_JOB_CONTRACT_COLLIDES_WITH_INVENTORY' }
    $resolvedJobContractPath = Assert-RegularFilePath -Path $resolvedJobContractPath -Label 'ROUTE_JOB_CONTRACT'
    $jobContractHashBefore = (Get-FileHash -LiteralPath $resolvedJobContractPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $jobContractCandidate = Read-JsonFile -Path $resolvedJobContractPath
    if ($null -eq $jobContractCandidate -or $jobContractCandidate -is [System.Array] -or $jobContractCandidate -is [string] -or $jobContractCandidate -is [ValueType]) { throw 'ROUTE_JOB_CONTRACT_MUST_BE_OBJECT' }
    foreach ($name in @('schema_version', 'primary_operation', 'modifiers', 'preservation_mode', 'certification_mode')) {
      if ($null -eq $jobContractCandidate.PSObject.Properties[$name]) { throw "ROUTE_JOB_CONTRACT_PROPERTY_MISSING:$name" }
    }
    if ([string]$jobContractCandidate.schema_version -ne '1.0') { throw 'ROUTE_JOB_CONTRACT_SCHEMA_VERSION_INVALID' }
    $candidateOperation = [string]$jobContractCandidate.primary_operation
    if ($candidateOperation -notin $operations) { throw "ROUTE_JOB_CONTRACT_OPERATION_INVALID:$candidateOperation" }
    if ($jobContractCandidate.modifiers -isnot [System.Array]) { throw 'ROUTE_JOB_CONTRACT_MODIFIERS_INVALID' }
    $seenModifiers = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
    foreach ($modifier in @($jobContractCandidate.modifiers)) {
      if ($modifier -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$modifier)) { throw 'ROUTE_JOB_CONTRACT_MODIFIER_INVALID' }
      $candidateModifier = [string]$modifier
      if ($candidateModifier -notin $modifierValues) { throw "ROUTE_JOB_CONTRACT_MODIFIER_INVALID:$candidateModifier" }
      if (-not $seenModifiers.Add($candidateModifier)) { throw "ROUTE_JOB_CONTRACT_MODIFIER_DUPLICATE:$candidateModifier" }
    }
    $candidatePreservationMode = [string]$jobContractCandidate.preservation_mode
    if ($candidatePreservationMode -notin $preservationModes) { throw "ROUTE_JOB_CONTRACT_PRESERVATION_INVALID:$candidatePreservationMode" }
    $candidateCertificationMode = [string]$jobContractCandidate.certification_mode
    if ($candidateCertificationMode -notin $certificationModes) { throw "ROUTE_JOB_CONTRACT_CERTIFICATION_INVALID:$candidateCertificationMode" }
    $jobContract = $jobContractCandidate
  } catch {
    $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
    $route = New-FallbackRoute -Reason ("ROUTING_INPUT_INVALID:$message")
    if ($outputIsSafe -and -not (Test-Path -LiteralPath $resolvedOutputPath)) { Write-JsonFileNew -Value $route -Path $resolvedOutputPath }
    $route | ConvertTo-Json -Depth 20
    [Console]::Error.WriteLine($message)
    exit 2
  }
}

try {
  $inventory = Read-JsonFile -Path $resolvedInventoryPath
  if ($null -eq $inventory -or $inventory -is [System.Array] -or $inventory -is [string] -or $inventory -is [ValueType]) {
    throw 'INVENTORY_MUST_BE_OBJECT'
  }
  if (-not (Has-Property -Object $inventory -Name 'sources') -or $null -eq $inventory.sources) {
    throw 'INVENTORY_SOURCES_MISSING'
  }

  $sources = @($inventory.sources)
  if ($sources.Count -eq 0) { throw 'INVENTORY_CONTAINS_NO_SOURCES' }

  $blockingReasons = [System.Collections.Generic.List[string]]::new()
  $unverifiedReasons = [System.Collections.Generic.List[string]]::new()
  if (-not (Has-Property -Object $inventory -Name 'schema_version') -or [string]$inventory.schema_version -ne '1.0') {
    $blockingReasons.Add('INVENTORY_SCHEMA_VERSION_INVALID')
  }
  $hasInventoryStatus = Has-Property -Object $inventory -Name 'status'
  $inventoryStatus = if ($hasInventoryStatus) { [string]$inventory.status } else { '' }
  if (-not $hasInventoryStatus) {
    $blockingReasons.Add('INVENTORY_STATUS_MISSING')
  } elseif ($inventoryStatus -notin @('PASS', 'UNVERIFIED', 'BLOCKED')) {
    $blockingReasons.Add('INVALID_INVENTORY_STATUS')
  } elseif ($inventoryStatus -ne 'PASS') {
    $blockingReasons.Add('INVENTORY_NOT_CERTIFIED')
  }

  $sourceIds = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  $formats = [System.Collections.Generic.List[string]]::new()
  foreach ($source in $sources) {
    if ($null -eq $source -or $source -is [string] -or $source -is [ValueType]) {
      $blockingReasons.Add('MALFORMED_SOURCE_RECORD')
      continue
    }
    $sourceId = if (Has-Property -Object $source -Name 'source_id') { [string]$source.source_id } else { '' }
    if ([string]::IsNullOrWhiteSpace($sourceId)) {
      $blockingReasons.Add('SOURCE_ID_MISSING')
    } elseif (-not $sourceIds.Add($sourceId)) {
      $blockingReasons.Add("DUPLICATE_SOURCE_ID:$sourceId")
    }

    $format = if (Has-Property -Object $source -Name 'detected_format') { ([string]$source.detected_format).ToUpperInvariant() } else { '' }
    if ([string]::IsNullOrWhiteSpace($format) -or $format -notin $knownFormats) {
      $blockingReasons.Add("UNKNOWN_OR_MISSING_SOURCE_FORMAT:$sourceId")
    } else {
      $formats.Add($format)
    }

    $hasRiskFlags = (Has-Property -Object $source -Name 'risk_flags') -and ($null -ne $source.risk_flags)
    $riskFlags = if ($hasRiskFlags) { @($source.risk_flags | ForEach-Object { [string]$_ }) } else { @() }
    foreach ($riskFlag in $riskFlags) {
      switch ($riskFlag) {
        'MACRO_ENABLED' { $blockingReasons.Add('MACRO_SOURCE_REQUIRES_EXPLICIT_SAFE_HANDLING') }
        'CORRUPT_ARCHIVE' { $blockingReasons.Add('CORRUPT_ARCHIVE') }
        'UNKNOWN_FORMAT' { $blockingReasons.Add('UNKNOWN_FORMAT') }
        'SIGNATURE_EXTENSION_MISMATCH' { $blockingReasons.Add('SIGNATURE_EXTENSION_MISMATCH') }
        'EMPTY_FILE' { $blockingReasons.Add('EMPTY_SOURCE_FILE') }
        'REPARSE_POINT' { $blockingReasons.Add('REPARSE_POINT_SOURCE') }
        'SOURCE_CHANGED_DURING_INVENTORY' { $blockingReasons.Add('SOURCE_CHANGED_DURING_INVENTORY') }
      }
    }
  }

  $formatValues = @($formats)
  $hasDeck = @($formatValues | Where-Object { $_ -in $deckFormats }).Count -gt 0
  $hasDocument = @($formatValues | Where-Object { $_ -in $documentFormats }).Count -gt 0
  $hasPdf = @($formatValues | Where-Object { $_ -in $pdfFormats }).Count -gt 0
  $hasData = @($formatValues | Where-Object { $_ -in $dataFormats }).Count -gt 0
  $hasAudio = @($formatValues | Where-Object { $_ -in $audioFormats }).Count -gt 0
  $hasVideo = @($formatValues | Where-Object { $_ -in $videoFormats }).Count -gt 0
  $hasImage = @($formatValues | Where-Object { $_ -in $imageFormats }).Count -gt 0
  $hasArchive = @($formatValues | Where-Object { $_ -in $archiveFormats }).Count -gt 0
  $formatFamilies = @(@($hasDeck, $hasDocument, $hasPdf, $hasData, ($hasAudio -or $hasVideo), $hasImage, $hasArchive) | Where-Object { $_ }).Count

  if ($hasDeck) {
    $inputClass = 'EDITABLE_DECK'
    $maturity = 'S4'
    $defaultOperation = 'REDESIGN'
    $preservationMode = 'LOCKED'
    $visualRoute = 'SOURCE_DECK'
  } elseif ($formatFamilies -gt 1) {
    $inputClass = 'MIXED_SOURCES'
    $maturity = 'S1'
    $defaultOperation = 'CREATE'
    $preservationMode = 'EDITORIAL'
    $visualRoute = 'CUSTOM'
  } elseif ($hasPdf) {
    $inputClass = 'REPORT_OR_FLAT_SOURCE'
    $maturity = 'S3'
    $defaultOperation = 'CREATE'
    $preservationMode = 'CONTROLLED'
    $visualRoute = 'PDF_RECONSTRUCTION'
  } elseif ($hasDocument) {
    $inputClass = 'STRUCTURED_CONTENT'
    $maturity = 'S1'
    $defaultOperation = 'CREATE'
    $preservationMode = 'EDITORIAL'
    $visualRoute = 'CUSTOM'
  } elseif ($hasData) {
    $inputClass = 'DATA_SOURCE'
    $maturity = 'S1'
    $defaultOperation = 'CREATE'
    $preservationMode = 'CONTROLLED'
    $visualRoute = 'DATA_STORY'
  } elseif ($hasAudio -or $hasVideo) {
    $inputClass = 'MEDIA_SOURCE'
    $maturity = 'S0'
    $defaultOperation = 'CREATE'
    $preservationMode = 'EDITORIAL'
    $visualRoute = 'TRANSCRIPT_TO_STORY'
  } elseif ($hasImage) {
    $inputClass = 'VISUAL_SOURCE'
    $maturity = 'S0'
    $defaultOperation = 'REBUILD'
    $preservationMode = 'CONTROLLED'
    $visualRoute = 'VISUAL_RECONSTRUCTION'
  } elseif ($hasArchive) {
    $inputClass = 'ARCHIVE_SOURCE'
    $maturity = 'S0'
    $defaultOperation = 'CREATE'
    $preservationMode = 'CONTROLLED'
    $visualRoute = 'ARCHIVE_EXTRACTION'
  } else {
    $inputClass = 'UNKNOWN_SOURCE'
    $maturity = 'S0'
    $defaultOperation = 'CREATE'
    $preservationMode = 'EDITORIAL'
    $visualRoute = 'CUSTOM'
    $unverifiedReasons.Add('NO_SUPPORTED_SOURCE_FAMILY')
  }

  $contractOperation = if ($jobContract) { [string]$jobContract.primary_operation } else { $null }
  if ($jobContract -and $RequestedOperation -ne 'auto' -and $RequestedOperation.ToUpperInvariant() -ne $contractOperation) {
    $blockingReasons.Add("REQUESTED_OPERATION_JOB_CONTRACT_MISMATCH:requested=$($RequestedOperation.ToUpperInvariant());contract=$contractOperation")
  }
  $primaryOperation = if ($jobContract) { $contractOperation } elseif ($RequestedOperation -eq 'auto') { $defaultOperation } else { $RequestedOperation.ToUpperInvariant() }
  if ($primaryOperation -in @('REPAIR', 'REDESIGN', 'UPDATE_DATA', 'EXTEND', 'LOCALIZE', 'MOTION', 'CERTIFY') -and -not $hasDeck) {
    $blockingReasons.Add('OPERATION_REQUIRES_DECK')
  }
  if ($primaryOperation -eq 'UPDATE_DATA' -and -not $hasData) {
    $blockingReasons.Add('OPERATION_REQUIRES_DATA')
  }
  if ($primaryOperation -eq 'MERGE' -and $sources.Count -lt 2) {
    $blockingReasons.Add('OPERATION_REQUIRES_MULTIPLE_SOURCES')
  }

  $modifiers = [System.Collections.Generic.List[string]]::new()
  if ($jobContract) {
    foreach ($modifier in @($jobContract.modifiers)) { $modifiers.Add([string]$modifier) }
  } else {
    if ($hasDeck -and $primaryOperation -eq 'REDESIGN') { $modifiers.Add('REPAIR') }
    if ($hasData -and $hasDeck) { $modifiers.Add('UPDATE_DATA') }
    if ($hasAudio -or $hasVideo) { $modifiers.Add('TRANSCRIBE_MEDIA') }
    if ($hasArchive) { $modifiers.Add('EXTRACT_ARCHIVE') }
    if ($sources.Count -gt 1) { $modifiers.Add('RECONCILE_SOURCES') }
    $modifiers.Add('CERTIFY')
  }
  if ('REPAIR' -in $modifiers -and -not $hasDeck) { $blockingReasons.Add('MODIFIER_REPAIR_REQUIRES_DECK') }
  if ('UPDATE_DATA' -in $modifiers -and -not $hasDeck) { $blockingReasons.Add('MODIFIER_UPDATE_DATA_REQUIRES_DECK') }
  if ('UPDATE_DATA' -in $modifiers -and -not $hasData) { $blockingReasons.Add('MODIFIER_UPDATE_DATA_REQUIRES_DATA') }
  if ('TRANSCRIBE_MEDIA' -in $modifiers -and -not ($hasAudio -or $hasVideo)) { $blockingReasons.Add('MODIFIER_TRANSCRIBE_MEDIA_REQUIRES_AUDIO_OR_VIDEO') }
  if ('EXTRACT_ARCHIVE' -in $modifiers -and -not $hasArchive) { $blockingReasons.Add('MODIFIER_EXTRACT_ARCHIVE_REQUIRES_ARCHIVE') }
  if ('RECONCILE_SOURCES' -in $modifiers -and $sources.Count -lt 2) { $blockingReasons.Add('MODIFIER_RECONCILE_SOURCES_REQUIRES_MULTIPLE_SOURCES') }

  $requiredAdapters = [System.Collections.Generic.List[object]]::new()
  foreach ($format in @($formatValues | Select-Object -Unique)) {
    $adapter = switch ($format) {
      { $_ -in $deckFormats } { 'POWERPOINT'; break }
      { $_ -in $pdfFormats } { 'PDF'; break }
      { $_ -in $documentFormats } { 'DOCUMENT'; break }
      { $_ -in $dataFormats } { 'DATA'; break }
      { $_ -in $audioFormats } { 'AUDIO'; break }
      { $_ -in $videoFormats } { 'VIDEO'; break }
      { $_ -in $imageFormats } { 'IMAGE'; break }
      { $_ -in $archiveFormats } { 'ARCHIVE'; break }
      default { 'UNKNOWN' }
    }
    $requiredAdapters.Add([ordered]@{ format = $format; adapter = $adapter })
  }

  $dataAuthorities = @($sources | Where-Object { (Has-Property -Object $_ -Name 'role') -and ([string]$_.role -eq 'DATA_AUTHORITY') })
  if ($dataAuthorities.Count -gt 1) { $blockingReasons.Add('MULTIPLE_DATA_AUTHORITIES_REQUIRE_RECONCILIATION') }
  $blockingUnique = @($blockingReasons | Select-Object -Unique)
  $unverifiedUnique = @($unverifiedReasons | Select-Object -Unique)
  $status = if ($blockingUnique.Count -gt 0) { 'BLOCKED' } elseif ($unverifiedUnique.Count -gt 0) { 'UNVERIFIED' } else { 'PASS' }

  $route = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = $status
    input_class = $inputClass
    maturity = $maturity
    primary_operation = $primaryOperation
    modifiers = @($modifiers | Select-Object -Unique)
    preservation_mode = if ($jobContract) { [string]$jobContract.preservation_mode } else { $preservationMode }
    visual_route = $visualRoute
    data_authority = if ($dataAuthorities.Count -eq 1) { [string]$dataAuthorities[0].source_id } else { $null }
    required_adapters = @($requiredAdapters)
    certification_mode = if ($jobContract) { [string]$jobContract.certification_mode } else { 'CERTIFIED' }
    job_contract_path = $resolvedJobContractPath
    job_contract_sha256 = $jobContractHashBefore
    source_count = $sources.Count
    blocking_reasons = $blockingUnique
    unverified_reasons = $unverifiedUnique
  }
  if ($resolvedJobContractPath) {
    $jobContractHashAfter = (Get-FileHash -LiteralPath (Assert-RegularFilePath -Path $resolvedJobContractPath -Label 'ROUTE_JOB_CONTRACT_RECHECK') -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($jobContractHashAfter -ne $jobContractHashBefore) { throw 'ROUTE_JOB_CONTRACT_CHANGED_DURING_ROUTING' }
  }
  Write-JsonFileNew -Value $route -Path $resolvedOutputPath
  $route | ConvertTo-Json -Depth 20
  if ($status -eq 'BLOCKED') { exit 2 }
  if ($status -eq 'UNVERIFIED') { exit 3 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $route = New-FallbackRoute -Reason ("ROUTING_INPUT_INVALID:$message")
  if ($outputIsSafe -and -not (Test-Path -LiteralPath $resolvedOutputPath)) { Write-JsonFileNew -Value $route -Path $resolvedOutputPath }
  $route | ConvertTo-Json -Depth 20
  [Console]::Error.WriteLine($message)
  exit 2
}
