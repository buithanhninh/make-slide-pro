param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$MinimumQualityScore = '97',
  [string]$MinimumDomainScore = '90'
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$policyMinimumQualityScore = 97.0
$policyMinimumDomainScore = 90.0
$qualityScoreFormulaVersion = 'WEIGHTED_DOMAIN_V1'
$sourceHashFormulaVersion = 'SOURCE_FILE_SHA256_OR_SET_V1'
$qualityScoreTolerance = 0.05
$receiptFutureSkewSeconds = 300
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
$finalRequiredDomains = @(
  'source_integrity',
  'content_fidelity',
  'data_accuracy',
  'narrative_logic',
  'visual_design',
  'layout_typography',
  'charts_tables',
  'images_icons',
  'motion',
  'native_compatibility'
)
$staticRequiredDomains = @($finalRequiredDomains | Where-Object { $_ -ne 'motion' })
$finalRequiredEvidence = @(
  'source_hash_unchanged',
  'mandatory_capabilities_verified',
  'all_slides_rendered',
  'all_slides_reviewed',
  'all_data_validated',
  'all_changes_documented',
  'blueprint_coverage_verified',
  'visual_assets_verified',
  'contrast_verified',
  'icon_consistency_verified',
  'motion_verified',
  'source_traceability_verified',
  'static_motion_equivalent',
  'fresh_powerpoint_open'
)
$staticRequiredEvidence = @($finalRequiredEvidence | Where-Object { $_ -notin @('motion_verified', 'static_motion_equivalent') })
$certificationProfile = 'FINAL_RELEASE_MOTION'
$requiredDomains = @($finalRequiredDomains)
$requiredEvidence = @($finalRequiredEvidence)
$receiptEvidence = @($requiredEvidence | Where-Object { $_ -ne 'source_hash_unchanged' })
$hashPattern = '^[0-9a-fA-F]{64}$'
$resolvedInputPath = Get-NormalizedFullPath -Path $InputPath
$resolvedOutputPath = Get-NormalizedFullPath -Path $OutputPath

function Has-Property {
  param([Parameter(Mandatory = $true)][object]$Object, [Parameter(Mandatory = $true)][string]$Name)
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Add-UnknownFields {
  param(
    [Parameter(Mandatory = $true)][object]$Object,
    [Parameter(Mandatory = $true)][string[]]$AllowedFields,
    [Parameter(Mandatory = $true)][string]$ErrorPrefix,
    [Parameter(Mandatory = $true)][AllowEmptyCollection()][System.Collections.Generic.List[string]]$Failures
  )
  $allowed = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
  foreach ($fieldName in $AllowedFields) { [void]$allowed.Add($fieldName) }
  foreach ($property in $Object.PSObject.Properties) {
    if (-not $allowed.Contains([string]$property.Name)) { $Failures.Add("${ErrorPrefix}$($property.Name)") }
  }
}

function Get-ZeroDomainScores {
  param([string[]]$Domains = $requiredDomains)
  $scores = [ordered]@{}
  foreach ($domain in $Domains) { $scores[$domain] = 0 }
  return $scores
}

function ConvertTo-FiniteScore {
  param([object]$Value, [ref]$Parsed)
  if ($null -eq $Value -or $Value -is [bool] -or $Value -is [string]) { return $false }
  $candidate = 0.0
  $valid = [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate)
  if (-not $valid -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or $candidate -lt 0 -or $candidate -gt 100) { return $false }
  $Parsed.Value = $candidate
  return $true
}

function ConvertTo-FiniteThreshold {
  param([string]$Value, [ref]$Parsed)
  $candidate = 0.0
  $valid = [double]::TryParse($Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate)
  if (-not $valid -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or $candidate -lt 0 -or $candidate -gt 100) { return $false }
  $Parsed.Value = $candidate
  return $true
}

function Get-CalculatedQualityScore {
  param(
    [Parameter(Mandatory = $true)][object]$Scores,
    [Parameter(Mandatory = $true)][string[]]$Domains
  )
  $weightedTotal = 0.0
  $weightTotal = 0.0
  foreach ($domain in $Domains) {
    $weight = [double]$qualityScoreWeights[$domain]
    $weightedTotal += ([double]$Scores[$domain]) * $weight
    $weightTotal += $weight
  }
  if ($weightTotal -le 0) { return 0.0 }
  return [Math]::Round($weightedTotal / $weightTotal, 4, [MidpointRounding]::AwayFromZero)
}

function Get-SourceSetHash {
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

$requestedQualityThreshold = 0.0
$requestedDomainThreshold = 0.0
$qualityThresholdValid = ConvertTo-FiniteThreshold -Value $MinimumQualityScore -Parsed ([ref]$requestedQualityThreshold)
$domainThresholdValid = ConvertTo-FiniteThreshold -Value $MinimumDomainScore -Parsed ([ref]$requestedDomainThreshold)
$effectiveQualityThreshold = if ($qualityThresholdValid) { [Math]::Max($policyMinimumQualityScore, $requestedQualityThreshold) } else { $policyMinimumQualityScore }
$effectiveDomainThreshold = if ($domainThresholdValid) { [Math]::Max($policyMinimumDomainScore, $requestedDomainThreshold) } else { $policyMinimumDomainScore }

function New-FallbackCertificate {
  param([Parameter(Mandatory = $true)][string]$ErrorMessage)
  $safeMessage = ($ErrorMessage -replace '[\r\n]+', ' ').Trim()
  return [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    certification_profile = $certificationProfile
    status = 'BLOCKED'
    quality_score = 0
    calculated_quality_score = 0
    domain_scores = Get-ZeroDomainScores -Domains $requiredDomains
    source_hash_unchanged = $false
    source_hash_before = ('0' * 64)
    source_hash_after = ('0' * 64)
    source_bindings = @()
    output_sha256 = ('0' * 64)
    output_path = 'UNAVAILABLE'
    output_detected_format = 'UNKNOWN'
    required_domains = $requiredDomains
    required_evidence = $requiredEvidence
    evidence_receipts = [ordered]@{}
    findings = @()
    failed_requirements = @('RELEASE_INPUT_UNREADABLE:' + $safeMessage)
    blocking_requirements = @('RELEASE_INPUT_UNREADABLE:' + $safeMessage)
    unverified_requirements = @()
    certification_rules = [ordered]@{
      minimum_quality_score = $effectiveQualityThreshold
      minimum_domain_score = $effectiveDomainThreshold
      policy_minimum_quality_score = $policyMinimumQualityScore
      policy_minimum_domain_score = $policyMinimumDomainScore
      maximum_p0_findings = 0
      maximum_p1_findings = 0
      source_hash_formula = $sourceHashFormulaVersion
      quality_score_formula = $qualityScoreFormulaVersion
      quality_score_tolerance = $qualityScoreTolerance
      domain_weights = $qualityScoreWeights
    }
    error = $safeMessage
  }
}

if (Test-PathsEqual -FirstPath $resolvedInputPath -SecondPath $resolvedOutputPath) {
  [Console]::Error.WriteLine('Release certificate output cannot overwrite release input.')
  exit 2
}
if (Test-Path -LiteralPath $resolvedOutputPath) {
  [Console]::Error.WriteLine("RELEASE_CERTIFICATE_OUTPUT_ALREADY_EXISTS:$resolvedOutputPath")
  exit 2
}
try {
  [void](Assert-RegularFilePath -Path $resolvedInputPath -Label 'RELEASE_INPUT')
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutputPath))
} catch {
  [Console]::Error.WriteLine($_.Exception.Message)
  exit 2
}

