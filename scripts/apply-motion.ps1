param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [Parameter(Mandatory = $true)][string]$StoryboardPath,
  [Parameter(Mandatory = $true)][string]$StaticCertificationPath,
  [Parameter(Mandatory = $true)][string]$ReportPath
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoFalse = 0
$msoTrue = -1
$msoAnimateLevelNone = 0
$effectMap = @{ appear = 1; fade = 10; wipe = 22; grow = 6 }
$triggerMap = @{ on_click = 1; with_previous = 2; after_previous = 3 }
$transitionMap = @{ none = 0; fade_smoothly = 3849; morph = 3954 }
$hashPattern = '^[0-9a-fA-F]{64}$'
$staticRequiredDomains = @('source_integrity', 'content_fidelity', 'data_accuracy', 'narrative_logic', 'visual_design', 'layout_typography', 'charts_tables', 'images_icons', 'native_compatibility')
$staticRequiredEvidence = @('source_hash_unchanged', 'mandatory_capabilities_verified', 'all_slides_rendered', 'all_slides_reviewed', 'all_data_validated', 'all_changes_documented', 'blueprint_coverage_verified', 'visual_assets_verified', 'contrast_verified', 'icon_consistency_verified', 'source_traceability_verified', 'fresh_powerpoint_open')
$qualityScoreFormulaVersion = 'WEIGHTED_DOMAIN_V1'
$sourceHashFormulaVersion = 'SOURCE_FILE_SHA256_OR_SET_V1'
$qualityScoreTolerance = 0.05
$qualityScoreWeights = [ordered]@{
  source_integrity = 3.0
  content_fidelity = 18.0
  data_accuracy = 16.0
  narrative_logic = 10.0
  visual_design = 12.0
  layout_typography = 14.0
  charts_tables = 8.0
  images_icons = 7.0
  motion = 6.0
  native_compatibility = 6.0
}
$receiptFutureSkewSeconds = 300

$resolvedInput = $null
$resolvedOutput = $null
$resolvedStoryboard = $null
$resolvedStaticCertificate = $null
$resolvedReport = $null
$sourceHashBefore = $null
$sourceHashAfter = $null
$storyboardHashBefore = $null
$storyboardHashAfter = $null
$staticCertificateHashBefore = $null
$staticCertificateHashAfter = $null
$outputCreated = $false
$powerPoint = $null
$presentation = $null

function Has-Property {
  param([Parameter(Mandatory = $true)][object]$Object, [Parameter(Mandatory = $true)][string]$Name)
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Assert-NoUnknownProperties {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string[]]$Allowed,
    [Parameter(Mandatory = $true)][string]$Label
  )
  foreach ($property in @($Object.PSObject.Properties | ForEach-Object { $_.Name })) {
    if ($property -notin $Allowed) { throw "${Label}_UNKNOWN_PROPERTY:$property" }
  }
}

function ConvertTo-StrictInteger {
  param([object]$Value, [int]$Minimum = 1, [int]$Maximum = 100000, [string]$Label = 'value')
  if ($null -eq $Value -or $Value -is [bool] -or $Value -is [string]) { throw "INVALID_INTEGER:$Label" }
  $candidate = 0.0
  if (-not [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate) -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or [Math]::Truncate($candidate) -ne $candidate -or $candidate -lt $Minimum -or $candidate -gt $Maximum) {
    throw "INVALID_INTEGER:$Label"
  }
  return [int]$candidate
}

function ConvertTo-StrictFiniteNumber {
  param([object]$Value, [double]$Minimum, [double]$Maximum, [string]$Label)
  if ($null -eq $Value -or $Value -is [bool] -or $Value -is [string]) { throw "INVALID_NUMBER:$Label" }
  $candidate = 0.0
  if (-not [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate) -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or $candidate -lt $Minimum -or $candidate -gt $Maximum) {
    throw "INVALID_NUMBER:$Label"
  }
  return $candidate
}

function Assert-ReceiptTimestamp {
  param([object]$Value, [string]$Label)
  $parsed = [DateTimeOffset]::MinValue
  $valid = $false
  if ($Value -is [DateTimeOffset]) {
    $parsed = [DateTimeOffset]$Value
    $valid = $true
  } elseif ($Value -is [DateTime] -and $Value.Kind -ne [DateTimeKind]::Unspecified) {
    $parsed = [DateTimeOffset]$Value
    $valid = $true
  } elseif ($Value -is [string] -and -not [string]::IsNullOrWhiteSpace($Value) -and $Value -match '(Z|[+-]\d{2}:\d{2})$') {
    $valid = [DateTimeOffset]::TryParse(
      $Value,
      [Globalization.CultureInfo]::InvariantCulture,
      ([Globalization.DateTimeStyles]::AssumeUniversal -bor [Globalization.DateTimeStyles]::AdjustToUniversal),
      [ref]$parsed
    )
  }
  if (-not $valid) { throw "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_INVALID:$Label" }
  if ($parsed -gt [DateTimeOffset]::UtcNow.AddSeconds($receiptFutureSkewSeconds)) { throw "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_IN_FUTURE:$Label" }
  return $parsed
}

