param(
  [Parameter(Mandatory = $true)][string]$DeckPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string]$ReportPath
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoTrue = -1
$msoFalse = 0
$ppSaveAsPDF = 32
$powerPoint = $null
$presentation = $null
$resolvedDeck = $null
$resolvedOutput = $null
$resolvedReport = $null
$temporaryOutput = $null
$published = $false
$sourceHashBefore = $null
$sourceHashAfter = $null

function Assert-RegularFile {
  param([Parameter(Mandatory = $true)][string]$Path, [string]$Label = 'FILE')
  $resolved = Get-NormalizedFullPath -Path $Path
  if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { throw "${Label}_MISSING:$resolved" }
  $item = Get-Item -LiteralPath $resolved -Force -ErrorAction Stop
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "${Label}_REPARSE_POINT_NOT_ALLOWED:$resolved" }
  return $resolved
}

function Assert-NoReparseAncestors {
  param([Parameter(Mandatory = $true)][string]$Path)
  $current = Get-NormalizedFullPath -Path $Path
  while ($current) {
    if (Test-Path -LiteralPath $current) {
      $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
      if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "PATH_REPARSE_POINT_NOT_ALLOWED:$current" }
    }
    $parent = [System.IO.Path]::GetDirectoryName($current)
    if ([string]::IsNullOrEmpty($parent) -or $parent -eq $current) { break }
    $current = $parent
  }
}

function Write-ReportIfNew {
  param([object]$Value, [string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path)) { return }
  if (-not (Test-Path -LiteralPath $Path)) { Write-JsonFileNew -Value $Value -Path $Path }
}

try {
  $resolvedDeck = Assert-RegularFilePath -Path $DeckPath -Label 'DECK'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  if (Test-PathsEqual -FirstPath $resolvedDeck -SecondPath $resolvedOutput) { throw 'PDF_OUTPUT_PATH_COLLISION' }
  if ([System.IO.Path]::GetExtension($resolvedOutput).ToLowerInvariant() -ne '.pdf') { throw 'PDF_OUTPUT_EXTENSION_REQUIRED' }
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedDeck) -Label 'PDF_OUTPUT')
  if ($ReportPath) {
    $resolvedReport = Assert-NewOutputPath -OutputPath $ReportPath -ProtectedPaths @($resolvedDeck, $resolvedOutput) -Label 'PDF_REPORT'
    Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedReport))
  }
  Ensure-ParentDirectory -Path $resolvedOutput
  $temporaryOutput = Join-Path ([System.IO.Path]::GetDirectoryName($resolvedOutput)) ('.' + [System.IO.Path]::GetFileNameWithoutExtension($resolvedOutput) + '.tmp-' + [guid]::NewGuid().ToString('N') + '.pdf')
  $sourceHashBefore = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()

  $powerPoint = New-Object -ComObject PowerPoint.Application
  Set-PowerPointSafeAutomation -Application $powerPoint
  $presentation = $powerPoint.Presentations.Open($resolvedDeck, $msoTrue, 0, 0)
  $slideCount = [int]$presentation.Slides.Count
  if ($slideCount -lt 1) { throw 'DECK_CONTAINS_NO_SLIDES' }
  $presentation.SaveAs($temporaryOutput, $ppSaveAsPDF, $msoFalse)
  $temporaryOutput = Assert-RegularFile -Path $temporaryOutput -Label 'PDF_TEMP_OUTPUT'
  if ((Get-Item -LiteralPath $temporaryOutput -Force).Length -lt 1 -or (Get-DetectedFileFormat -Path $temporaryOutput) -ne 'PDF') { throw 'INVALID_PDF_EXPORT' }
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_PDF_EXPORT' }
  if (Test-Path -LiteralPath $resolvedOutput) { throw "PDF_OUTPUT_RACE:$resolvedOutput" }
  [System.IO.File]::Move($temporaryOutput, $resolvedOutput)
  $published = $true
  $temporaryOutput = $null
  if ((Get-DetectedFileFormat -Path $resolvedOutput) -ne 'PDF') { throw 'OUTPUT_IS_NOT_PDF_AFTER_PUBLISH' }
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  $status = if ($sourceHashBefore -eq $sourceHashAfter) { 'PASS' } else { 'BLOCKED' }
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = $status
    deck_path = $resolvedDeck
    output_path = $resolvedOutput
    slide_count = $slideCount
    source_sha256_before = $sourceHashBefore
    source_sha256_after = $sourceHashAfter
    output_sha256 = (Get-FileHash -LiteralPath $resolvedOutput -Algorithm SHA256).Hash.ToLowerInvariant()
  }
  if ($resolvedReport) { Write-JsonFileNew -Value $report -Path $resolvedReport }
  $report | ConvertTo-Json -Depth 20
  if ($status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isBlocked = $message -match '^(SOURCE_CHANGED|PDF_OUTPUT|INVALID_PDF|OUTPUT_IS_NOT_PDF|.*PATH_COLLISION|.*ALREADY_EXISTS|.*REPARSE_POINT|PDF_OUTPUT_EXTENSION)'
  if ($temporaryOutput -and (Test-Path -LiteralPath $temporaryOutput -PathType Leaf) -and -not $published) {
    try { [System.IO.File]::Delete($temporaryOutput) } catch {}
  }
  $failure = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    status = if ($isBlocked) { 'BLOCKED' } else { 'UNVERIFIED' }
    deck_path = if ($resolvedDeck) { $resolvedDeck } else { $DeckPath }
    output_path = if ($resolvedOutput) { $resolvedOutput } else { $OutputPath }
    error = $message
  }
  if ($sourceHashBefore) { $failure.source_sha256_before = $sourceHashBefore }
  if ($sourceHashAfter) { $failure.source_sha256_after = $sourceHashAfter }
  if ($resolvedReport) { Write-ReportIfNew -Value $failure -Path $resolvedReport }
  [Console]::Error.WriteLine($message)
  exit $(if ($isBlocked) { 2 } else { 3 })
} finally {
  if ($presentation) { try { $presentation.Close() } catch {}; Release-ComObject -Object $presentation }
  if ($powerPoint) { try { $powerPoint.Quit() } catch {}; Release-ComObject -Object $powerPoint }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
