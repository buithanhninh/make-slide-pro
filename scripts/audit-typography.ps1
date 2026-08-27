param(
  [Parameter(Mandatory = $true)][string]$DeckPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [string[]]$AllowedFonts = @(),
  [double]$MinimumBodyFontSize = 16,
  [double]$MinimumTitleFontSize = 28,
  [double]$MinimumUtilityFontSize = 8
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoTrue = -1
$msoGroup = 6
$AllowedFonts = @($AllowedFonts | ForEach-Object { ([string]$_ -split ',') } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
$allowedFontSet = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
foreach ($fontName in $AllowedFonts) { [void]$allowedFontSet.Add([string]$fontName) }
$findings = [System.Collections.Generic.List[object]]::new()
$fontUsage = @{}
$slides = [System.Collections.Generic.List[object]]::new()
$powerPoint = $null
$presentation = $null
$resolvedDeck = $null
$resolvedOutput = $null
$reportReady = $false
$sourceHashBefore = $null
$sourceHashAfter = $null

function Add-TypographyFinding {
  param([string]$Severity, [string]$Code, [int]$Slide, [string]$Object, [string]$Detail)
  $script:findings.Add([ordered]@{ severity = $Severity; code = $Code; slide = $Slide; object = $Object; detail = $Detail })
}

function Assert-FiniteThreshold {
  param([double]$Value, [string]$Name, [double]$Minimum, [double]$Maximum)
  if ([double]::IsNaN($Value) -or [double]::IsInfinity($Value) -or $Value -lt $Minimum -or $Value -gt $Maximum) { throw "INVALID_TYPOGRAPHY_THRESHOLD:$Name=$Value" }
}

function Visit-Shape {
  param([object]$Shape, [int]$SlideNumber, [string]$ObjectLabel)
  $shapeName = if ([string]::IsNullOrWhiteSpace($ObjectLabel)) { [string]$Shape.Name } else { $ObjectLabel }
  $textSnapshot = $null
  try {
    $hasText = $false
    try { $hasText = $Shape.HasTextFrame -eq $msoTrue -and $Shape.TextFrame2.HasText -eq $msoTrue } catch { $hasText = $false }
    if ($hasText) {
      $range = $null
      try {
        $range = $Shape.TextFrame2.TextRange
        $font = [string]$range.Font.Name
        $size = [double]$range.Font.Size
        $rawText = [string]$range.Text
        $text = (($rawText -replace '\s+', ' ').Trim())
        if ([string]::IsNullOrWhiteSpace($font)) { Add-TypographyFinding 'P1' 'FONT_NAME_MISSING' $SlideNumber $shapeName 'font name is empty' }
        if (-not $fontUsage.ContainsKey($font)) { $fontUsage[$font] = 0 }
        $fontUsage[$font] += 1
        if ($AllowedFonts.Count -gt 0 -and -not $allowedFontSet.Contains($font)) { Add-TypographyFinding 'P1' 'FONT_NOT_ALLOWED' $SlideNumber $shapeName "font=$font" }
        if ([double]::IsNaN($size) -or [double]::IsInfinity($size) -or $size -le 0) { Add-TypographyFinding 'P1' 'FONT_SIZE_INVALID' $SlideNumber $shapeName "size=$size" }
        $isTitle = ($shapeName -match '(?i)(title|headline|heading)') -or ([double]$Shape.Top -lt 130 -and $size -ge 20)
        $isChrome = (([double]$Shape.Top -lt 48 -or [double]$Shape.Top -gt 660) -and $text.Length -le 80)
        $isUtility = $isChrome -or ($shapeName -match '(?i)(label|caption|kicker|eyebrow|badge|tag|footer|header|source|note|legend|year|page|gate|proof|metric|section|pill|chip)') -or ($size -le 14 -and $text.Length -le 90 -and [double]$Shape.Height -le 44)
        $minimum = if ($isTitle) { $MinimumTitleFontSize } elseif ($isUtility) { $MinimumUtilityFontSize } else { $MinimumBodyFontSize }
        if ($size -lt $minimum) { Add-TypographyFinding 'P1' 'FONT_TOO_SMALL' $SlideNumber $shapeName "size=$size minimum=$minimum utility=$isUtility text=$text" }
        if ($rawText -match '[\r\n\v]' -and $isTitle -and $text.Length -lt 160) { Add-TypographyFinding 'P1' 'TITLE_WRAP_RISK' $SlideNumber $shapeName $text }
        $textSnapshot = [ordered]@{ name = $shapeName; font = $font; size = $size; text = $text; is_title = $isTitle; is_utility = $isUtility; minimum_size = $minimum }
      } finally { Release-ComObject -Object $range }
    }

    $hasTable = $false
    try { $hasTable = $Shape.HasTable -eq $msoTrue } catch { $hasTable = $false }
    if ($hasTable) {
      $table = $null
      try {
        $table = $Shape.Table
        for ($row = 1; $row -le $table.Rows.Count; $row += 1) {
          for ($column = 1; $column -le $table.Columns.Count; $column += 1) {
            $cell = $null
            $cellShape = $null
            try {
              $cell = $table.Cell($row, $column)
              $cellShape = $cell.Shape
              [void](Visit-Shape -Shape $cellShape -SlideNumber $SlideNumber -ObjectLabel "$shapeName[$row,$column]")
            } catch { Add-TypographyFinding 'P1' 'TABLE_TEXT_INSPECTION_FAILED' $SlideNumber "$shapeName[$row,$column]" $_.Exception.Message } finally {
              Release-ComObject -Object $cellShape
              Release-ComObject -Object $cell
            }
          }
        }
      } finally { Release-ComObject -Object $table }
    }

    $shapeType = 0
    try { $shapeType = [int]$Shape.Type } catch {}
    if ($shapeType -eq $msoGroup) {
      $groupItems = $null
      try {
        $groupItems = $Shape.GroupItems
        for ($itemIndex = 1; $itemIndex -le $groupItems.Count; $itemIndex += 1) {
          $groupItem = $null
          try {
            $groupItem = $groupItems.Item($itemIndex)
            [void](Visit-Shape -Shape $groupItem -SlideNumber $SlideNumber -ObjectLabel "$shapeName/$($groupItem.Name)")
          } finally { Release-ComObject -Object $groupItem }
        }
      } catch { Add-TypographyFinding 'P1' 'GROUP_TEXT_INSPECTION_FAILED' $SlideNumber $shapeName $_.Exception.Message } finally { Release-ComObject -Object $groupItems }
    }
  } catch {
    Add-TypographyFinding 'P1' 'TEXT_INSPECTION_FAILED' $SlideNumber $shapeName $_.Exception.Message
  }
  return $textSnapshot
}

try {
  $resolvedDeck = Assert-RegularFilePath -Path $DeckPath -Label 'DECK'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedDeck) -Label 'AUDIT_OUTPUT')
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  Assert-FiniteThreshold -Value $MinimumBodyFontSize -Name 'body' -Minimum 1 -Maximum 200
  Assert-FiniteThreshold -Value $MinimumTitleFontSize -Name 'title' -Minimum 1 -Maximum 200
  Assert-FiniteThreshold -Value $MinimumUtilityFontSize -Name 'utility' -Minimum 1 -Maximum 200
  Ensure-ParentDirectory -Path $resolvedOutput
  $reportReady = $true
  $sourceHashBefore = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  $powerPoint = New-Object -ComObject PowerPoint.Application
  Set-PowerPointSafeAutomation -Application $powerPoint
  $presentation = $powerPoint.Presentations.Open($resolvedDeck, $msoTrue, 0, 0)
  $slideCount = [int]$presentation.Slides.Count
  if ($slideCount -lt 1) { throw 'DECK_CONTAINS_NO_SLIDES' }
  for ($slideIndex = 1; $slideIndex -le $slideCount; $slideIndex += 1) {
    $slide = $null
    try {
      $slide = $presentation.Slides.Item($slideIndex)
      $texts = [System.Collections.Generic.List[object]]::new()
      for ($shapeIndex = 1; $shapeIndex -le $slide.Shapes.Count; $shapeIndex += 1) {
        $shape = $null
        try {
          $shape = $slide.Shapes.Item($shapeIndex)
          $snapshot = Visit-Shape -Shape $shape -SlideNumber $slideIndex -ObjectLabel ([string]$shape.Name)
          if ($snapshot) { $texts.Add($snapshot) }
        } finally { Release-ComObject -Object $shape }
      }
      $slides.Add([ordered]@{ slide = $slideIndex; text_objects = @($texts) })
    } finally { Release-ComObject -Object $slide }
  }
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_TYPOGRAPHY_AUDIT' }
  $criticalCount = @($findings | Where-Object { $_.severity -in @('P0', 'P1') }).Count
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    deck_path = $resolvedDeck
    deck_sha256_before = $sourceHashBefore
    deck_sha256_after = $sourceHashAfter
    status = if ($criticalCount -gt 0) { 'BLOCKED' } else { 'PASS' }
    allowed_fonts = @($AllowedFonts)
    thresholds = [ordered]@{ body = $MinimumBodyFontSize; title = $MinimumTitleFontSize; utility = $MinimumUtilityFontSize }
    font_usage = $fontUsage
    findings = @($findings)
    slides = @($slides)
  }
  Write-JsonFileNew -Value $report -Path $resolvedOutput
  $report | ConvertTo-Json -Depth 30
  if ($report.status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isBlocked = $message -match '^(SOURCE_CHANGED|AUDIT_OUTPUT|INVALID_TYPOGRAPHY_THRESHOLD|DECK_CONTAINS_NO_SLIDES|.*COLLISION|.*ALREADY_EXISTS|.*REPARSE_POINT)'
  $failure = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); deck_path = if ($resolvedDeck) { $resolvedDeck } else { $DeckPath }; status = if ($isBlocked) { 'BLOCKED' } else { 'UNVERIFIED' }; error = $message; findings = @($findings) }
  if ($sourceHashBefore) { $failure.deck_sha256_before = $sourceHashBefore }
  if ($sourceHashAfter) { $failure.deck_sha256_after = $sourceHashAfter }
  if ($reportReady -and -not (Test-Path -LiteralPath $resolvedOutput)) { Write-JsonFileNew -Value $failure -Path $resolvedOutput }
  [Console]::Error.WriteLine($message)
  exit $(if ($isBlocked) { 2 } else { 3 })
} finally {
  if ($presentation) { try { $presentation.Close() } catch {}; Release-ComObject -Object $presentation }
  if ($powerPoint) { try { $powerPoint.Quit() } catch {}; Release-ComObject -Object $powerPoint }
  [GC]::Collect(); [GC]::WaitForPendingFinalizers()
}