function Get-StaticCalculatedQualityScore {
  param([Parameter(Mandatory = $true)][object]$Scores)
  $weightedTotal = 0.0
  $weightTotal = 0.0
  foreach ($domainName in $staticRequiredDomains) {
    $weight = [double]$qualityScoreWeights[$domainName]
    $weightedTotal += ([double]$Scores.$domainName) * $weight
    $weightTotal += $weight
  }
  return [Math]::Round($weightedTotal / $weightTotal, 4, [MidpointRounding]::AwayFromZero)
}

function Get-StaticSourceSetHash {
  param([Parameter(Mandatory = $true)][object[]]$Bindings)
  if ($Bindings.Count -eq 1) { return [string]$Bindings[0].actual_sha256.ToLowerInvariant() }
  $records = [System.Collections.Generic.List[string]]::new()
  foreach ($binding in $Bindings) {
    $normalizedPath = (Get-NormalizedFullPath -Path ([string]$binding.path)).ToLowerInvariant()
    $records.Add(([string]$binding.source_id + [char]0x1F + $normalizedPath + [char]0x1F + ([string]$binding.actual_sha256).ToLowerInvariant()))
  }
  $canonical = [string]::Join("`n", @($records | Sort-Object -CaseSensitive))
  $sha = [Security.Cryptography.SHA256]::Create()
  try {
    return ([Convert]::ToHexString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($canonical)))).ToLowerInvariant()
  } finally {
    $sha.Dispose()
  }
}

function Assert-Object {
  param([object]$Value, [string]$Label)
  if ($null -eq $Value -or $Value -is [System.Array] -or $Value -is [string] -or $Value -is [ValueType]) { throw "MALFORMED_OBJECT:$Label" }
}

function Assert-Array {
  param([object]$Value, [string]$Label, [int]$Minimum = 0)
  if ($null -eq $Value -or $Value -isnot [System.Array] -or $Value.Count -lt $Minimum) { throw "MALFORMED_ARRAY:$Label" }
}

function Assert-ExactStringSet {
  param(
    [object]$Value,
    [string[]]$Expected,
    [string]$ErrorCode
  )
  if ($Value -isnot [System.Array]) { throw $ErrorCode }
  $seen = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
  foreach ($item in @($Value)) {
    if ($item -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$item) -or -not $seen.Add([string]$item)) { throw $ErrorCode }
  }
  if ($seen.Count -ne $Expected.Count) { throw $ErrorCode }
  foreach ($expectedItem in $Expected) { if (-not $seen.Contains($expectedItem)) { throw $ErrorCode } }
}

function Assert-PathNotReparse {
  param([string]$Path, [string]$Label)
  try { Assert-NoReparseAncestors -Path $Path } catch { throw "${Label}_$($_.Exception.Message)" }
}

function Write-ReportNew {
  param([object]$Value)
  if ($resolvedReport -and -not (Test-Path -LiteralPath $resolvedReport)) { Write-JsonFileNew -Value $Value -Path $resolvedReport }
}

