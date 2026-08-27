param(
  [Parameter(Mandatory = $true)][string]$ArchivePath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$ExtractionDirectory,
  [switch]$Extract,
  [int]$MaxEntries = 10000,
  [long]$MaxUncompressedBytes = 2147483648,
  [long]$MaxEntryBytes = 536870912
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')

function New-Finding {
  param([string]$Severity, [string]$Code, [string]$Detail)
  return [ordered]@{ severity = $Severity; code = $Code; detail = $Detail }
}

function Assert-ContainedPath {
  param([string]$RootPath, [string]$CandidatePath)
  $root = [System.IO.Path]::GetFullPath($RootPath).TrimEnd('\') + '\'
  $candidate = [System.IO.Path]::GetFullPath($CandidatePath)
  if (-not $candidate.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "ARCHIVE_EXTRACTION_PATH_ESCAPE:$CandidatePath"
  }
  return $candidate
}

function Get-MemberRouteHint {
  param([string]$MemberName)
  $extension = [System.IO.Path]::GetExtension($MemberName).ToLowerInvariant()
  switch ($extension) {
    { $_ -in @('.pptx', '.pptm', '.ppt', '.odp') } { return 'POWERPOINT' }
    { $_ -in @('.docx', '.docm', '.doc', '.rtf') } { return 'DOCUMENT' }
    '.pdf' { return 'PDF' }
    { $_ -in @('.xlsx', '.xlsm', '.xls', '.ods', '.csv', '.tsv', '.json', '.xml') } { return 'DATA' }
    { $_ -in @('.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg') } { return 'AUDIO' }
    { $_ -in @('.mp4', '.mov', '.mkv', '.avi', '.webm') } { return 'VIDEO' }
    { $_ -in @('.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff', '.bmp', '.webp', '.svg') } { return 'IMAGE' }
    default { return 'UNKNOWN' }
  }
}

function Write-ArchiveReport {
  param(
    [string]$Status,
    [object[]]$Risks,
    [object[]]$Entries,
    [object[]]$Artifacts,
    [int]$Processed,
    [int]$Total,
    [string]$DetectedFormat,
    [string]$SourceHashBefore,
    [string]$SourceHashAfter,
    [string]$ExtractionPath,
    [string]$ErrorMessage
  )
  $report = [ordered]@{
    schema_version = '1.0'
    source_id = 'archive-001'
    adapter = 'ARCHIVE'
    status = $Status
    coverage = [ordered]@{ processed = $Processed; total = $Total }
    artifacts = @($Artifacts)
    risks = @($Risks)
    archive_path = $resolvedArchive
    archive_format = $DetectedFormat
    source_sha256_before = $SourceHashBefore
    source_sha256_after = $SourceHashAfter
    extraction_requested = [bool]$Extract
    extraction_directory = $ExtractionPath
    entries = @($Entries)
  }
  if ($ErrorMessage) { $report.error = $ErrorMessage }
  Write-JsonFileNew -Value $report -Path $resolvedOutput
  $report | ConvertTo-Json -Depth 30
  return $report
}

$resolvedArchive = $null
$resolvedOutput = $null
try {
  $resolvedArchive = Assert-RegularFilePath -Path $ArchivePath -Label 'ARCHIVE'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  if (Test-PathsEqual -FirstPath $resolvedArchive -SecondPath $resolvedOutput) { throw 'ARCHIVE_REPORT_PATH_COLLISION' }
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedArchive) -Label 'ARCHIVE_REPORT')
  if ($Extract -and [string]::IsNullOrWhiteSpace($ExtractionDirectory)) { throw 'EXTRACTION_DIRECTORY_REQUIRED' }
  if ($MaxEntries -lt 1 -or $MaxEntries -gt 1000000 -or $MaxUncompressedBytes -lt 1 -or $MaxEntryBytes -lt 1 -or $MaxEntryBytes -gt $MaxUncompressedBytes) { throw 'ARCHIVE_SAFETY_LIMITS_INVALID' }
} catch {
  [Console]::Error.WriteLine(($_.Exception.Message -replace '[\r\n]+', ' ').Trim())
  exit 2
}
$sourceHashBefore = (Get-FileHash -LiteralPath $resolvedArchive -Algorithm SHA256).Hash.ToLowerInvariant()
$detectedFormat = Get-DetectedFileFormat -Path $resolvedArchive
$risks = [System.Collections.Generic.List[object]]::new()
$entries = [System.Collections.Generic.List[object]]::new()
$artifacts = [System.Collections.Generic.List[object]]::new()
$artifacts.Add([ordered]@{ kind = 'ARCHIVE_SOURCE'; path = $resolvedArchive; sha256 = $sourceHashBefore })
$extractionPath = $null
$stagingExtractionPath = $null
$extractionPublished = $false
$sourceHashAfter = $sourceHashBefore

