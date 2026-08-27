param(
  [Parameter(Mandatory = $true)][string]$BaselinePath,
  [Parameter(Mandatory = $true)][string]$CandidatePath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$CollectionProperty = 'atoms',
  [string]$KeyProperty = 'atom_id',
  [string[]]$CriticalFields = @('verbatim', 'normalized', 'priority', 'destination')
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$resolvedBaseline = $null
$resolvedCandidate = $null
$resolvedOutput = $null
$reportReady = $false
$baselineHashBefore = $null
$candidateHashBefore = $null
$baselineHashAfter = $null
$candidateHashAfter = $null

function Get-PropertyValue {
  param([object]$Value, [string]$Name)
  if ($null -eq $Value) { return $null }
  $property = $Value.PSObject.Properties[$Name]
  if ($null -eq $property) { return $null }
  return $property.Value
}

function ConvertTo-CanonicalObject {
  param([object]$Value)
  if ($null -eq $Value -or $Value -is [string] -or $Value -is [ValueType]) { return $Value }
  if ($Value -is [System.Collections.IDictionary]) {
    $ordered = [ordered]@{}
    foreach ($key in @($Value.Keys | Sort-Object)) { $ordered[[string]$key] = ConvertTo-CanonicalObject -Value $Value[$key] }
    return $ordered
  }
  if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [pscustomobject])) {
    return @($Value | ForEach-Object { ConvertTo-CanonicalObject -Value $_ })
  }
  $object = [ordered]@{}
  foreach ($property in @($Value.PSObject.Properties | Sort-Object Name)) { $object[$property.Name] = ConvertTo-CanonicalObject -Value $property.Value }
  return $object
}

function ConvertTo-CanonicalJson {
  param([object]$Value)
  return (ConvertTo-CanonicalObject -Value $Value | ConvertTo-Json -Depth 40 -Compress)
}

function Get-Collection {
  param([object]$Value, [string]$Name)
  if ($Value -is [System.Array]) { return @($Value) }
  if ($null -eq $Value -or $Value -is [string] -or $Value -is [ValueType]) { throw "COLLECTION_ROOT_INVALID:$Name" }
  $property = $Value.PSObject.Properties[$Name]
  if ($null -eq $property) { throw "COLLECTION_NOT_FOUND:$Name" }
  if ($null -eq $property.Value -or $property.Value -isnot [System.Array]) { throw "COLLECTION_MUST_BE_ARRAY:$Name" }
  return @($property.Value)
}

function Assert-ItemObject {
  param([object]$Item, [string]$Label)
  if ($null -eq $Item -or $Item -is [string] -or $Item -is [ValueType] -or $Item -is [System.Array]) { throw "ITEM_MUST_BE_OBJECT:$Label" }
}