function Assert-StaticCertificate {
  param(
    [Parameter(Mandatory = $true)][object]$Certificate,
    [Parameter(Mandatory = $true)][string]$InputDeck,
    [Parameter(Mandatory = $true)][string]$InputHash
  )
  Assert-Object -Value $Certificate -Label 'static certificate'
  $inputDeckLastWriteUtc = [DateTimeOffset](Get-Item -LiteralPath $InputDeck -Force -ErrorAction Stop).LastWriteTimeUtc
  if (-not (Has-Property -Object $Certificate -Name 'status') -or [string]$Certificate.status -ne 'PASS') { throw 'STATIC_CERTIFICATION_MUST_PASS_BEFORE_MOTION' }
  if (-not (Has-Property -Object $Certificate -Name 'output_sha256') -or [string]$Certificate.output_sha256 -notmatch $hashPattern) { throw 'STATIC_CERTIFICATE_DECK_HASH_INVALID' }
  if ([string]$Certificate.output_sha256.ToLowerInvariant() -ne $InputHash) { throw 'STATIC_CERTIFICATE_DECK_HASH_MISMATCH' }
  if (-not (Has-Property -Object $Certificate -Name 'certification_profile') -or [string]$Certificate.certification_profile -ne 'STATIC_READY_FOR_MOTION') { throw 'STATIC_CERTIFICATION_PROFILE_REQUIRED' }
  foreach ($requiredProperty in @('output_path', 'output_sha256', 'output_detected_format', 'source_hash_unchanged', 'source_hash_before', 'source_hash_after', 'quality_score', 'calculated_quality_score', 'domain_scores', 'required_domains', 'required_evidence', 'evidence_receipts', 'blocking_requirements', 'unverified_requirements', 'failed_requirements', 'source_bindings', 'certification_rules')) {
    if (-not (Has-Property -Object $Certificate -Name $requiredProperty)) { throw "STATIC_CERTIFICATE_PROPERTY_MISSING:$requiredProperty" }
  }
  if (-not (Test-PathsEqual -FirstPath ([string]$Certificate.output_path) -SecondPath $InputDeck)) { throw 'STATIC_CERTIFICATE_DECK_PATH_MISMATCH' }
  $actualDeckFormat = Get-DetectedFileFormat -Path $InputDeck
  if ([string]$Certificate.output_detected_format -ne $actualDeckFormat -or $actualDeckFormat -notin @('PPTX', 'PPTM', 'PPT', 'ODP')) { throw 'STATIC_CERTIFICATE_OUTPUT_FORMAT_MISMATCH' }
  if ($Certificate.source_hash_unchanged -isnot [bool] -or $Certificate.source_hash_unchanged -ne $true) { throw 'STATIC_CERTIFICATE_SOURCE_HASH_NOT_VERIFIED' }
  foreach ($hashProperty in @('source_hash_before', 'source_hash_after')) {
    if ([string]$Certificate.$hashProperty -notmatch $hashPattern) { throw "STATIC_CERTIFICATE_SOURCE_HASH_INVALID:$hashProperty" }
  }
  if ([string]$Certificate.source_hash_before -ine [string]$Certificate.source_hash_after) { throw 'STATIC_CERTIFICATE_SOURCE_HASH_NOT_VERIFIED' }
  $staticQualityScore = ConvertTo-StrictFiniteNumber -Value $Certificate.quality_score -Minimum 97 -Maximum 100 -Label 'static quality_score'
  $staticCalculatedQualityScore = ConvertTo-StrictFiniteNumber -Value $Certificate.calculated_quality_score -Minimum 97 -Maximum 100 -Label 'static calculated_quality_score'
  Assert-ExactStringSet -Value $Certificate.required_domains -Expected $staticRequiredDomains -ErrorCode 'STATIC_CERTIFICATE_REQUIRED_DOMAINS_MISMATCH'
  Assert-ExactStringSet -Value $Certificate.required_evidence -Expected $staticRequiredEvidence -ErrorCode 'STATIC_CERTIFICATE_REQUIRED_EVIDENCE_MISMATCH'
  Assert-Object -Value $Certificate.domain_scores -Label 'static domain scores'
  $domainNames = @($Certificate.domain_scores.PSObject.Properties | ForEach-Object { [string]$_.Name })
  Assert-ExactStringSet -Value $domainNames -Expected $staticRequiredDomains -ErrorCode 'STATIC_CERTIFICATE_DOMAIN_SET_MISMATCH'
  foreach ($domainName in $staticRequiredDomains) {
    if (-not (Has-Property -Object $Certificate.domain_scores -Name $domainName)) { throw "STATIC_CERTIFICATE_DOMAIN_MISSING:$domainName" }
    [void](ConvertTo-StrictFiniteNumber -Value $Certificate.domain_scores.$domainName -Minimum 90 -Maximum 100 -Label "static domain:$domainName")
  }
  $recalculatedQualityScore = Get-StaticCalculatedQualityScore -Scores $Certificate.domain_scores
  if ([Math]::Abs($staticQualityScore - $staticCalculatedQualityScore) -gt 0.0001 -or [Math]::Abs($staticCalculatedQualityScore - $recalculatedQualityScore) -gt 0.0001) {
    throw 'STATIC_CERTIFICATE_QUALITY_SCORE_MISMATCH'
  }
  Assert-Object -Value $Certificate.certification_rules -Label 'static certification rules'
  foreach ($rule in @(
    @{ name = 'minimum_quality_score'; value = 97 },
    @{ name = 'minimum_domain_score'; value = 90 },
    @{ name = 'policy_minimum_quality_score'; value = 97 },
    @{ name = 'policy_minimum_domain_score'; value = 90 },
    @{ name = 'maximum_p0_findings'; value = 0 },
    @{ name = 'maximum_p1_findings'; value = 0 }
  )) {
    if (-not (Has-Property -Object $Certificate.certification_rules -Name $rule.name) -or [double]$Certificate.certification_rules.($rule.name) -ne [double]$rule.value) { throw "STATIC_CERTIFICATE_POLICY_MISMATCH:$($rule.name)" }
  }
  if (-not (Has-Property -Object $Certificate.certification_rules -Name 'quality_score_formula') -or [string]$Certificate.certification_rules.quality_score_formula -ne $qualityScoreFormulaVersion) {
    throw 'STATIC_CERTIFICATE_POLICY_MISMATCH:quality_score_formula'
  }
  if (-not (Has-Property -Object $Certificate.certification_rules -Name 'source_hash_formula') -or [string]$Certificate.certification_rules.source_hash_formula -ne $sourceHashFormulaVersion) {
    throw 'STATIC_CERTIFICATE_POLICY_MISMATCH:source_hash_formula'
  }
  if (-not (Has-Property -Object $Certificate.certification_rules -Name 'quality_score_tolerance') -or [double]$Certificate.certification_rules.quality_score_tolerance -ne $qualityScoreTolerance) {
    throw 'STATIC_CERTIFICATE_POLICY_MISMATCH:quality_score_tolerance'
  }
  if (-not (Has-Property -Object $Certificate.certification_rules -Name 'domain_weights')) { throw 'STATIC_CERTIFICATE_POLICY_MISMATCH:domain_weights' }
  Assert-Object -Value $Certificate.certification_rules.domain_weights -Label 'static domain weights'
  foreach ($domainName in $qualityScoreWeights.Keys) {
    $weightProperty = $Certificate.certification_rules.domain_weights.PSObject.Properties[[string]$domainName]
    if ($null -eq $weightProperty -or [double]$weightProperty.Value -ne [double]$qualityScoreWeights[$domainName]) { throw "STATIC_CERTIFICATE_POLICY_MISMATCH:domain_weights.$domainName" }
  }
  foreach ($listName in @('blocking_requirements', 'unverified_requirements', 'failed_requirements')) {
    if ($Certificate.$listName -isnot [System.Array] -or @($Certificate.$listName).Count -ne 0) { throw "STATIC_CERTIFICATE_$($listName.ToUpperInvariant())_NOT_EMPTY" }
  }
  $receiptContainer = $Certificate.evidence_receipts
  Assert-Object -Value $receiptContainer -Label 'static evidence receipts'
  $requiredReceiptEvidence = @($staticRequiredEvidence | Where-Object { $_ -ne 'source_hash_unchanged' })
  $receiptNames = @($receiptContainer.PSObject.Properties | ForEach-Object { [string]$_.Name })
  Assert-ExactStringSet -Value $receiptNames -Expected $requiredReceiptEvidence -ErrorCode 'STATIC_CERTIFICATE_RECEIPT_SET_MISMATCH'
  foreach ($evidenceName in $requiredReceiptEvidence) {
    $receiptProperty = $receiptContainer.PSObject.Properties[[string]$evidenceName]
    if ($null -eq $receiptProperty) { throw "STATIC_CERTIFICATE_RECEIPT_MISSING:$evidenceName" }
    $receipt = $receiptProperty.Value
    Assert-Object -Value $receipt -Label "static receipt:$evidenceName"
    if ([string]$receipt.status -ne 'PASS' -or [string]$receipt.sha256 -notmatch $hashPattern) { throw "STATIC_CERTIFICATE_RECEIPT_NOT_VERIFIED:$evidenceName" }
    $summaryTimestamp = Assert-ReceiptTimestamp -Value $receipt.generated_at -Label $evidenceName
    if ($summaryTimestamp -lt $inputDeckLastWriteUtc.AddSeconds(-$receiptFutureSkewSeconds)) { throw "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_PREDATES_DECK:$evidenceName" }
    if (-not (Test-PathsEqual -FirstPath ([string]$receipt.subject_path) -SecondPath $InputDeck)) { throw "STATIC_CERTIFICATE_RECEIPT_SUBJECT_PATH_MISMATCH:$evidenceName" }
    if ([string]$receipt.subject_sha256 -notmatch $hashPattern -or [string]$receipt.subject_sha256 -ine $InputHash) { throw "STATIC_CERTIFICATE_RECEIPT_SUBJECT_HASH_MISMATCH:$evidenceName" }
    if ([string]::IsNullOrWhiteSpace([string]$receipt.producer) -or [int]$receipt.check_count -lt 1) { throw "STATIC_CERTIFICATE_RECEIPT_SUMMARY_INVALID:$evidenceName" }
    $receiptPath = Assert-RegularFilePath -Path ([string]$receipt.path) -Label "STATIC_RECEIPT_$evidenceName"
    if ((Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne [string]$receipt.sha256.ToLowerInvariant()) { throw "STATIC_CERTIFICATE_RECEIPT_HASH_MISMATCH:$evidenceName" }
    $receiptPayload = Read-JsonFile -Path $receiptPath
    Assert-Object -Value $receiptPayload -Label "static receipt payload:$evidenceName"
    if ([string]$receiptPayload.evidence_name -ne $evidenceName -or [string]$receiptPayload.status -ne 'PASS') { throw "STATIC_CERTIFICATE_RECEIPT_PAYLOAD_MISMATCH:$evidenceName" }
    $payloadTimestamp = Assert-ReceiptTimestamp -Value $receiptPayload.generated_at -Label $evidenceName
    if ($payloadTimestamp -lt $inputDeckLastWriteUtc.AddSeconds(-$receiptFutureSkewSeconds)) { throw "STATIC_CERTIFICATE_RECEIPT_TIMESTAMP_PREDATES_DECK:$evidenceName" }
    if (-not (Test-PathsEqual -FirstPath ([string]$receiptPayload.subject_path) -SecondPath $InputDeck)) { throw "STATIC_CERTIFICATE_RECEIPT_SUBJECT_PATH_MISMATCH:$evidenceName" }
    if ([string]$receiptPayload.subject_sha256 -notmatch $hashPattern -or [string]$receiptPayload.subject_sha256 -ine $InputHash) { throw "STATIC_CERTIFICATE_RECEIPT_SUBJECT_HASH_MISMATCH:$evidenceName" }
    if ([string]::IsNullOrWhiteSpace([string]$receiptPayload.producer) -or [string]$receiptPayload.producer -ne [string]$receipt.producer) { throw "STATIC_CERTIFICATE_RECEIPT_PRODUCER_MISMATCH:$evidenceName" }
    Assert-Array -Value $receiptPayload.checks -Label "static receipt checks:$evidenceName" -Minimum 1
    if (@($receiptPayload.checks).Count -ne [int]$receipt.check_count) { throw "STATIC_CERTIFICATE_RECEIPT_CHECK_COUNT_MISMATCH:$evidenceName" }
    $checkIds = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($check in @($receiptPayload.checks)) {
      Assert-Object -Value $check -Label "static receipt check:$evidenceName"
      if ([string]::IsNullOrWhiteSpace([string]$check.check_id) -or -not $checkIds.Add([string]$check.check_id) -or [string]$check.status -ne 'PASS') { throw "STATIC_CERTIFICATE_RECEIPT_CHECK_INVALID:$evidenceName" }
    }
    if ($evidenceName -eq 'visual_assets_verified') {
      if (-not (Has-Property -Object $receipt -Name 'metadata')) { throw 'NATIVE_VISUAL_BINDING_MISSING:certificate_summary' }
      if (-not (Has-Property -Object $receiptPayload -Name 'metadata')) { throw 'NATIVE_VISUAL_BINDING_MISSING:raw_receipt' }
      $summaryNativeBinding = Assert-NativeVisualCoverageBinding -Metadata $receipt.metadata -ExpectedDeckPath $InputDeck -ExpectedDeckHash $InputHash -Label 'certificate_summary'
      $payloadNativeBinding = Assert-NativeVisualCoverageBinding -Metadata $receiptPayload.metadata -ExpectedDeckPath $InputDeck -ExpectedDeckHash $InputHash -Label 'raw_receipt'
      foreach ($bindingField in @('native_bindings_verified', 'native_visual_coverage_report_path', 'native_visual_coverage_report_sha256', 'native_visual_coverage_deck_sha256')) {
        if ([string]$summaryNativeBinding[$bindingField] -ne [string]$payloadNativeBinding[$bindingField]) { throw "NATIVE_VISUAL_BINDING_SUMMARY_RAW_MISMATCH:$bindingField" }
      }
    }
  }
  $bindings = @($Certificate.source_bindings)
  if ($bindings.Count -lt 1) { throw 'STATIC_CERTIFICATE_SOURCE_BINDINGS_MISSING' }
  $verifiedBindings = [System.Collections.Generic.List[object]]::new()
  foreach ($binding in $bindings) {
    Assert-Object -Value $binding -Label 'static source binding'
    foreach ($hashProperty in @('sha256_before', 'sha256_after', 'actual_sha256')) {
      if (-not (Has-Property -Object $binding -Name $hashProperty) -or [string]$binding.$hashProperty -notmatch $hashPattern) { throw "STATIC_CERTIFICATE_SOURCE_BINDING_INVALID:$hashProperty" }
    }
    if ([string]$binding.sha256_before -ne [string]$binding.sha256_after -or [string]$binding.sha256_before -ne [string]$binding.actual_sha256) { throw 'STATIC_CERTIFICATE_SOURCE_BINDING_HASH_MISMATCH' }
    $boundSource = Assert-RegularFilePath -Path ([string]$binding.path) -Label 'STATIC_BOUND_SOURCE'
    $actualBoundHash = (Get-FileHash -LiteralPath $boundSource -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualBoundHash -ne [string]$binding.actual_sha256.ToLowerInvariant()) { throw 'STATIC_CERTIFICATE_SOURCE_BINDING_STALE' }
    $verifiedBindings.Add([ordered]@{ source_id = [string]$binding.source_id; path = $boundSource; actual_sha256 = $actualBoundHash })
  }
  $calculatedSourceSetHash = Get-StaticSourceSetHash -Bindings @($verifiedBindings)
  if ([string]$Certificate.source_hash_before -ine $calculatedSourceSetHash -or [string]$Certificate.source_hash_after -ine $calculatedSourceSetHash) { throw 'STATIC_CERTIFICATE_SOURCE_SET_HASH_MISMATCH' }
}

try {
  $resolvedInput = Assert-RegularFilePath -Path $InputPath -Label 'MOTION_INPUT'
  $resolvedStoryboard = Assert-RegularFilePath -Path $StoryboardPath -Label 'STORYBOARD'
  $resolvedStaticCertificate = Assert-RegularFilePath -Path $StaticCertificationPath -Label 'STATIC_CERTIFICATE'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  $resolvedReport = Get-NormalizedFullPath -Path $ReportPath
  Assert-PathNotReparse -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput)) -Label 'OUTPUT'
  Assert-PathNotReparse -Path ([System.IO.Path]::GetDirectoryName($resolvedReport)) -Label 'REPORT'
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedInput, $resolvedStoryboard, $resolvedStaticCertificate, $resolvedReport) -Label 'MOTION_OUTPUT')
  [void](Assert-NewOutputPath -OutputPath $resolvedReport -ProtectedPaths @($resolvedInput, $resolvedStoryboard, $resolvedStaticCertificate, $resolvedOutput) -Label 'MOTION_REPORT')
  if ([System.IO.Path]::GetExtension($resolvedInput).ToLowerInvariant() -ne [System.IO.Path]::GetExtension($resolvedOutput).ToLowerInvariant()) { throw 'MOTION_OUTPUT_EXTENSION_MUST_MATCH_INPUT' }

  $sourceHashBefore = (Get-FileHash -LiteralPath $resolvedInput -Algorithm SHA256).Hash.ToLowerInvariant()
  $storyboardHashBefore = (Get-FileHash -LiteralPath $resolvedStoryboard -Algorithm SHA256).Hash.ToLowerInvariant()
  $staticCertificateHashBefore = (Get-FileHash -LiteralPath $resolvedStaticCertificate -Algorithm SHA256).Hash.ToLowerInvariant()
  $staticCertificate = Read-JsonFile -Path $resolvedStaticCertificate
  Assert-StaticCertificate -Certificate $staticCertificate -InputDeck $resolvedInput -InputHash $sourceHashBefore
  $certificateHashProperty = $staticCertificate.PSObject.Properties['output_sha256']
  $certificateOutputHash = if ($null -ne $certificateHashProperty) { [string]$certificateHashProperty.Value } else { '' }
  if ($certificateOutputHash -notmatch $hashPattern) { throw 'STATIC_CERTIFICATE_DECK_HASH_INVALID' }
  if ($certificateOutputHash.ToLowerInvariant() -ne $sourceHashBefore) { throw 'STATIC_CERTIFICATE_DECK_HASH_MISMATCH' }

  $storyboard = Read-JsonFile -Path $resolvedStoryboard
  Assert-Object -Value $storyboard -Label 'storyboard'
  if (-not (Has-Property -Object $storyboard -Name 'schema_version') -or [string]$storyboard.schema_version -ne '1.0') { throw 'STORYBOARD_SCHEMA_VERSION_INVALID' }
  Assert-NoUnknownProperties -Object $storyboard -Allowed @('schema_version', 'click_controlled', 'auto_advance_allowed', 'replace_existing', 'max_effects_per_slide', 'slides') -Label 'STORYBOARD'
  foreach ($requiredProperty in @('click_controlled', 'auto_advance_allowed', 'replace_existing', 'slides')) {
    if (-not (Has-Property -Object $storyboard -Name $requiredProperty)) { throw "STORYBOARD_PROPERTY_MISSING:$requiredProperty" }
  }
  if ($storyboard.click_controlled -isnot [bool] -or $storyboard.click_controlled -ne $true) { throw 'STORYBOARD_MUST_BE_CLICK_CONTROLLED' }
  if ($storyboard.auto_advance_allowed -isnot [bool] -or $storyboard.auto_advance_allowed -ne $false) { throw 'STORYBOARD_AUTO_ADVANCE_NOT_ALLOWED' }
  if ($storyboard.replace_existing -isnot [bool] -or $storyboard.replace_existing -ne $true) { throw 'STORYBOARD_REPLACE_EXISTING_MUST_BE_TRUE' }
  Assert-Array -Value $storyboard.slides -Label 'slides' -Minimum 1
  $maximumEffects = 40
  if (Has-Property -Object $storyboard -Name 'max_effects_per_slide') {
    $maximumEffects = ConvertTo-StrictInteger -Value $storyboard.max_effects_per_slide -Minimum 1 -Maximum 100 -Label 'max_effects_per_slide'
  }

  $slidePlans = [System.Collections.Generic.List[object]]::new()
  $slideNumbers = [System.Collections.Generic.HashSet[int]]::new()
  foreach ($slidePlan in @($storyboard.slides)) {
    Assert-Object -Value $slidePlan -Label 'slide plan'
    Assert-NoUnknownProperties -Object $slidePlan -Allowed @('slide', 'transition', 'beats') -Label 'STORYBOARD_SLIDE'
    foreach ($requiredProperty in @('slide', 'transition', 'beats')) {
      if (-not (Has-Property -Object $slidePlan -Name $requiredProperty)) { throw "STORYBOARD_SLIDE_PROPERTY_MISSING:$requiredProperty" }
    }
    $slideNumber = ConvertTo-StrictInteger -Value $slidePlan.slide -Minimum 1 -Maximum 100000 -Label 'slide'
    if (-not $slideNumbers.Add($slideNumber)) { throw "STORYBOARD_DUPLICATE_SLIDE:$slideNumber" }
    $transitionName = [string]$slidePlan.transition
    if (-not $transitionMap.ContainsKey($transitionName)) { throw "UNKNOWN_TRANSITION:$transitionName" }
    Assert-Array -Value $slidePlan.beats -Label "beats[$slideNumber]"
    $shapeNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    $effectCount = 0
    $validatedBeats = [System.Collections.Generic.List[object]]::new()
    foreach ($beat in @($slidePlan.beats)) {
      Assert-Object -Value $beat -Label "beat[$slideNumber]"
      Assert-NoUnknownProperties -Object $beat -Allowed @('shape_names', 'effect', 'trigger', 'duration', 'delay', 'narrative_purpose') -Label "STORYBOARD_BEAT"
      foreach ($requiredProperty in @('shape_names', 'effect', 'trigger', 'duration', 'delay', 'narrative_purpose')) {
        if (-not (Has-Property -Object $beat -Name $requiredProperty)) { throw "STORYBOARD_BEAT_PROPERTY_MISSING:${requiredProperty}:slide=$slideNumber" }
      }
      Assert-Array -Value $beat.shape_names -Label "shape_names[$slideNumber]" -Minimum 1
      $validatedShapeNames = [System.Collections.Generic.List[string]]::new()
      foreach ($shapeNameValue in @($beat.shape_names)) {
        if ($shapeNameValue -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$shapeNameValue)) { throw "INVALID_SHAPE_NAME:slide=$slideNumber" }
        $shapeName = ([string]$shapeNameValue).Trim()
        if (-not $shapeNames.Add($shapeName)) { throw "DUPLICATE_MOTION_SHAPE:slide=$slideNumber;shape=$shapeName" }
        $validatedShapeNames.Add($shapeName)
        $effectCount += 1
      }
      $effectName = [string]$beat.effect
      $triggerName = [string]$beat.trigger
      if (-not $effectMap.ContainsKey($effectName)) { throw "UNKNOWN_EFFECT:$effectName:slide=$slideNumber" }
      if (-not $triggerMap.ContainsKey($triggerName)) { throw "UNKNOWN_TRIGGER:$triggerName:slide=$slideNumber" }
      $duration = ConvertTo-StrictFiniteNumber -Value $beat.duration -Minimum 0.001 -Maximum 10 -Label "duration:slide=$slideNumber"
      $delay = ConvertTo-StrictFiniteNumber -Value $beat.delay -Minimum 0 -Maximum 10 -Label "delay:slide=$slideNumber"
      if ([string]::IsNullOrWhiteSpace([string]$beat.narrative_purpose)) { throw "STORYBOARD_BEAT_NARRATIVE_PURPOSE_EMPTY:slide=$slideNumber" }
      $validatedBeats.Add([ordered]@{ shape_names = @($validatedShapeNames); effect = $effectName; trigger = $triggerName; duration = $duration; delay = $delay; narrative_purpose = ([string]$beat.narrative_purpose).Trim() })
    }
    if ($effectCount -gt $maximumEffects) { throw "EFFECT_COUNT_EXCEEDS_LIMIT:slide=$slideNumber;count=$effectCount;limit=$maximumEffects" }
    $slidePlans.Add([ordered]@{ slide = $slideNumber; transition = $transitionName; beats = @($validatedBeats); effect_count = $effectCount })
  }

  [System.IO.File]::Copy($resolvedInput, $resolvedOutput, $false)
  $outputCreated = $true
  [void](Assert-RegularFilePath -Path $resolvedOutput -Label 'MOTION_OUTPUT')
  if ((Get-FileHash -LiteralPath $resolvedOutput -Algorithm SHA256).Hash.ToLowerInvariant() -ne $sourceHashBefore) { throw 'MOTION_COPY_HASH_MISMATCH' }

  $powerPoint = New-Object -ComObject PowerPoint.Application
  Set-PowerPointSafeAutomation -Application $powerPoint
  $presentation = $powerPoint.Presentations.Open($resolvedOutput, $msoFalse, $msoFalse, $msoFalse)
  $slideCount = [int]$presentation.Slides.Count
  if ($slideCount -lt 1) { throw 'DECK_CONTAINS_NO_SLIDES' }
  $expectedSlideNumbers = [System.Collections.Generic.HashSet[int]]::new()
  for ($expectedSlide = 1; $expectedSlide -le $slideCount; $expectedSlide += 1) { [void]$expectedSlideNumbers.Add($expectedSlide) }
  $missingSlides = @($expectedSlideNumbers | Where-Object { -not $slideNumbers.Contains([int]$_) })
  $extraSlides = @($slideNumbers | Where-Object { $_ -gt $slideCount })
  if ($missingSlides.Count -gt 0) { throw "STORYBOARD_MISSING_SLIDES:$($missingSlides -join ',')" }
  if ($extraSlides.Count -gt 0) { throw "STORYBOARD_SLIDES_OUT_OF_RANGE:$($extraSlides -join ',')" }

  foreach ($slidePlan in @($slidePlans)) {
    $slide = $null
    try {
      $slide = $presentation.Slides.Item([int]$slidePlan.slide)
      foreach ($beat in @($slidePlan.beats)) {
        foreach ($shapeName in @($beat.shape_names)) {
          $shape = $null
          try { $shape = $slide.Shapes.Item([string]$shapeName) } catch { throw "STORYBOARD_SHAPE_NOT_FOUND:slide=$($slidePlan.slide);shape=$shapeName" } finally { Release-ComObject -Object $shape }
        }
      }
    } finally { Release-ComObject -Object $slide }
  }

  $slidesReport = [System.Collections.Generic.List[object]]::new()
  foreach ($slidePlan in @($slidePlans | Sort-Object slide)) {
    $slide = $null
    $sequence = $null
    $transition = $null
    try {
      $slide = $presentation.Slides.Item([int]$slidePlan.slide)
      $sequence = $slide.TimeLine.MainSequence
      if ($storyboard.replace_existing) { while ($sequence.Count -gt 0) { $sequence.Item(1).Delete() } }
      $existingEffectCount = if ($storyboard.replace_existing) { 0 } else { [int]$sequence.Count }
      if ($existingEffectCount + [int]$slidePlan.effect_count -gt $maximumEffects) { throw "EFFECT_COUNT_EXCEEDS_LIMIT_WITH_EXISTING:slide=$($slidePlan.slide)" }
      $transition = $slide.SlideShowTransition
      $transition.AdvanceOnClick = $msoTrue
      $transition.AdvanceOnTime = $msoFalse
      $transition.EntryEffect = $transitionMap[[string]$slidePlan.transition]
      $effectCount = 0
      foreach ($beat in @($slidePlan.beats)) {
        foreach ($shapeName in @($beat.shape_names)) {
          $shape = $null
          $effect = $null
          try {
            $shape = $slide.Shapes.Item([string]$shapeName)
            $effect = $sequence.AddEffect($shape, $effectMap[[string]$beat.effect], $msoAnimateLevelNone, $triggerMap[[string]$beat.trigger])
            $effect.Timing.Duration = [double]$beat.duration
            $effect.Timing.TriggerDelayTime = [double]$beat.delay
            try { $effect.Timing.SmoothStart = $msoTrue } catch {}
            try { $effect.Timing.SmoothEnd = $msoTrue } catch {}
            $effectCount += 1
          } finally {
            Release-ComObject -Object $effect
            Release-ComObject -Object $shape
          }
        }
      }
      $slidesReport.Add([ordered]@{ slide = [int]$slidePlan.slide; transition = [string]$slidePlan.transition; effects = $effectCount; advance_on_click = $true; advance_on_time = $false })
    } finally {
      Release-ComObject -Object $transition
      Release-ComObject -Object $sequence
      Release-ComObject -Object $slide
    }
  }
  $presentation.Save()
  $presentation.Close()
  Release-ComObject -Object $presentation
  $presentation = $null
  $resolvedInput = Assert-RegularFilePath -Path $resolvedInput -Label 'MOTION_INPUT_RECHECK'
  $resolvedStoryboard = Assert-RegularFilePath -Path $resolvedStoryboard -Label 'STORYBOARD_RECHECK'
  $resolvedStaticCertificate = Assert-RegularFilePath -Path $resolvedStaticCertificate -Label 'STATIC_CERTIFICATE_RECHECK'
  $resolvedOutput = Assert-RegularFilePath -Path $resolvedOutput -Label 'MOTION_OUTPUT_RECHECK'
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedInput -Algorithm SHA256).Hash.ToLowerInvariant()
  $storyboardHashAfter = (Get-FileHash -LiteralPath $resolvedStoryboard -Algorithm SHA256).Hash.ToLowerInvariant()
  $staticCertificateHashAfter = (Get-FileHash -LiteralPath $resolvedStaticCertificate -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_MOTION' }
  if ($storyboardHashBefore -ne $storyboardHashAfter) { throw 'STORYBOARD_CHANGED_DURING_MOTION' }
  if ($staticCertificateHashBefore -ne $staticCertificateHashAfter) { throw 'STATIC_CERTIFICATE_CHANGED_DURING_MOTION' }
  $staticCertificateAfter = Read-JsonFile -Path $resolvedStaticCertificate
  Assert-StaticCertificate -Certificate $staticCertificateAfter -InputDeck $resolvedInput -InputHash $sourceHashAfter
  $outputHash = (Get-FileHash -LiteralPath $resolvedOutput -Algorithm SHA256).Hash.ToLowerInvariant()
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = 'PASS'
    input_path = $resolvedInput
    output_path = $resolvedOutput
    storyboard_path = $resolvedStoryboard
    static_certification_path = $resolvedStaticCertificate
    input_sha256_before = $sourceHashBefore
    input_sha256_after = $sourceHashAfter
    storyboard_sha256_before = $storyboardHashBefore
    storyboard_sha256_after = $storyboardHashAfter
    static_certificate_sha256_before = $staticCertificateHashBefore
    static_certificate_sha256_after = $staticCertificateHashAfter
    output_sha256 = $outputHash
    slide_count = $slideCount
    max_effects_per_slide = $maximumEffects
    slides = @($slidesReport)
  }
  Write-JsonFileNew -Value $report -Path $resolvedReport
  $report | ConvertTo-Json -Depth 30
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isUnverified = $message -match '(?i)(COM|PowerPoint|RPC|class not registered|automation|could not be opened)'
  if ($outputCreated -and (Test-Path -LiteralPath $resolvedOutput -PathType Leaf)) {
    try {
      $outputItem = Get-Item -LiteralPath $resolvedOutput -Force -ErrorAction Stop
      if (($outputItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) { [System.IO.File]::Delete($resolvedOutput) }
    } catch {}
  }
  $failure = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = if ($isUnverified) { 'UNVERIFIED' } else { 'BLOCKED' }
    input_path = if ($resolvedInput) { $resolvedInput } else { $InputPath }
    output_path = if ($resolvedOutput) { $resolvedOutput } else { $OutputPath }
    storyboard_path = if ($resolvedStoryboard) { $resolvedStoryboard } else { $StoryboardPath }
    static_certification_path = if ($resolvedStaticCertificate) { $resolvedStaticCertificate } else { $StaticCertificationPath }
    error = $message
  }
  if ($sourceHashBefore) { $failure.input_sha256_before = $sourceHashBefore }
  if ($sourceHashAfter) { $failure.input_sha256_after = $sourceHashAfter }
  if ($resolvedReport -and -not (Test-Path -LiteralPath $resolvedReport)) { Write-JsonFileNew -Value $failure -Path $resolvedReport }
  [Console]::Error.WriteLine($message)
  exit $(if ($isUnverified) { 3 } else { 2 })
} finally {
  if ($presentation) { try { $presentation.Close() } catch {}; Release-ComObject -Object $presentation }
  if ($powerPoint) { try { $powerPoint.Quit() } catch {}; Release-ComObject -Object $powerPoint }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