if ($detectedFormat -notin @('ZIP', 'ZIP_CORRUPT', '7Z', 'RAR')) {
  $risks.Add((New-Finding -Severity 'P1' -Code 'NOT_ARCHIVE' -Detail "Detected format is $detectedFormat."))
  [void](Write-ArchiveReport -Status 'BLOCKED' -Risks @($risks) -Entries @() -Artifacts @($artifacts) -Processed 0 -Total 0 -DetectedFormat $detectedFormat -SourceHashBefore $sourceHashBefore -SourceHashAfter $sourceHashAfter -ExtractionPath $null)
  exit 2
}

if ($detectedFormat -in @('7Z', 'RAR')) {
  $tool = if ($detectedFormat -eq '7Z') { Get-Command 7z -ErrorAction SilentlyContinue } else { Get-Command unrar -ErrorAction SilentlyContinue }
  if ($null -eq $tool) {
    $risks.Add((New-Finding -Severity 'P1' -Code 'ARCHIVE_TOOL_UNAVAILABLE' -Detail "Safe listing tool required for $detectedFormat is unavailable."))
    [void](Write-ArchiveReport -Status 'UNVERIFIED' -Risks @($risks) -Entries @() -Artifacts @($artifacts) -Processed 0 -Total 0 -DetectedFormat $detectedFormat -SourceHashBefore $sourceHashBefore -SourceHashAfter $sourceHashAfter -ExtractionPath $null)
    exit 3
  }
  $risks.Add((New-Finding -Severity 'P2' -Code 'ARCHIVE_ADAPTER_NOT_ENABLED' -Detail "Tool $($tool.Source) detected; member listing remains agent-controlled."))
  [void](Write-ArchiveReport -Status 'UNVERIFIED' -Risks @($risks) -Entries @() -Artifacts @($artifacts) -Processed 0 -Total 0 -DetectedFormat $detectedFormat -SourceHashBefore $sourceHashBefore -SourceHashAfter $sourceHashAfter -ExtractionPath $null)
  exit 3
}

if ($detectedFormat -eq 'ZIP_CORRUPT') {
  $risks.Add((New-Finding -Severity 'P1' -Code 'CORRUPT_ARCHIVE' -Detail 'ZIP signature or central directory could not be read.'))
  [void](Write-ArchiveReport -Status 'BLOCKED' -Risks @($risks) -Entries @() -Artifacts @($artifacts) -Processed 0 -Total 0 -DetectedFormat $detectedFormat -SourceHashBefore $sourceHashBefore -SourceHashAfter $sourceHashAfter -ExtractionPath $null)
  exit 2
}

