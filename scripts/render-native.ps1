param(
  [Parameter(Mandatory = $true)][string]$DeckPath,
  [Parameter(Mandatory = $true)][string]$OutputDirectory,
  [string]$ReportPath,
  [int]$Width = 1920,
  [int]$Height = 1080
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoTrue = -1
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

function Assert-RenderDimension {
  param([int]$Value, [string]$Name)
  if ($Value -lt 1 -or $Value -gt 10000) { throw "INVALID_RENDER_DIMENSION:$Name=$Value" }
}

function Write-ReportIfNew {
  param([object]$Value, [string]$Path)
  if ([string]::IsNullOrWhiteSpace($Path)) { return }
  if (-not (Test-Path -LiteralPath $Path)) { Write-JsonFileNew -Value $Value -Path $Path }
}

try {
  $resolvedDeck = Assert-RegularFilePath -Path $DeckPath -Label 'DECK'
  Assert-RenderDimension -Value $Width -Name 'width'
  Assert-RenderDimension -Value $Height -Name 'height'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputDirectory
  $deckDirectory = [System.IO.Path]::GetDirectoryName($resolvedDeck)
  if ((Test-PathsEqual -FirstPath $resolvedOutput -SecondPath $deckDirectory) -or (Test-PathInsideDirectory -Path $resolvedOutput -Directory $deckDirectory)) {
    throw 'RENDER_OUTPUT_MUST_BE_OUTSIDE_SOURCE_DIRECTORY'
  }
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedDeck) -Label 'RENDER_OUTPUT')
  if ($ReportPath) {
    $resolvedReport = Assert-NewOutputPath -OutputPath $ReportPath -ProtectedPaths @($resolvedDeck, $resolvedOutput) -Label 'RENDER_REPORT'
    if (Test-PathInsideDirectory -Path $resolvedReport -Directory $resolvedOutput) { throw 'RENDER_REPORT_MUST_BE_OUTSIDE_OUTPUT_DIRECTORY' }
    Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedReport))
  }
  Ensure-ParentDirectory -Path $resolvedOutput
  $temporaryOutput = Join-Path ([System.IO.Path]::GetDirectoryName($resolvedOutput)) ('.' + [System.IO.Path]::GetFileName($resolvedOutput) + '.tmp-' + [guid]::NewGuid().ToString('N'))
  [System.IO.Directory]::CreateDirectory($temporaryOutput) | Out-Null
  $sourceHashBefore = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()

  $powerPoint = New-Object -ComObject PowerPoint.Application
  Set-PowerPointSafeAutomation -Application $powerPoint
  $presentation = $powerPoint.Presentations.Open($resolvedDeck, $msoTrue, 0, 0)
  $slideCount = [int]$presentation.Slides.Count
  if ($slideCount -lt 1) { throw 'DECK_CONTAINS_NO_SLIDES' }
  $renders = [System.Collections.Generic.List[object]]::new()
  for ($slideIndex = 1; $slideIndex -le $slideCount; $slideIndex += 1) {
    $slide = $null
    try {
      $slide = $presentation.Slides.Item($slideIndex)
      $temporaryPath = Join-Path $temporaryOutput ('slide-{0:d3}.png' -f $slideIndex)
      if (Test-Path -LiteralPath $temporaryPath) { throw "RENDER_TEMP_COLLISION:$temporaryPath" }
      $slide.Export($temporaryPath, 'PNG', $Width, $Height)
      $renderedPath = Assert-RegularFile -Path $temporaryPath -Label "RENDER_SLIDE_$slideIndex"
      if ((Get-Item -LiteralPath $renderedPath -Force).Length -lt 1 -or (Get-DetectedFileFormat -Path $renderedPath) -ne 'PNG') {
        throw "INVALID_RENDER_OUTPUT:slide=$slideIndex"
      }
      $renders.Add([ordered]@{
        slide = $slideIndex
        path = Join-Path $resolvedOutput ('slide-{0:d3}.png' -f $slideIndex)
        sha256 = (Get-FileHash -LiteralPath $renderedPath -Algorithm SHA256).Hash.ToLowerInvariant()
        size_bytes = (Get-Item -LiteralPath $renderedPath -Force).Length
      })
    } finally { Release-ComObject -Object $slide }
  }

  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_RENDER' }
  $expectedNames = @($renders | ForEach-Object { [System.IO.Path]::GetFileName([string]$_.path) })
  $actualNames = @(Get-ChildItem -LiteralPath $temporaryOutput -File -Force | ForEach-Object { $_.Name })
  if ($actualNames.Count -ne $expectedNames.Count -or @($actualNames | Where-Object { $_ -notin $expectedNames }).Count -gt 0 -or @($expectedNames | Where-Object { $_ -notin $actualNames }).Count -gt 0) {
    throw "RENDER_OUTPUT_SET_INCOMPLETE:expected=$($expectedNames.Count);actual=$($actualNames.Count)"
  }
  if (Test-Path -LiteralPath $resolvedOutput) { throw "RENDER_OUTPUT_RACE:$resolvedOutput" }
  [System.IO.Directory]::Move($temporaryOutput, $resolvedOutput)
  $published = $true
  $temporaryOutput = $null
  $finalNames = @(Get-ChildItem -LiteralPath $resolvedOutput -File -Force | ForEach-Object { $_.Name })
  if ($finalNames.Count -ne $slideCount -or @($finalNames | Where-Object { $_ -notin $expectedNames }).Count -gt 0) { throw 'RENDER_OUTPUT_SET_INCOMPLETE_AFTER_PUBLISH' }
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    deck_path = $resolvedDeck
    output_directory = $resolvedOutput
    status = 'PASS'
    slide_count = $slideCount
    width = $Width
    height = $Height
    source_sha256_before = $sourceHashBefore
    source_sha256_after = $sourceHashAfter
    renders = @($renders)
  }
  if ($resolvedReport) { Write-JsonFileNew -Value $report -Path $resolvedReport }
  $report | ConvertTo-Json -Depth 20
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isBlocked = $message -match '^(SOURCE_CHANGED|RENDER_OUTPUT_RACE|RENDER_OUTPUT_SET_INCOMPLETE|INVALID_RENDER_DIMENSION|.*PATH_COLLISION|.*ALREADY_EXISTS|.*REPARSE_POINT|RENDER_OUTPUT_MUST_BE)'
  if ($temporaryOutput -and (Test-Path -LiteralPath $temporaryOutput -PathType Container) -and -not $published) {
    try { [System.IO.Directory]::Delete($temporaryOutput, $true) } catch {}
  }
  $failure = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    deck_path = if ($resolvedDeck) { $resolvedDeck } else { $DeckPath }
    output_directory = if ($resolvedOutput) { $resolvedOutput } else { $OutputDirectory }
    status = if ($isBlocked) { 'BLOCKED' } else { 'UNVERIFIED' }
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