try {
  $resolvedBaseline = Assert-RegularFilePath -Path $BaselinePath -Label 'BASELINE'
  $resolvedCandidate = Assert-RegularFilePath -Path $CandidatePath -Label 'CANDIDATE'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  if (Test-PathsEqual -FirstPath $resolvedBaseline -SecondPath $resolvedCandidate) { throw 'BASELINE_CANDIDATE_PATH_COLLISION' }
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedBaseline, $resolvedCandidate) -Label 'CONTENT_DIFF_OUTPUT')
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  if ([string]::IsNullOrWhiteSpace($CollectionProperty) -or [string]::IsNullOrWhiteSpace($KeyProperty)) { throw 'COLLECTION_OR_KEY_PROPERTY_REQUIRED' }
  $criticalFieldSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
  foreach ($field in @($CriticalFields)) {
    if ([string]::IsNullOrWhiteSpace([string]$field) -or -not $criticalFieldSet.Add([string]$field)) { throw 'CRITICAL_FIELDS_MUST_BE_UNIQUE_AND_NONEMPTY' }
  }
  Ensure-ParentDirectory -Path $resolvedOutput
  $reportReady = $true
  $baselineHashBefore = (Get-FileHash -LiteralPath $resolvedBaseline -Algorithm SHA256).Hash.ToLowerInvariant()
  $candidateHashBefore = (Get-FileHash -LiteralPath $resolvedCandidate -Algorithm SHA256).Hash.ToLowerInvariant()
  $baseline = Read-JsonFile -Path $resolvedBaseline
  $candidate = Read-JsonFile -Path $resolvedCandidate
  $baselineItems = @(Get-Collection -Value $baseline -Name $CollectionProperty)
  $candidateItems = @(Get-Collection -Value $candidate -Name $CollectionProperty)
  $findings = [System.Collections.Generic.List[object]]::new()
  $candidateMap = [System.Collections.Generic.Dictionary[string,object]]::new([System.StringComparer]::Ordinal)
  $baselineMap = [System.Collections.Generic.Dictionary[string,object]]::new([System.StringComparer]::Ordinal)

  for ($index = 0; $index -lt $candidateItems.Count; $index += 1) {
    $item = $candidateItems[$index]
    Assert-ItemObject -Item $item -Label "candidate[$index]"
    $keyValue = Get-PropertyValue -Value $item -Name $KeyProperty
    if ($keyValue -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$keyValue)) {
      $findings.Add([ordered]@{ severity = 'P1'; code = 'CANDIDATE_ITEM_KEY_INVALID'; detail = "${KeyProperty}:index=$index" })
      continue
    }
    $key = ([string]$keyValue).Trim()
    if (-not $candidateMap.TryAdd($key, $item)) { $findings.Add([ordered]@{ severity = 'P1'; code = 'CANDIDATE_DUPLICATE_KEY'; detail = $key }) }
  }

  for ($index = 0; $index -lt $baselineItems.Count; $index += 1) {
    $item = $baselineItems[$index]
    Assert-ItemObject -Item $item -Label "baseline[$index]"
    $keyValue = Get-PropertyValue -Value $item -Name $KeyProperty
    if ($keyValue -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$keyValue)) {
      $findings.Add([ordered]@{ severity = 'P1'; code = 'BASELINE_ITEM_KEY_INVALID'; detail = "${KeyProperty}:index=$index" })
      continue
    }
    $key = ([string]$keyValue).Trim()
    if (-not $baselineMap.TryAdd($key, $item)) { $findings.Add([ordered]@{ severity = 'P1'; code = 'BASELINE_DUPLICATE_KEY'; detail = $key }); continue }
    if (-not $candidateMap.ContainsKey($key)) {
      $priority = [string](Get-PropertyValue -Value $item -Name 'priority')
      $mustPreserveValue = Get-PropertyValue -Value $item -Name 'must_preserve'
      $mustPreserve = $mustPreserveValue -is [bool] -and [bool]$mustPreserveValue
      $severity = if ($priority -in @('P0', 'P1') -or $mustPreserve) { 'P1' } else { 'P2' }
      $findings.Add([ordered]@{ severity = $severity; code = 'CONTENT_ITEM_MISSING'; detail = $key })
      continue
    }
    $candidateItem = $candidateMap[$key]
    foreach ($field in @($CriticalFields)) {
      $before = ConvertTo-CanonicalJson -Value (Get-PropertyValue -Value $item -Name $field)
      $after = ConvertTo-CanonicalJson -Value (Get-PropertyValue -Value $candidateItem -Name $field)
      if ($before -ne $after) { $findings.Add([ordered]@{ severity = 'P1'; code = 'CONTENT_FIELD_CHANGED'; detail = "${key}:$field"; baseline = $before; candidate = $after }) }
    }
  }

  foreach ($key in @($candidateMap.Keys)) {
    if (-not $baselineMap.ContainsKey($key)) { $findings.Add([ordered]@{ severity = 'P2'; code = 'CONTENT_ITEM_ADDED'; detail = $key }) }
  }
  $baselineHashAfter = (Get-FileHash -LiteralPath $resolvedBaseline -Algorithm SHA256).Hash.ToLowerInvariant()
  $candidateHashAfter = (Get-FileHash -LiteralPath $resolvedCandidate -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($baselineHashBefore -ne $baselineHashAfter) { $findings.Add([ordered]@{ severity = 'P0'; code = 'BASELINE_CHANGED_DURING_COMPARE'; detail = $resolvedBaseline }) }
  if ($candidateHashBefore -ne $candidateHashAfter) { $findings.Add([ordered]@{ severity = 'P0'; code = 'CANDIDATE_CHANGED_DURING_COMPARE'; detail = $resolvedCandidate }) }
  $criticalCount = @($findings | Where-Object { $_.severity -in @('P0', 'P1') }).Count
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = if ($criticalCount -gt 0) { 'BLOCKED' } else { 'PASS' }
    baseline_path = $resolvedBaseline
    candidate_path = $resolvedCandidate
    baseline_sha256_before = $baselineHashBefore
    baseline_sha256_after = $baselineHashAfter
    candidate_sha256_before = $candidateHashBefore
    candidate_sha256_after = $candidateHashAfter
    collection_property = $CollectionProperty
    key_property = $KeyProperty
    baseline_count = $baselineItems.Count
    candidate_count = $candidateItems.Count
    findings = @($findings)
  }
  Write-JsonFileNew -Value $report -Path $resolvedOutput
  $report | ConvertTo-Json -Depth 30
  if ($report.status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $failure = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); status = 'BLOCKED'; baseline_path = if ($resolvedBaseline) { $resolvedBaseline } else { $BaselinePath }; candidate_path = if ($resolvedCandidate) { $resolvedCandidate } else { $CandidatePath }; error = $message; findings = @() }
  if ($baselineHashBefore) { $failure.baseline_sha256_before = $baselineHashBefore }
  if ($baselineHashAfter) { $failure.baseline_sha256_after = $baselineHashAfter }
  if ($candidateHashBefore) { $failure.candidate_sha256_before = $candidateHashBefore }
  if ($candidateHashAfter) { $failure.candidate_sha256_after = $candidateHashAfter }
  if ($reportReady -and -not (Test-Path -LiteralPath $resolvedOutput)) { Write-JsonFileNew -Value $failure -Path $resolvedOutput }
  [Console]::Error.WriteLine($message)
  exit 2
}