$stream = $null
$archive = $null
$status = 'PASS'
$totalBytes = 0L
$seenNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$seenCanonicalNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$fileMembers = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$directoryMembers = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
$implicitDirectories = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
try {
  Add-Type -AssemblyName System.IO.Compression -ErrorAction SilentlyContinue
  $stream = [System.IO.File]::Open($resolvedArchive, 'Open', 'Read', 'Read')
  $archive = [System.IO.Compression.ZipArchive]::new($stream, [System.IO.Compression.ZipArchiveMode]::Read, $false)
  $total = $archive.Entries.Count
  if ($total -eq 0) { $risks.Add((New-Finding -Severity 'P1' -Code 'ARCHIVE_EMPTY' -Detail 'Archive contains no entries.')); $status = 'BLOCKED' }
  if ($total -gt $MaxEntries) { $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_ENTRY_LIMIT_EXCEEDED' -Detail "entries=$total limit=$MaxEntries")); $status = 'BLOCKED' }

  $entryIndex = 0
  foreach ($entry in $archive.Entries) {
    $entryIndex += 1
    if ($entryIndex -gt $MaxEntries) { break }
    $rawName = [string]$entry.FullName
    $normalizedName = $rawName.Replace('\', '/')
    $segments = @($normalizedName.Split('/'))
    $nonTerminalEmptySegment = @($segments | Select-Object -SkipLast 1 | Where-Object { [string]::IsNullOrEmpty($_) }).Count -gt 0
    $traversalPath = [string]::IsNullOrWhiteSpace($normalizedName) -or $normalizedName.StartsWith('/') -or $normalizedName -match '^[A-Za-z]:' -or $nonTerminalEmptySegment -or @($segments | Where-Object { $_ -in @('.', '..') }).Count -gt 0
    $invalidPath = $traversalPath -or $normalizedName -match ':' -or $normalizedName -match '[\x00-\x1F\x7F]' -or $normalizedName -match '[<>"|?*]'
    $canonicalName = $normalizedName.TrimEnd('/')
    $invalidSegment = @($canonicalName.Split('/') | Where-Object {
      $_ -match '[ .]$' -or $_ -match '^(?i:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?$'
    }).Count -gt 0
    if ($invalidSegment) { $invalidPath = $true }
    if ($invalidPath) {
      $riskCode = if ($traversalPath) { 'ARCHIVE_PATH_TRAVERSAL' } else { 'ARCHIVE_INVALID_MEMBER_NAME' }
      $risks.Add((New-Finding -Severity 'P0' -Code $riskCode -Detail $rawName))
      $status = 'BLOCKED'
      continue
    }
    if (-not $seenNames.Add($normalizedName) -or -not $seenCanonicalNames.Add($canonicalName)) {
      $risks.Add((New-Finding -Severity 'P1' -Code 'ARCHIVE_DUPLICATE_MEMBER' -Detail $normalizedName))
      $status = 'BLOCKED'
    }
    $isDirectory = $normalizedName.EndsWith('/') -or [string]::IsNullOrEmpty($entry.Name)
    $canonicalSegments = @($canonicalName.Split('/'))
    $ancestorPath = ''
    for ($ancestorIndex = 0; $ancestorIndex -lt ($canonicalSegments.Count - 1); $ancestorIndex += 1) {
      $ancestorPath = if ($ancestorIndex -eq 0) { $canonicalSegments[$ancestorIndex] } else { $ancestorPath + '/' + $canonicalSegments[$ancestorIndex] }
      if ($fileMembers.Contains($ancestorPath)) {
        $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_MEMBER_PREFIX_COLLISION' -Detail "$normalizedName conflicts with file $ancestorPath"))
        $status = 'BLOCKED'
      }
      [void]$implicitDirectories.Add($ancestorPath)
    }
    if ($isDirectory) {
      if ($fileMembers.Contains($canonicalName)) {
        $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_MEMBER_PREFIX_COLLISION' -Detail "$normalizedName conflicts with file $canonicalName"))
        $status = 'BLOCKED'
      }
      [void]$directoryMembers.Add($canonicalName)
    } else {
      if ($directoryMembers.Contains($canonicalName) -or $implicitDirectories.Contains($canonicalName)) {
        $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_MEMBER_PREFIX_COLLISION' -Detail "$normalizedName conflicts with directory $canonicalName"))
        $status = 'BLOCKED'
      }
      [void]$fileMembers.Add($canonicalName)
    }
    $entryBytes = [long]$entry.Length
    $compressedBytes = [long]$entry.CompressedLength
    if ($entryBytes -lt 0 -or $compressedBytes -lt 0) {
      $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_MEMBER_SIZE_INVALID' -Detail $normalizedName))
      $status = 'BLOCKED'
      continue
    }
    $unixMode = ([int64]$entry.ExternalAttributes -shr 16) -band 0xF000
    if ($unixMode -eq 0xA000) {
      $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_SYMLINK_MEMBER' -Detail $normalizedName))
      $status = 'BLOCKED'
    }
    if (-not $isDirectory -and $entryBytes -gt $MaxEntryBytes) {
      $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_MEMBER_LIMIT_EXCEEDED' -Detail "$normalizedName bytes=$entryBytes limit=$MaxEntryBytes"))
      $status = 'BLOCKED'
    }
    if (-not $isDirectory) {
      if ($entryBytes -gt ($MaxUncompressedBytes - $totalBytes)) {
        $totalBytes = $MaxUncompressedBytes
        $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_TOTAL_LIMIT_EXCEEDED' -Detail "bytes>$MaxUncompressedBytes limit=$MaxUncompressedBytes"))
        $status = 'BLOCKED'
      } else {
        $totalBytes += $entryBytes
      }
    }
    if ($totalBytes -gt $MaxUncompressedBytes) {
      $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_TOTAL_LIMIT_EXCEEDED' -Detail "bytes=$totalBytes limit=$MaxUncompressedBytes"))
      $status = 'BLOCKED'
    }
    if ($normalizedName -match '(^|/)(vbaProject\.bin|xlm|customUI)(/|$)' -or $normalizedName -match '\.(pptm|docm|xlsm)$') {
      $risks.Add((New-Finding -Severity 'P1' -Code 'ARCHIVE_CONTAINS_MACRO_PAYLOAD' -Detail $normalizedName))
      $status = 'BLOCKED'
    }
    $entries.Add([ordered]@{
      name = $normalizedName
      directory = $isDirectory
      compressed_bytes = $compressedBytes
      uncompressed_bytes = $entryBytes
      route_hint = if ($isDirectory) { 'DIRECTORY' } else { Get-MemberRouteHint -MemberName $normalizedName }
      signature_check_required = -not $isDirectory
    })
  }

  if ($Extract -and $status -eq 'PASS') {
    $hashBeforeExtraction = (Get-FileHash -LiteralPath $resolvedArchive -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hashBeforeExtraction -ne $sourceHashBefore) {
      $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_SOURCE_CHANGED_BEFORE_EXTRACTION' -Detail 'Archive hash changed before extraction.'))
      $status = 'BLOCKED'
    }
  }
  if ($Extract -and $status -eq 'PASS') {
    $extractionPath = Get-NormalizedFullPath -Path $ExtractionDirectory
    $archiveParent = Get-NormalizedFullPath -Path ([System.IO.Path]::GetDirectoryName($resolvedArchive))
    if (Test-PathsEqual -FirstPath $extractionPath -SecondPath $archiveParent) { throw 'Extraction directory cannot be archive parent.' }
    if ((Test-PathsEqual -FirstPath $extractionPath -SecondPath $resolvedOutput) -or (Test-PathInsideDirectory -Path $resolvedOutput -Directory $extractionPath)) { throw 'Extraction directory collides with report path.' }
    Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($extractionPath))
    if (Test-Path -LiteralPath $extractionPath) { throw 'Extraction directory must not already exist.' }
    $extractionParent = [System.IO.Path]::GetDirectoryName($extractionPath)
    [System.IO.Directory]::CreateDirectory($extractionParent) | Out-Null
    $stagingExtractionPath = Join-Path $extractionParent ('.' + [System.IO.Path]::GetFileName($extractionPath) + '.tmp-' + [guid]::NewGuid().ToString('N'))
    [System.IO.Directory]::CreateDirectory($stagingExtractionPath) | Out-Null
    $stagingItem = Get-Item -LiteralPath $stagingExtractionPath -Force -ErrorAction Stop
    if (($stagingItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Extraction staging path cannot be a reparse point.' }
    foreach ($entry in $archive.Entries) {
      $normalizedName = ([string]$entry.FullName).Replace('\', '/')
      $isDirectory = $normalizedName.EndsWith('/') -or [string]::IsNullOrEmpty($entry.Name)
      if ($isDirectory) { continue }
      $relativePath = ($normalizedName.Split('/') | Where-Object { $_ }) -join [System.IO.Path]::DirectorySeparatorChar
      $destination = Assert-ContainedPath -RootPath $stagingExtractionPath -CandidatePath (Join-Path $stagingExtractionPath $relativePath)
      Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($destination))
      Ensure-ParentDirectory -Path $destination
      $entryStream = $null
      $fileStream = $null
      try {
        $entryStream = $entry.Open()
        $fileStream = [System.IO.File]::Open($destination, 'CreateNew', 'Write', 'None')
        $entryStream.CopyTo($fileStream)
      } finally {
        if ($fileStream) { $fileStream.Dispose() }
        if ($entryStream) { $entryStream.Dispose() }
      }
      $destinationItem = Get-Item -LiteralPath $destination -Force -ErrorAction Stop
      if (($destinationItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0 -or $destinationItem.Length -ne [long]$entry.Length) { throw "ARCHIVE_MEMBER_EXTRACTION_MISMATCH:$normalizedName" }
      $memberFormat = Get-DetectedFileFormat -Path $destination
      $memberHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
      $finalDestination = Assert-ContainedPath -RootPath $extractionPath -CandidatePath (Join-Path $extractionPath $relativePath)
      $artifacts.Add([ordered]@{ kind = 'ARCHIVE_MEMBER'; path = $finalDestination; sha256 = $memberHash })
      $entries | Where-Object name -eq $normalizedName | ForEach-Object { $_.detected_format = $memberFormat; $_.sha256 = $memberHash }
    }
    if (Test-Path -LiteralPath $extractionPath) { throw "EXTRACTION_OUTPUT_RACE:$extractionPath" }
    [System.IO.Directory]::Move($stagingExtractionPath, $extractionPath)
    $stagingExtractionPath = $null
    $extractionPublished = $true
  } elseif ($Extract -and $status -ne 'PASS') {
    $risks.Add((New-Finding -Severity 'P1' -Code 'EXTRACTION_SKIPPED_UNSAFE' -Detail 'Archive safety findings prevent extraction.'))
  }
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedArchive -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashAfter -ne $sourceHashBefore) { $risks.Add((New-Finding -Severity 'P0' -Code 'ARCHIVE_SOURCE_CHANGED' -Detail 'Source hash changed during inspection.')); $status = 'BLOCKED' }
  if (@($risks | Where-Object { $_.severity -eq 'P0' -or $_.severity -eq 'P1' }).Count -gt 0) { $status = 'BLOCKED' }
  $reportPayload = [ordered]@{
    schema_version = '1.0'
    source_id = 'archive-001'
    adapter = 'ARCHIVE'
    status = $status
    coverage = [ordered]@{ processed = (@($entries | Where-Object { -not $_.directory }).Count); total = $total }
    artifacts = @($artifacts)
    risks = @($risks)
    archive_path = $resolvedArchive
    archive_format = $detectedFormat
    source_sha256_before = $sourceHashBefore
    source_sha256_after = $sourceHashAfter
    extraction_requested = [bool]$Extract
    extraction_directory = $extractionPath
    entries = @($entries)
  }
  Write-JsonFileNew -Value $reportPayload -Path $resolvedOutput
  $reportPayload | ConvertTo-Json -Depth 30
  if ($status -eq 'BLOCKED') { exit 2 }
} catch {
  if ($stagingExtractionPath -and (Test-Path -LiteralPath $stagingExtractionPath -PathType Container)) {
    $stagingItem = Get-Item -LiteralPath $stagingExtractionPath -Force -ErrorAction SilentlyContinue
    if ($stagingItem -and ($stagingItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) { try { [System.IO.Directory]::Delete($stagingExtractionPath, $true) } catch {} }
  }
  if ($extractionPublished -and $extractionPath -and (Test-Path -LiteralPath $extractionPath -PathType Container)) {
    $publishedItem = Get-Item -LiteralPath $extractionPath -Force -ErrorAction SilentlyContinue
    if ($publishedItem -and ($publishedItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) { try { [System.IO.Directory]::Delete($extractionPath, $true) } catch {} }
  }
  $risks.Add((New-Finding -Severity 'P1' -Code 'ARCHIVE_INSPECTION_FAILED' -Detail $_.Exception.Message))
  $failureReport = [ordered]@{
    schema_version = '1.0'
    source_id = 'archive-001'
    adapter = 'ARCHIVE'
    status = 'UNVERIFIED'
    coverage = [ordered]@{ processed = 0; total = @($entries).Count }
    artifacts = @($artifacts)
    risks = @($risks)
    archive_path = $resolvedArchive
    archive_format = $detectedFormat
    source_sha256_before = $sourceHashBefore
    source_sha256_after = $sourceHashAfter
    extraction_requested = [bool]$Extract
    extraction_directory = $extractionPath
    entries = @($entries)
    error = $_.Exception.Message
  }
  if (-not (Test-Path -LiteralPath $resolvedOutput)) { Write-JsonFileNew -Value $failureReport -Path $resolvedOutput }
  $failureReport | ConvertTo-Json -Depth 30
  exit 3
} finally {
  if ($archive) { $archive.Dispose() }
  if ($stream) { $stream.Dispose() }
}