try {
  $releaseInputHashBefore = (Get-FileHash -LiteralPath $resolvedInputPath -Algorithm SHA256).Hash.ToLowerInvariant()
  $releaseInput = Read-JsonFile -Path $resolvedInputPath
  if ($null -eq $releaseInput -or $releaseInput -is [System.Array] -or $releaseInput -is [string] -or $releaseInput -is [ValueType]) {
    throw 'RELEASE_INPUT_MUST_BE_OBJECT'
  }

  $blocked = [System.Collections.Generic.List[string]]::new()
  $unverified = [System.Collections.Generic.List[string]]::new()
  $profileProperty = $releaseInput.PSObject.Properties['certification_profile']
  if ($null -eq $profileProperty -or $profileProperty.Value -isnot [string] -or [string]$profileProperty.Value -notin @('STATIC_READY_FOR_MOTION', 'FINAL_RELEASE_STATIC', 'FINAL_RELEASE_MOTION')) {
    $blocked.Add('INVALID_CERTIFICATION_PROFILE')
  } else {
    $certificationProfile = [string]$profileProperty.Value
  }
  if ($certificationProfile -in @('STATIC_READY_FOR_MOTION', 'FINAL_RELEASE_STATIC')) {
    $requiredDomains = @($staticRequiredDomains)
    $requiredEvidence = @($staticRequiredEvidence)
  } else {
    $requiredDomains = @($finalRequiredDomains)
    $requiredEvidence = @($finalRequiredEvidence)
  }
  $receiptEvidence = @($requiredEvidence | Where-Object { $_ -ne 'source_hash_unchanged' })
  $allowedReleaseFields = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
  foreach ($fieldName in @(
    'certification_profile', 'source_bindings', 'source_hash_before', 'source_hash_after', 'output_sha256', 'output_path',
    'quality_score', 'domain_scores', 'findings', 'evidence_receipts', 'macro_review_verified'
  ) + $finalRequiredEvidence) { [void]$allowedReleaseFields.Add([string]$fieldName) }
  foreach ($property in $releaseInput.PSObject.Properties) {
    if (-not $allowedReleaseFields.Contains([string]$property.Name)) { $blocked.Add("UNKNOWN_RELEASE_FIELD:$($property.Name)") }
  }
  if ($certificationProfile -in @('STATIC_READY_FOR_MOTION', 'FINAL_RELEASE_STATIC')) {
    foreach ($forbiddenField in @('motion_verified', 'static_motion_equivalent')) {
      if (Has-Property -Object $releaseInput -Name $forbiddenField) { $blocked.Add("FIELD_NOT_ALLOWED_FOR_PROFILE:$forbiddenField") }
    }
  }
  if (-not $qualityThresholdValid -or -not $domainThresholdValid) {
    $blocked.Add('INVALID_CERTIFICATION_THRESHOLD')
  }
  if (($qualityThresholdValid -and $requestedQualityThreshold -lt $policyMinimumQualityScore) -or ($domainThresholdValid -and $requestedDomainThreshold -lt $policyMinimumDomainScore)) {
    $blocked.Add('CERTIFICATION_THRESHOLD_CANNOT_BE_LOWERED')
  }

  foreach ($evidenceName in $requiredEvidence) {
    $property = $releaseInput.PSObject.Properties[$evidenceName]
    if ($null -eq $property -or $property.Value -isnot [bool] -or -not [bool]$property.Value) {
      $unverified.Add("MISSING_OR_FAILED_EVIDENCE:$evidenceName")
    }
  }

  $sourceHashBefore = if (Has-Property -Object $releaseInput -Name 'source_hash_before') { [string]$releaseInput.source_hash_before } else { '' }
  $sourceHashAfter = if (Has-Property -Object $releaseInput -Name 'source_hash_after') { [string]$releaseInput.source_hash_after } else { '' }
  $outputSha256 = if (Has-Property -Object $releaseInput -Name 'output_sha256') { [string]$releaseInput.output_sha256 } else { '' }
  $boundOutputPath = if (Has-Property -Object $releaseInput -Name 'output_path') { [string]$releaseInput.output_path } else { '' }

  foreach ($hashBinding in @(
    [ordered]@{ name = 'source_hash_before'; value = $sourceHashBefore },
    [ordered]@{ name = 'source_hash_after'; value = $sourceHashAfter },
    [ordered]@{ name = 'output_sha256'; value = $outputSha256 }
  )) {
    if ([string]::IsNullOrWhiteSpace([string]$hashBinding.value)) {
      $blocked.Add("MISSING_RELEASE_BINDING:$($hashBinding.name)")
    } elseif ([string]$hashBinding.value -notmatch $hashPattern) {
      $blocked.Add("INVALID_RELEASE_BINDING:$($hashBinding.name)")
    }
  }
  if ([string]::IsNullOrWhiteSpace($boundOutputPath)) { $blocked.Add('MISSING_RELEASE_BINDING:output_path') }

  $sourceHashUnchanged = $false
  if (-not (Has-Property -Object $releaseInput -Name 'source_hash_unchanged') -or $releaseInput.source_hash_unchanged -isnot [bool]) {
    $blocked.Add('INVALID_RELEASE_FIELD:source_hash_unchanged')
  } else {
    $sourceHashUnchanged = [bool]$releaseInput.source_hash_unchanged
    if (-not $sourceHashUnchanged) { $blocked.Add('SOURCE_HASH_CHANGED') }
  }
  if ($sourceHashBefore -match $hashPattern -and $sourceHashAfter -match $hashPattern -and $sourceHashBefore -ine $sourceHashAfter) {
    $blocked.Add('SOURCE_HASH_CHANGED')
  }

  $resolvedBoundOutput = $null
  if (-not [string]::IsNullOrWhiteSpace($boundOutputPath)) {
    try { $resolvedBoundOutput = Get-NormalizedFullPath -Path $boundOutputPath } catch { $blocked.Add('INVALID_RELEASE_BINDING:output_path') }
  }

  $verifiedSourceBindings = [System.Collections.Generic.List[object]]::new()
  if (-not (Has-Property -Object $releaseInput -Name 'source_bindings') -or $null -eq $releaseInput.source_bindings) {
    $blocked.Add('SOURCE_BINDINGS_MISSING')
  } else {
    $sourceBindings = @($releaseInput.source_bindings)
    if ($sourceBindings.Count -eq 0) {
      $blocked.Add('SOURCE_BINDINGS_MISSING')
    } else {
      $sourceIds = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
      $sourcePaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
      foreach ($binding in $sourceBindings) {
        if ($null -eq $binding -or $binding -is [string] -or $binding -is [ValueType]) {
          $blocked.Add('MALFORMED_SOURCE_BINDING')
          continue
        }
        $sourceId = if (Has-Property -Object $binding -Name 'source_id') { [string]$binding.source_id } else { '' }
        $sourcePath = if (Has-Property -Object $binding -Name 'path') { [string]$binding.path } else { '' }
        $shaBefore = if (Has-Property -Object $binding -Name 'sha256_before') { [string]$binding.sha256_before } else { '' }
        $shaAfter = if (Has-Property -Object $binding -Name 'sha256_after') { [string]$binding.sha256_after } else { '' }
        Add-UnknownFields -Object $binding -AllowedFields @('source_id', 'path', 'sha256_before', 'sha256_after') -ErrorPrefix "UNKNOWN_SOURCE_BINDING_FIELD:${sourceId}:" -Failures $blocked
        if ([string]::IsNullOrWhiteSpace($sourceId) -or [string]::IsNullOrWhiteSpace($sourcePath) -or $shaBefore -notmatch $hashPattern -or $shaAfter -notmatch $hashPattern) {
          $blocked.Add('MALFORMED_SOURCE_BINDING')
          continue
        }
        if (-not $sourceIds.Add($sourceId)) { $blocked.Add("DUPLICATE_SOURCE_BINDING_ID:$sourceId") }
        $resolvedSourcePath = $null
        try {
          $resolvedSourcePath = Assert-RegularFilePath -Path $sourcePath -Label 'SOURCE_FILE'
        } catch {
          $sourcePathError = [string]$_.Exception.Message
          if ($sourcePathError -like 'PATH_REPARSE_POINT_NOT_ALLOWED:*' -or $sourcePathError -like 'SOURCE_FILE_REPARSE_POINT_NOT_ALLOWED:*') {
            $blocked.Add("SOURCE_REPARSE_POINT_NOT_ALLOWED:$sourceId")
          } elseif ($sourcePathError -like 'SOURCE_FILE_MISSING:*') {
            $blocked.Add("SOURCE_FILE_MISSING:$sourceId")
          } else {
            $blocked.Add("INVALID_SOURCE_PATH:$sourceId")
          }
          continue
        }
        if (-not $sourcePaths.Add($resolvedSourcePath)) { $blocked.Add("DUPLICATE_SOURCE_BINDING_PATH:$sourceId") }
        if (Test-PathsEqual -FirstPath $resolvedSourcePath -SecondPath $resolvedInputPath) { $blocked.Add("SOURCE_PATH_COLLIDES_WITH_RELEASE_INPUT:$sourceId") }
        if ($resolvedBoundOutput -and (Test-PathsEqual -FirstPath $resolvedSourcePath -SecondPath $resolvedBoundOutput)) { $blocked.Add("SOURCE_PATH_COLLIDES_WITH_OUTPUT:$sourceId") }
        $actualSourceHash = (Get-FileHash -LiteralPath $resolvedSourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($shaBefore -ine $shaAfter) { $blocked.Add('SOURCE_HASH_CHANGED') }
        if ($actualSourceHash -ine $shaBefore -or $actualSourceHash -ine $shaAfter) { $blocked.Add('SOURCE_HASH_MISMATCH') }
        $verifiedSourceBindings.Add([ordered]@{
          source_id = $sourceId
          path = $resolvedSourcePath
          sha256_before = $shaBefore.ToLowerInvariant()
          sha256_after = $shaAfter.ToLowerInvariant()
          actual_sha256 = $actualSourceHash
        })
      }
      if ($verifiedSourceBindings.Count -eq $sourceBindings.Count) {
        $calculatedSourceSetHash = Get-SourceSetHash -Bindings @($verifiedSourceBindings)
        if (($sourceHashBefore -match $hashPattern -and $sourceHashBefore -ine $calculatedSourceSetHash) -or ($sourceHashAfter -match $hashPattern -and $sourceHashAfter -ine $calculatedSourceSetHash)) {
          $blocked.Add('SOURCE_SET_HASH_MISMATCH')
          if ($sourceBindings.Count -eq 1) { $blocked.Add('SOURCE_HASH_MISMATCH') }
        }
      }
    }
  }

  $submittedQualityScore = 0.0
  if (-not (Has-Property -Object $releaseInput -Name 'quality_score')) {
    $blocked.Add('MISSING_RELEASE_FIELD:quality_score')
  } elseif (-not (ConvertTo-FiniteScore -Value $releaseInput.quality_score -Parsed ([ref]$submittedQualityScore))) {
    $blocked.Add('INVALID_RELEASE_FIELD:quality_score')
  }

  $domainScores = Get-ZeroDomainScores -Domains $requiredDomains
  $domainScoresValid = (Has-Property -Object $releaseInput -Name 'domain_scores') -and $null -ne $releaseInput.domain_scores -and $releaseInput.domain_scores -isnot [System.Array] -and $releaseInput.domain_scores -isnot [string] -and $releaseInput.domain_scores -isnot [ValueType]
  $allDomainScoresParsed = $domainScoresValid
  if (-not $domainScoresValid) {
    $blocked.Add('INVALID_RELEASE_FIELD:domain_scores')
  } else {
    Add-UnknownFields -Object $releaseInput.domain_scores -AllowedFields $requiredDomains -ErrorPrefix 'UNKNOWN_DOMAIN_SCORE:' -Failures $blocked
    foreach ($domain in $requiredDomains) {
      $property = $releaseInput.domain_scores.PSObject.Properties[$domain]
      if ($null -eq $property) {
        $blocked.Add("MISSING_DOMAIN_SCORE:$domain")
        $allDomainScoresParsed = $false
        continue
      }
      $parsedDomain = 0.0
      if (-not (ConvertTo-FiniteScore -Value $property.Value -Parsed ([ref]$parsedDomain))) {
        $blocked.Add("INVALID_DOMAIN_SCORE:$domain")
        $allDomainScoresParsed = $false
        continue
      }
      $domainScores[$domain] = $parsedDomain
      if ($parsedDomain -lt $effectiveDomainThreshold) { $blocked.Add("DOMAIN_SCORE_BELOW_THRESHOLD:$domain") }
    }
  }
  $calculatedQualityScore = 0.0
  if ($allDomainScoresParsed) {
    $calculatedQualityScore = Get-CalculatedQualityScore -Scores $domainScores -Domains $requiredDomains
    if ($calculatedQualityScore -lt $effectiveQualityThreshold) { $blocked.Add('QUALITY_SCORE_BELOW_THRESHOLD') }
    if ((Has-Property -Object $releaseInput -Name 'quality_score') -and [Math]::Abs($submittedQualityScore - $calculatedQualityScore) -gt $qualityScoreTolerance) {
      $blocked.Add('QUALITY_SCORE_FORMULA_MISMATCH')
    }
  }

  $findings = @()
  if (-not (Has-Property -Object $releaseInput -Name 'findings') -or $null -eq $releaseInput.findings -or $releaseInput.findings -isnot [System.Array]) {
    $blocked.Add('INVALID_RELEASE_FIELD:findings')
  } else {
    $findings = @($releaseInput.findings)
  }
  foreach ($finding in $findings) {
    if ($null -eq $finding -or $finding -is [string] -or $finding -is [ValueType] -or -not (Has-Property -Object $finding -Name 'severity') -or -not (Has-Property -Object $finding -Name 'code') -or -not (Has-Property -Object $finding -Name 'detail')) {
      $blocked.Add('MALFORMED_FINDING_RECORD')
      continue
    }
    $severity = [string]$finding.severity
    $code = [string]$finding.code
    $detail = [string]$finding.detail
    if ($severity -notin @('P0', 'P1', 'P2', 'P3', 'INFO')) { $blocked.Add("INVALID_FINDING_SEVERITY:$severity") }
    if ([string]::IsNullOrWhiteSpace($code) -or [string]::IsNullOrWhiteSpace($detail)) { $blocked.Add('MALFORMED_FINDING_RECORD') }
    if ($severity -in @('P0', 'P1')) { $blocked.Add('P0_P1_FINDINGS_REMAIN') }
  }

  $outputDetectedFormat = 'UNKNOWN'
  $actualOutputHash = ''
  $outputLastWriteUtc = $null
  if ($resolvedBoundOutput -and $outputSha256 -match $hashPattern) {
    try {
      $resolvedBoundOutput = Assert-RegularFilePath -Path $resolvedBoundOutput -Label 'OUTPUT_FILE'
    } catch {
      $outputPathError = [string]$_.Exception.Message
      if ($outputPathError -like 'PATH_REPARSE_POINT_NOT_ALLOWED:*' -or $outputPathError -like 'OUTPUT_FILE_REPARSE_POINT_NOT_ALLOWED:*') {
        $blocked.Add('OUTPUT_REPARSE_POINT_NOT_ALLOWED')
      } elseif ($outputPathError -like 'OUTPUT_FILE_MISSING:*') {
        $blocked.Add('OUTPUT_FILE_MISSING')
      } else {
        $blocked.Add('INVALID_RELEASE_BINDING:output_path')
      }
      $resolvedBoundOutput = $null
    }
    if ($resolvedBoundOutput) {
      $outputLastWriteUtc = [DateTimeOffset](Get-Item -LiteralPath $resolvedBoundOutput -Force -ErrorAction Stop).LastWriteTimeUtc
      $actualOutputHash = (Get-FileHash -LiteralPath $resolvedBoundOutput -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($actualOutputHash -ine $outputSha256) { $blocked.Add('OUTPUT_HASH_MISMATCH') }
      $outputDetectedFormat = Get-DetectedFileFormat -Path $resolvedBoundOutput
      if ($outputDetectedFormat -notin @('PPTX', 'PPTM', 'PPT', 'ODP')) { $blocked.Add("OUTPUT_FORMAT_NOT_PRESENTATION:$outputDetectedFormat") }
      $expectedOutputFormats = @(Get-ExpectedFormatsForExtension -Extension ([System.IO.Path]::GetExtension($resolvedBoundOutput)))
      if ($expectedOutputFormats.Count -eq 0 -or $outputDetectedFormat -notin $expectedOutputFormats) { $blocked.Add('OUTPUT_SIGNATURE_EXTENSION_MISMATCH') }
      if ($outputDetectedFormat -eq 'PPTM' -and (-not (Has-Property -Object $releaseInput -Name 'macro_review_verified') -or $releaseInput.macro_review_verified -isnot [bool] -or -not [bool]$releaseInput.macro_review_verified)) {
        $blocked.Add('MACRO_OUTPUT_REQUIRES_EXPLICIT_SAFE_HANDLING')
      }
    }
  }

  $verifiedEvidenceReceipts = [ordered]@{}
  $receiptPaths = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
  $receiptContainerValid = (Has-Property -Object $releaseInput -Name 'evidence_receipts') -and $null -ne $releaseInput.evidence_receipts -and $releaseInput.evidence_receipts -isnot [System.Array] -and $releaseInput.evidence_receipts -isnot [string] -and $releaseInput.evidence_receipts -isnot [ValueType]
  if (-not $receiptContainerValid) {
    $unverified.Add('EVIDENCE_RECEIPTS_MISSING')
  } else {
    Add-UnknownFields -Object $releaseInput.evidence_receipts -AllowedFields $receiptEvidence -ErrorPrefix 'UNKNOWN_EVIDENCE_RECEIPT:' -Failures $blocked
    foreach ($evidenceName in $receiptEvidence) {
      $resolvedReceiptSubjectPath = $null
      $receiptProperty = $releaseInput.evidence_receipts.PSObject.Properties[$evidenceName]
      if ($null -eq $receiptProperty -or $null -eq $receiptProperty.Value -or $receiptProperty.Value -is [string] -or $receiptProperty.Value -is [ValueType]) {
        $unverified.Add("EVIDENCE_RECEIPT_MISSING:$evidenceName")
        continue
      }
      $binding = $receiptProperty.Value
      Add-UnknownFields -Object $binding -AllowedFields @('path', 'sha256') -ErrorPrefix "UNKNOWN_EVIDENCE_RECEIPT_BINDING_FIELD:${evidenceName}:" -Failures $blocked
      $receiptPath = if (Has-Property -Object $binding -Name 'path') { [string]$binding.path } else { '' }
      $receiptHash = if (Has-Property -Object $binding -Name 'sha256') { [string]$binding.sha256 } else { '' }
      if ([string]::IsNullOrWhiteSpace($receiptPath) -or $receiptHash -notmatch $hashPattern) {
        $blocked.Add("MALFORMED_EVIDENCE_RECEIPT_BINDING:$evidenceName")
        continue
      }
      $resolvedReceiptPath = $null
      try {
        $resolvedReceiptPath = Assert-RegularFilePath -Path $receiptPath -Label 'EVIDENCE_RECEIPT_FILE'
      } catch {
        $receiptPathError = [string]$_.Exception.Message
        if ($receiptPathError -like 'PATH_REPARSE_POINT_NOT_ALLOWED:*' -or $receiptPathError -like 'EVIDENCE_RECEIPT_FILE_REPARSE_POINT_NOT_ALLOWED:*') {
          $blocked.Add("EVIDENCE_RECEIPT_REPARSE_POINT:$evidenceName")
        } elseif ($receiptPathError -like 'EVIDENCE_RECEIPT_FILE_MISSING:*') {
          $unverified.Add("EVIDENCE_RECEIPT_FILE_MISSING:$evidenceName")
        } else {
          $blocked.Add("INVALID_EVIDENCE_RECEIPT_PATH:$evidenceName")
        }
        continue
      }
      if (-not $receiptPaths.Add($resolvedReceiptPath)) { $blocked.Add("DUPLICATE_EVIDENCE_RECEIPT_PATH:$evidenceName") }
      if (Test-PathsEqual -FirstPath $resolvedReceiptPath -SecondPath $resolvedInputPath) { $blocked.Add("EVIDENCE_RECEIPT_PATH_COLLISION:$evidenceName") }
      if ($resolvedBoundOutput -and (Test-PathsEqual -FirstPath $resolvedReceiptPath -SecondPath $resolvedBoundOutput)) { $blocked.Add("EVIDENCE_RECEIPT_PATH_COLLISION:$evidenceName") }
      foreach ($sourceBinding in @($verifiedSourceBindings)) {
        if (Test-PathsEqual -FirstPath $resolvedReceiptPath -SecondPath ([string]$sourceBinding.path)) { $blocked.Add("EVIDENCE_RECEIPT_PATH_COLLISION:$evidenceName") }
      }
      $actualReceiptHash = (Get-FileHash -LiteralPath $resolvedReceiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($actualReceiptHash -ine $receiptHash) {
        $blocked.Add("EVIDENCE_RECEIPT_HASH_MISMATCH:$evidenceName")
        continue
      }
      try {
        $receipt = Read-JsonFile -Path $resolvedReceiptPath
        if ($null -eq $receipt -or $receipt -is [System.Array] -or $receipt -is [string] -or $receipt -is [ValueType]) { throw 'RECEIPT_MUST_BE_OBJECT' }
        Add-UnknownFields -Object $receipt -AllowedFields @('schema_version', 'generated_at', 'status', 'evidence_name', 'subject_path', 'subject_sha256', 'producer', 'checks', 'metadata') -ErrorPrefix "UNKNOWN_EVIDENCE_RECEIPT_FIELD:${evidenceName}:" -Failures $blocked
        if (-not (Has-Property -Object $receipt -Name 'schema_version') -or [string]$receipt.schema_version -ne '1.0') { $blocked.Add("EVIDENCE_RECEIPT_SCHEMA_VERSION_INVALID:$evidenceName") }
        $receiptStatus = if (Has-Property -Object $receipt -Name 'status') { [string]$receipt.status } else { '' }
        $receiptGeneratedAt = if (Has-Property -Object $receipt -Name 'generated_at') { $receipt.generated_at } else { $null }
        $receiptEvidenceName = if (Has-Property -Object $receipt -Name 'evidence_name') { [string]$receipt.evidence_name } else { '' }
        $receiptSubjectPath = if (Has-Property -Object $receipt -Name 'subject_path') { [string]$receipt.subject_path } else { '' }
        $receiptSubjectHash = if (Has-Property -Object $receipt -Name 'subject_sha256') { [string]$receipt.subject_sha256 } else { '' }
        $receiptProducer = if (Has-Property -Object $receipt -Name 'producer') { [string]$receipt.producer } else { '' }
        $receiptChecks = @()
        if (Has-Property -Object $receipt -Name 'checks') { $receiptChecks = @($receipt.checks) }
        if ($receiptEvidenceName -ne $evidenceName) { $blocked.Add("EVIDENCE_RECEIPT_NAME_MISMATCH:$evidenceName") }
        $parsedReceiptGeneratedAt = [DateTimeOffset]::MinValue
        $receiptTimestampValid = $false
        if ($receiptGeneratedAt -is [DateTimeOffset]) {
          $parsedReceiptGeneratedAt = [DateTimeOffset]$receiptGeneratedAt
          $receiptTimestampValid = $true
        } elseif ($receiptGeneratedAt -is [DateTime] -and $receiptGeneratedAt.Kind -ne [DateTimeKind]::Unspecified) {
          $parsedReceiptGeneratedAt = [DateTimeOffset]$receiptGeneratedAt
          $receiptTimestampValid = $true
        } elseif ($receiptGeneratedAt -is [string] -and -not [string]::IsNullOrWhiteSpace($receiptGeneratedAt) -and $receiptGeneratedAt -match '(Z|[+-]\d{2}:\d{2})$') {
          $receiptTimestampValid = [DateTimeOffset]::TryParse(
            $receiptGeneratedAt,
            [Globalization.CultureInfo]::InvariantCulture,
            ([Globalization.DateTimeStyles]::AssumeUniversal -bor [Globalization.DateTimeStyles]::AdjustToUniversal),
            [ref]$parsedReceiptGeneratedAt
          )
        }
        if (-not $receiptTimestampValid) {
          $blocked.Add("EVIDENCE_RECEIPT_TIMESTAMP_INVALID:$evidenceName")
        } elseif ($parsedReceiptGeneratedAt -gt [DateTimeOffset]::UtcNow.AddSeconds($receiptFutureSkewSeconds)) {
          $blocked.Add("EVIDENCE_RECEIPT_TIMESTAMP_IN_FUTURE:$evidenceName")
        } elseif ($outputLastWriteUtc -and $parsedReceiptGeneratedAt -lt $outputLastWriteUtc.AddSeconds(-$receiptFutureSkewSeconds)) {
          $blocked.Add("EVIDENCE_RECEIPT_TIMESTAMP_PREDATES_OUTPUT:$evidenceName")
        }
        if ($receiptStatus -eq 'BLOCKED') {
          $blocked.Add("EVIDENCE_RECEIPT_BLOCKED:$evidenceName")
        } elseif ($receiptStatus -ne 'PASS') {
          $unverified.Add("EVIDENCE_RECEIPT_NOT_PASS:$evidenceName")
        }
        if ([string]::IsNullOrWhiteSpace($receiptSubjectPath)) {
          $blocked.Add("EVIDENCE_RECEIPT_SUBJECT_PATH_MISSING:$evidenceName")
        } else {
          try { $resolvedReceiptSubjectPath = Get-NormalizedFullPath -Path $receiptSubjectPath } catch { $blocked.Add("EVIDENCE_RECEIPT_SUBJECT_PATH_INVALID:$evidenceName") }
          if ($resolvedReceiptSubjectPath -and $resolvedBoundOutput -and -not (Test-PathsEqual -FirstPath $resolvedReceiptSubjectPath -SecondPath $resolvedBoundOutput)) { $blocked.Add("EVIDENCE_RECEIPT_SUBJECT_PATH_MISMATCH:$evidenceName") }
        }
        if ($receiptSubjectHash -notmatch $hashPattern) {
          $blocked.Add("EVIDENCE_RECEIPT_SUBJECT_HASH_INVALID:$evidenceName")
        } elseif ($actualOutputHash -match $hashPattern -and $receiptSubjectHash -ine $actualOutputHash) {
          $blocked.Add("EVIDENCE_RECEIPT_SUBJECT_HASH_MISMATCH:$evidenceName")
        }
        if ([string]::IsNullOrWhiteSpace($receiptProducer)) { $blocked.Add("EVIDENCE_RECEIPT_PRODUCER_MISSING:$evidenceName") }
        if (@($receiptChecks).Count -lt 1) {
          $blocked.Add("EVIDENCE_RECEIPT_CHECKS_MISSING:$evidenceName")
        } else {
          $checkIds = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
          foreach ($check in @($receiptChecks)) {
            if ($null -eq $check -or $check -is [string] -or $check -is [ValueType]) { $blocked.Add("EVIDENCE_RECEIPT_CHECK_INVALID:$evidenceName"); continue }
            Add-UnknownFields -Object $check -AllowedFields @('check_id', 'status', 'detail', 'evidence', 'metrics') -ErrorPrefix "UNKNOWN_EVIDENCE_RECEIPT_CHECK_FIELD:${evidenceName}:" -Failures $blocked
            $checkId = if (Has-Property -Object $check -Name 'check_id') { [string]$check.check_id } else { '' }
            $checkStatus = if (Has-Property -Object $check -Name 'status') { [string]$check.status } else { '' }
            if ([string]::IsNullOrWhiteSpace($checkId) -or -not $checkIds.Add($checkId)) { $blocked.Add("EVIDENCE_RECEIPT_CHECK_INVALID:$evidenceName") }
            if ($checkStatus -eq 'BLOCKED') { $blocked.Add("EVIDENCE_RECEIPT_CHECK_BLOCKED:${evidenceName}:$checkId") }
            elseif ($checkStatus -ne 'PASS') { $unverified.Add("EVIDENCE_RECEIPT_CHECK_NOT_PASS:${evidenceName}:$checkId") }
          }
        }
        $verifiedNativeVisualBinding = $null
        if ($evidenceName -eq 'visual_assets_verified') {
          if (-not $resolvedBoundOutput -or $actualOutputHash -notmatch $hashPattern) {
            $blocked.Add('NATIVE_VISUAL_BINDING_OUTPUT_UNAVAILABLE:visual_assets_verified')
          } elseif (-not (Has-Property -Object $receipt -Name 'metadata')) {
            $blocked.Add('NATIVE_VISUAL_BINDING_MISSING')
          } else {
            try {
              $verifiedNativeVisualBinding = Assert-NativeVisualCoverageBinding -Metadata $receipt.metadata -ExpectedDeckPath $resolvedBoundOutput -ExpectedDeckHash $actualOutputHash -Label 'visual_assets_verified'
            } catch {
              $blocked.Add((($_.Exception.Message -replace '[\r\n]+', ' ').Trim()))
            }
          }
        }
        $receiptSummary = [ordered]@{
          path = $resolvedReceiptPath
          sha256 = $actualReceiptHash
          status = $receiptStatus
          generated_at = if ($receiptTimestampValid) { $parsedReceiptGeneratedAt.ToUniversalTime().ToString('o') } else { '1970-01-01T00:00:00.0000000Z' }
          subject_path = if ($resolvedReceiptSubjectPath) { $resolvedReceiptSubjectPath } else { $receiptSubjectPath }
          subject_sha256 = if ($receiptSubjectHash -match $hashPattern) { $receiptSubjectHash.ToLowerInvariant() } else { ('0' * 64) }
          producer = $receiptProducer
          check_count = @($receiptChecks).Count
        }
        if ($verifiedNativeVisualBinding) { $receiptSummary.metadata = $verifiedNativeVisualBinding }
        $verifiedEvidenceReceipts[$evidenceName] = $receiptSummary
      } catch {
        $blocked.Add("EVIDENCE_RECEIPT_INVALID_JSON:$evidenceName")
      }
    }
  }

  try {
    $releaseInputHashAfter = (Get-FileHash -LiteralPath (Assert-RegularFilePath -Path $resolvedInputPath -Label 'RELEASE_INPUT_RECHECK') -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($releaseInputHashAfter -ne $releaseInputHashBefore) { $blocked.Add('RELEASE_INPUT_CHANGED_DURING_CERTIFICATION') }
  } catch {
    $blocked.Add('RELEASE_INPUT_CHANGED_DURING_CERTIFICATION')
  }
  foreach ($sourceBinding in @($verifiedSourceBindings)) {
    $sourceId = [string]$sourceBinding.source_id
    try {
      $sourcePath = Assert-RegularFilePath -Path ([string]$sourceBinding.path) -Label 'SOURCE_RECHECK'
      $sourceHashRecheck = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($sourceHashRecheck -ne [string]$sourceBinding.actual_sha256) { $blocked.Add("SOURCE_CHANGED_DURING_CERTIFICATION:$sourceId") }
    } catch {
      $blocked.Add("SOURCE_CHANGED_DURING_CERTIFICATION:$sourceId")
    }
  }
  if ($resolvedBoundOutput -and $actualOutputHash -match $hashPattern) {
    try {
      $outputPathRecheck = Assert-RegularFilePath -Path $resolvedBoundOutput -Label 'OUTPUT_RECHECK'
      $outputHashRecheck = (Get-FileHash -LiteralPath $outputPathRecheck -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($outputHashRecheck -ne $actualOutputHash -or $outputHashRecheck -ine $outputSha256) { $blocked.Add('OUTPUT_CHANGED_DURING_CERTIFICATION') }
    } catch {
      $blocked.Add('OUTPUT_CHANGED_DURING_CERTIFICATION')
    }
  }
  foreach ($evidenceName in @($verifiedEvidenceReceipts.Keys)) {
    $receiptSummary = $verifiedEvidenceReceipts[$evidenceName]
    try {
      $receiptPathRecheck = Assert-RegularFilePath -Path ([string]$receiptSummary.path) -Label 'EVIDENCE_RECEIPT_RECHECK'
      $receiptHashRecheck = (Get-FileHash -LiteralPath $receiptPathRecheck -Algorithm SHA256).Hash.ToLowerInvariant()
      if ($receiptHashRecheck -ne [string]$receiptSummary.sha256) { $blocked.Add("EVIDENCE_RECEIPT_CHANGED_DURING_CERTIFICATION:$evidenceName") }
      if ($evidenceName -eq 'visual_assets_verified' -and $receiptSummary.metadata -and $resolvedBoundOutput -and $actualOutputHash -match $hashPattern) {
        [void](Assert-NativeVisualCoverageBinding -Metadata $receiptSummary.metadata -ExpectedDeckPath $resolvedBoundOutput -ExpectedDeckHash $actualOutputHash -Label 'visual_assets_verified_recheck')
      }
    } catch {
      $recheckMessage = (($_.Exception.Message -replace '[\r\n]+', ' ').Trim())
      if ($recheckMessage -like 'NATIVE_*') { $blocked.Add($recheckMessage) }
      else { $blocked.Add("EVIDENCE_RECEIPT_CHANGED_DURING_CERTIFICATION:$evidenceName") }
    }
  }

  $blockingUnique = @($blocked | Select-Object -Unique)
  $unverifiedUnique = @($unverified | Select-Object -Unique)
  $failedUnique = @($blockingUnique + $unverifiedUnique | Select-Object -Unique)
  $status = if ($blockingUnique.Count -gt 0) { 'BLOCKED' } elseif ($unverifiedUnique.Count -gt 0) { 'UNVERIFIED' } else { 'PASS' }
  $certificate = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    certification_profile = $certificationProfile
    status = $status
    quality_score = $calculatedQualityScore
    calculated_quality_score = $calculatedQualityScore
    domain_scores = $domainScores
    source_hash_unchanged = $sourceHashUnchanged
    source_hash_before = if ($sourceHashBefore -match $hashPattern) { $sourceHashBefore.ToLowerInvariant() } else { ('0' * 64) }
    source_hash_after = if ($sourceHashAfter -match $hashPattern) { $sourceHashAfter.ToLowerInvariant() } else { ('0' * 64) }
    source_bindings = @($verifiedSourceBindings)
    output_sha256 = if ($outputSha256 -match $hashPattern) { $outputSha256.ToLowerInvariant() } else { ('0' * 64) }
    output_path = if ($resolvedBoundOutput) { $resolvedBoundOutput } else { $boundOutputPath }
    output_detected_format = $outputDetectedFormat
    required_domains = $requiredDomains
    required_evidence = $requiredEvidence
    evidence_receipts = $verifiedEvidenceReceipts
    findings = $findings
    failed_requirements = $failedUnique
    blocking_requirements = $blockingUnique
    unverified_requirements = $unverifiedUnique
    certification_rules = [ordered]@{
      minimum_quality_score = $effectiveQualityThreshold
      minimum_domain_score = $effectiveDomainThreshold
      policy_minimum_quality_score = $policyMinimumQualityScore
      policy_minimum_domain_score = $policyMinimumDomainScore
      maximum_p0_findings = 0
      maximum_p1_findings = 0
      source_hash_formula = $sourceHashFormulaVersion
      quality_score_formula = $qualityScoreFormulaVersion
      quality_score_tolerance = $qualityScoreTolerance
      domain_weights = $qualityScoreWeights
    }
  }
  Write-JsonFileNew -Value $certificate -Path $resolvedOutputPath
  $certificate | ConvertTo-Json -Depth 30
  if ($status -eq 'BLOCKED') { exit 2 }
  if ($status -eq 'UNVERIFIED') { exit 3 }
} catch {
  $certificate = New-FallbackCertificate -ErrorMessage $_.Exception.Message
  if (-not (Test-Path -LiteralPath $resolvedOutputPath)) { Write-JsonFileNew -Value $certificate -Path $resolvedOutputPath }
  $certificate | ConvertTo-Json -Depth 30
  [Console]::Error.WriteLine($_.Exception.Message)
  exit 2
}
