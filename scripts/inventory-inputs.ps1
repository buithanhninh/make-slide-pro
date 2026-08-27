param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [switch]$NoRecurse,
  [int]$MaximumFiles = 10000,
  [long]$MaximumFileBytes = 8589934592,
  [long]$MaximumTotalBytes = 34359738368
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

$resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
$resolvedInput = $null
$outputIsSafe = $false

function New-FailureInventory {
  param([Parameter(Mandatory = $true)][string]$Message)
  return [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    input_root = if ($resolvedInput) { $resolvedInput } else { $InputPath }
    source_count = 0
    status = 'BLOCKED'
    blocking_reasons = @('INVENTORY_FAILED')
    errors = @($Message)
    sources = @()
  }
}

try {
  if ($MaximumFiles -lt 1 -or $MaximumFiles -gt 1000000) { throw "MAXIMUM_FILES_INVALID:$MaximumFiles" }
  if ($MaximumFileBytes -lt 1) { throw "MAXIMUM_FILE_BYTES_INVALID:$MaximumFileBytes" }
  if ($MaximumTotalBytes -lt 1) { throw "MAXIMUM_TOTAL_BYTES_INVALID:$MaximumTotalBytes" }
  $resolvedInput = (Resolve-Path -LiteralPath $InputPath -ErrorAction Stop).Path
  $inputItem = Get-Item -LiteralPath $resolvedInput -Force -ErrorAction Stop
  Assert-NoReparseAncestors -Path $resolvedInput
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  if ($inputItem.PSIsContainer) {
    if (($inputItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      throw "INPUT_ROOT_REPARSE_POINT_NOT_ALLOWED:$resolvedInput"
    }
    [void](Assert-NewOutputPath -OutputPath $resolvedOutput -Label 'INVENTORY_OUTPUT')
  } else {
    [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedInput) -Label 'INVENTORY_OUTPUT')
  }
  $outputIsSafe = $true

  $files = @(if ($inputItem.PSIsContainer) {
    Get-ChildItem -LiteralPath $resolvedInput -File -Force -Recurse:(-not $NoRecurse) -ErrorAction Stop | Select-Object -First ($MaximumFiles + 1)
  } else {
    $inputItem
  })
  if ($files.Count -gt $MaximumFiles) { throw "SOURCE_FILE_COUNT_LIMIT_EXCEEDED:count>$MaximumFiles;limit=$MaximumFiles" }
  $totalBytes = [long]0
  foreach ($candidate in $files) {
    $candidateBytes = [long]$candidate.Length
    if ($candidateBytes -gt $MaximumFileBytes) { throw "SOURCE_FILE_BYTES_LIMIT_EXCEEDED:path=$($candidate.FullName);bytes=$candidateBytes;limit=$MaximumFileBytes" }
    if ($totalBytes -gt ($MaximumTotalBytes - $candidateBytes)) { throw "SOURCE_TOTAL_BYTES_LIMIT_EXCEEDED:bytes>$MaximumTotalBytes;limit=$MaximumTotalBytes" }
    $totalBytes += $candidateBytes
  }

  $sources = [System.Collections.Generic.List[object]]::new()
  $errors = [System.Collections.Generic.List[string]]::new()
  $blockingReasons = [System.Collections.Generic.List[string]]::new()
  $index = 0
  foreach ($file in $files | Sort-Object FullName) {
    $index += 1
    $sourceId = 'source-{0:d3}' -f $index
    $riskFlags = [System.Collections.Generic.List[string]]::new()
    $sourceError = $null
    $detectedFormat = 'UNKNOWN'
    $extension = [System.IO.Path]::GetExtension($file.FullName).ToLowerInvariant()
    $sha256 = $null
    $sizeBytes = [long]$file.Length
    $modifiedAt = $file.LastWriteTimeUtc.ToString('o')
    $attributes = $file.Attributes

    try {
      if (($attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        $riskFlags.Add('REPARSE_POINT')
        $blockingReasons.Add('REPARSE_POINT_SOURCE')
      } else {
        Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($file.FullName))
        if ($sizeBytes -eq 0) {
          $riskFlags.Add('EMPTY_FILE')
          $blockingReasons.Add('EMPTY_SOURCE_FILE')
        }
        $hashBefore = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
        $detectedFormat = Get-DetectedFileFormat -Path $file.FullName
        $afterItem = Get-Item -LiteralPath $file.FullName -Force -ErrorAction Stop
        $hashAfter = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256 -ErrorAction Stop).Hash.ToLowerInvariant()
        $sha256 = $hashAfter
        if ($hashBefore -ne $hashAfter -or [long]$afterItem.Length -ne $sizeBytes -or $afterItem.LastWriteTimeUtc.ToString('o') -ne $modifiedAt) {
          $riskFlags.Add('SOURCE_CHANGED_DURING_INVENTORY')
          $blockingReasons.Add('SOURCE_CHANGED_DURING_INVENTORY')
        }
      }
    } catch {
      $sourceError = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
      $riskFlags.Add('SOURCE_READ_FAILED')
      $blockingReasons.Add('SOURCE_READ_FAILED')
      $errors.Add("${sourceId}:$sourceError")
    }

    $expected = @(Get-ExpectedFormatsForExtension -Extension $extension)
    $mismatch = $expected.Count -gt 0 -and $detectedFormat -notin $expected
    if ($mismatch) { $riskFlags.Add('SIGNATURE_EXTENSION_MISMATCH') }
    if ($detectedFormat -in @('PPTM', 'DOCM', 'XLSM')) { $riskFlags.Add('MACRO_ENABLED') }
    if ($detectedFormat -eq 'ZIP_CORRUPT') {
      $riskFlags.Add('CORRUPT_ARCHIVE')
      $blockingReasons.Add('CORRUPT_ARCHIVE')
    }
    if ($detectedFormat -eq 'UNKNOWN') { $riskFlags.Add('UNKNOWN_FORMAT') }

    $sources.Add([ordered]@{
      source_id = $sourceId
      path = $file.FullName
      name = $file.Name
      extension = $extension
      detected_format = $detectedFormat
      extension_mismatch = $mismatch
      sha256 = $sha256
      size_bytes = $sizeBytes
      modified_at = $modifiedAt
      role = Get-DefaultSourceRole -DetectedFormat $detectedFormat -Extension $extension
      authority = 'UNRESOLVED'
      risk_flags = @($riskFlags | Select-Object -Unique)
      error = $sourceError
    })
  }

  if ($sources.Count -eq 0) { $blockingReasons.Add('NO_SOURCE_FILES') }
  $blockingUnique = @($blockingReasons | Select-Object -Unique)
  $status = if ($blockingUnique.Count -gt 0) { 'BLOCKED' } else { 'PASS' }
  $payload = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    input_root = $resolvedInput
    source_count = $sources.Count
    status = $status
    blocking_reasons = $blockingUnique
    errors = @($errors)
    sources = @($sources)
  }
  Write-JsonFileNew -Value $payload -Path $resolvedOutput
  $payload | ConvertTo-Json -Depth 30
  if ($status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  if ($outputIsSafe -and -not (Test-Path -LiteralPath $resolvedOutput)) {
    $payload = New-FailureInventory -Message $message
    Write-JsonFileNew -Value $payload -Path $resolvedOutput
    $payload | ConvertTo-Json -Depth 20
  }
  [Console]::Error.WriteLine($message)
  exit 2
}
