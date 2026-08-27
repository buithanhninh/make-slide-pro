param(
  [Parameter(Mandatory = $true)][string]$DeckPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [double]$TextTolerancePoints = 4.0,
  [double]$CanvasTolerancePoints = 1.0
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoTrue = -1
$msoGroup = 6
$findings = [System.Collections.Generic.List[object]]::new()
$slidesReport = [System.Collections.Generic.List[object]]::new()
$powerPoint = $null
$presentation = $null
$resolvedDeck = $null
$resolvedOutput = $null
$reportReady = $false
$sourceHashBefore = $null
$sourceHashAfter = $null

function Add-Finding {
  param([string]$Severity, [string]$Code, [int]$Slide, [string]$Object, [string]$Detail)
  $script:findings.Add([ordered]@{ severity = $Severity; code = $Code; slide = $Slide; object = $Object; detail = $Detail })
}

function Test-TextFrame {
  param([object]$Shape, [int]$SlideNumber, [string]$ObjectLabel)
  if ($Shape.HasTextFrame -ne $msoTrue -or $Shape.TextFrame2.HasText -ne $msoTrue) { return $null }
  $range = $null
  try {
    $range = $Shape.TextFrame2.TextRange
    $left = [double]$Shape.Left
    $top = [double]$Shape.Top
    $right = $left + [double]$Shape.Width
    $bottom = $top + [double]$Shape.Height
    $textLeft = [double]$range.BoundLeft
    $textTop = [double]$range.BoundTop
    $textRight = $textLeft + [double]$range.BoundWidth
    $textBottom = $textTop + [double]$range.BoundHeight
    if ($textLeft -lt $left - $TextTolerancePoints -or $textTop -lt $top - $TextTolerancePoints -or $textRight -gt $right + $TextTolerancePoints -or $textBottom -gt $bottom + $TextTolerancePoints) {
      Add-Finding -Severity 'P1' -Code 'TEXT_OVERFLOW' -Slide $SlideNumber -Object $ObjectLabel -Detail ("text=({0:N1},{1:N1})-({2:N1},{3:N1}); shape=({4:N1},{5:N1})-({6:N1},{7:N1})" -f $textLeft,$textTop,$textRight,$textBottom,$left,$top,$right,$bottom)
    }
    $normalized = (([string]$range.Text -replace '\s+', ' ').Trim())
    if ($normalized -match '^(Click to add|Nhấp để thêm|Slide Number|Date|Footer)$') {
      Add-Finding -Severity 'P1' -Code 'UNRESOLVED_PLACEHOLDER_TEXT' -Slide $SlideNumber -Object $ObjectLabel -Detail $normalized
    }
    return [ordered]@{ text = $normalized; font = [string]$range.Font.Name; font_size = [double]$range.Font.Size; text_bounds = @($textLeft,$textTop,$textRight,$textBottom) }
  } finally {
    Release-ComObject -Object $range
  }
}

function Test-IntentionalOverlay {
  param([string]$Name)
  return $Name -match '(?i)(background|backdrop|glow|shadow|footer|header|chrome|surface|decorative|accent)$'
}

function Assert-FiniteTolerance {
  param([double]$Value, [string]$Name, [double]$Minimum = 0, [double]$Maximum = 1000)
  if ([double]::IsNaN($Value) -or [double]::IsInfinity($Value) -or $Value -lt $Minimum -or $Value -gt $Maximum) { throw "INVALID_LAYOUT_TOLERANCE:$Name=$Value" }
}

function Test-NestedShape {
  param([object]$Shape, [int]$SlideNumber, [string]$ParentLabel)
  $shapeName = "$ParentLabel/$([string]$Shape.Name)"
  $left = [double]$Shape.Left
  $top = [double]$Shape.Top
  $width = [double]$Shape.Width
  $height = [double]$Shape.Height
  if ([double]::IsNaN($left) -or [double]::IsInfinity($left) -or [double]::IsNaN($top) -or [double]::IsInfinity($top) -or [double]::IsNaN($width) -or [double]::IsInfinity($width) -or [double]::IsNaN($height) -or [double]::IsInfinity($height) -or $width -lt 0 -or $height -lt 0) {
    Add-Finding -Severity 'P1' -Code 'INVALID_OBJECT_GEOMETRY' -Slide $SlideNumber -Object $shapeName -Detail "bounds=$left,$top,$width,$height"
  }
  [void](Test-TextFrame -Shape $Shape -SlideNumber $SlideNumber -ObjectLabel $shapeName)
  $hasTable = $false
  try { $hasTable = $Shape.HasTable -eq $msoTrue } catch {}
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
            [void](Test-TextFrame -Shape $cellShape -SlideNumber $SlideNumber -ObjectLabel "$shapeName[$row,$column]")
          } finally {
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
          Test-NestedShape -Shape $groupItem -SlideNumber $SlideNumber -ParentLabel $shapeName
        } finally { Release-ComObject -Object $groupItem }
      }
    } finally { Release-ComObject -Object $groupItems }
  }
}

function Test-OverlapPair {
  param([object]$First, [object]$Second, [int]$SlideNumber)
  if ((Test-IntentionalOverlay -Name ([string]$First.name)) -or (Test-IntentionalOverlay -Name ([string]$Second.name))) { return }
  if (-not ($First.has_text -or $First.is_table -or $First.is_chart)) { return }
  if (-not ($Second.has_text -or $Second.is_table -or $Second.is_chart)) { return }
  $horizontal = [Math]::Min($First.right, $Second.right) - [Math]::Max($First.left, $Second.left)
  $vertical = [Math]::Min($First.bottom, $Second.bottom) - [Math]::Max($First.top, $Second.top)
  if ($horizontal -lt 4 -or $vertical -lt 4) { return }
  $intersection = $horizontal * $vertical
  $smallerArea = [Math]::Min(($First.right - $First.left) * ($First.bottom - $First.top), ($Second.right - $Second.left) * ($Second.bottom - $Second.top))
  if ($smallerArea -gt 0 -and ($intersection / $smallerArea) -ge 0.02) {
    Add-Finding -Severity 'P1' -Code 'UNINTENDED_OVERLAP' -Slide $SlideNumber -Object "$($First.name)|$($Second.name)" -Detail ("intersection={0:N1}pt² ratio={1:P1}" -f $intersection, ($intersection / $smallerArea))
  }
}

try {
  $resolvedDeck = Assert-RegularFilePath -Path $DeckPath -Label 'DECK'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedDeck) -Label 'AUDIT_OUTPUT')
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  Assert-FiniteTolerance -Value $TextTolerancePoints -Name 'text'
  Assert-FiniteTolerance -Value $CanvasTolerancePoints -Name 'canvas'
  Ensure-ParentDirectory -Path $resolvedOutput
  $reportReady = $true
  $sourceHashBefore = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  $powerPoint = New-Object -ComObject PowerPoint.Application
  Set-PowerPointSafeAutomation -Application $powerPoint
  $presentation = $powerPoint.Presentations.Open($resolvedDeck, $msoTrue, 0, 0)
  $slideWidth = [double]$presentation.PageSetup.SlideWidth
  $slideHeight = [double]$presentation.PageSetup.SlideHeight
  if ([double]::IsNaN($slideWidth) -or [double]::IsInfinity($slideWidth) -or [double]::IsNaN($slideHeight) -or [double]::IsInfinity($slideHeight) -or $slideWidth -le 0 -or $slideHeight -le 0) { throw 'INVALID_SLIDE_CANVAS' }
  $slideCount = [int]$presentation.Slides.Count
  if ($slideCount -lt 1) { throw 'DECK_CONTAINS_NO_SLIDES' }

  for ($slideIndex = 1; $slideIndex -le $slideCount; $slideIndex += 1) {
    $slide = $null
    $slideObjects = [System.Collections.Generic.List[object]]::new()
    try {
      $slide = $presentation.Slides.Item($slideIndex)
      for ($shapeIndex = 1; $shapeIndex -le $slide.Shapes.Count; $shapeIndex += 1) {
        $shape = $null
        try {
          $shape = $slide.Shapes.Item($shapeIndex)
          $name = [string]$shape.Name
          $left = [double]$shape.Left
          $top = [double]$shape.Top
          $width = [double]$shape.Width
          $height = [double]$shape.Height
          if ([double]::IsNaN($left) -or [double]::IsInfinity($left) -or [double]::IsNaN($top) -or [double]::IsInfinity($top) -or [double]::IsNaN($width) -or [double]::IsInfinity($width) -or [double]::IsNaN($height) -or [double]::IsInfinity($height) -or $width -lt 0 -or $height -lt 0) {
            Add-Finding -Severity 'P1' -Code 'INVALID_OBJECT_GEOMETRY' -Slide $slideIndex -Object $name -Detail "bounds=$left,$top,$width,$height"
          }
          $right = $left + [double]$shape.Width
          $bottom = $top + [double]$shape.Height
          if ($left -lt -$CanvasTolerancePoints -or $top -lt -$CanvasTolerancePoints -or $right -gt $slideWidth + $CanvasTolerancePoints -or $bottom -gt $slideHeight + $CanvasTolerancePoints) {
            Add-Finding -Severity 'P1' -Code 'OBJECT_OUTSIDE_CANVAS' -Slide $slideIndex -Object $name -Detail ("bounds=({0:N1},{1:N1})-({2:N1},{3:N1}); canvas={4:N1}x{5:N1}" -f $left,$top,$right,$bottom,$slideWidth,$slideHeight)
          }
          $textSnapshot = Test-TextFrame -Shape $shape -SlideNumber $slideIndex -ObjectLabel $name
          $isTable = $shape.HasTable -eq $msoTrue
          $isChart = $shape.HasChart -eq $msoTrue
          if ($shape.HasTable -eq $msoTrue) {
            $table = $null
            try {
              $table = $shape.Table
              for ($row = 1; $row -le $table.Rows.Count; $row += 1) {
                for ($column = 1; $column -le $table.Columns.Count; $column += 1) {
                  $cell = $null
                  $cellShape = $null
                  try {
                    $cell = $table.Cell($row, $column)
                    $cellShape = $cell.Shape
                    [void](Test-TextFrame -Shape $cellShape -SlideNumber $slideIndex -ObjectLabel "$name[$row,$column]")
                  } finally {
                    Release-ComObject -Object $cellShape
                    Release-ComObject -Object $cell
                  }
                }
              }
            } finally {
              Release-ComObject -Object $table
            }
          }
          $shapeType = 0
          try { $shapeType = [int]$shape.Type } catch {}
          if ($shapeType -eq $msoGroup) {
            $groupItems = $null
            try {
              $groupItems = $shape.GroupItems
              for ($itemIndex = 1; $itemIndex -le $groupItems.Count; $itemIndex += 1) {
                $groupItem = $null
                try {
                  $groupItem = $groupItems.Item($itemIndex)
                  Test-NestedShape -Shape $groupItem -SlideNumber $slideIndex -ParentLabel $name
                } finally { Release-ComObject -Object $groupItem }
              }
            } catch { Add-Finding -Severity 'P1' -Code 'GROUP_LAYOUT_INSPECTION_FAILED' -Slide $slideIndex -Object $name -Detail $_.Exception.Message } finally { Release-ComObject -Object $groupItems }
          }
          $slideObjects.Add([ordered]@{ name = $name; type = [int]$shape.Type; left = $left; top = $top; right = $right; bottom = $bottom; bounds = @($left,$top,$right,$bottom); has_text = $null -ne $textSnapshot; is_table = $isTable; is_chart = $isChart; text = $textSnapshot })
        } finally {
          Release-ComObject -Object $shape
        }
      }
      for ($firstIndex = 0; $firstIndex -lt $slideObjects.Count; $firstIndex += 1) {
        for ($secondIndex = $firstIndex + 1; $secondIndex -lt $slideObjects.Count; $secondIndex += 1) {
          Test-OverlapPair -First $slideObjects[$firstIndex] -Second $slideObjects[$secondIndex] -SlideNumber $slideIndex
        }
      }
      $slidesReport.Add([ordered]@{ slide = $slideIndex; shape_count = $slide.Shapes.Count; objects = @($slideObjects) })
    } finally {
      Release-ComObject -Object $slide
    }
  }

  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_LAYOUT_AUDIT' }
  $criticalCount = @($findings | Where-Object { $_.severity -in @('P0','P1') }).Count
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    deck_path = $resolvedDeck
    deck_sha256 = $sourceHashAfter
    deck_sha256_before = $sourceHashBefore
    deck_sha256_after = $sourceHashAfter
    status = if ($criticalCount -gt 0) { 'BLOCKED' } else { 'PASS' }
    slide_count = $presentation.Slides.Count
    slide_size_points = [ordered]@{ width = $slideWidth; height = $slideHeight }
    findings = @($findings)
    slides = @($slidesReport)
  }
  Write-JsonFileNew -Value $report -Path $resolvedOutput
  $report | ConvertTo-Json -Depth 30
  if ($report.status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isBlocked = $message -match '^(SOURCE_CHANGED|AUDIT_OUTPUT|INVALID_LAYOUT|INVALID_SLIDE|DECK_CONTAINS_NO_SLIDES|.*COLLISION|.*ALREADY_EXISTS|.*REPARSE_POINT)'
  $report = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); deck_path = if ($resolvedDeck) { $resolvedDeck } else { $DeckPath }; status = if ($isBlocked) { 'BLOCKED' } else { 'UNVERIFIED' }; error = $message; findings = @($findings) }
  if ($sourceHashBefore) { $report.deck_sha256_before = $sourceHashBefore }
  if ($sourceHashAfter) { $report.deck_sha256_after = $sourceHashAfter }
  if ($reportReady -and -not (Test-Path -LiteralPath $resolvedOutput)) { Write-JsonFileNew -Value $report -Path $resolvedOutput }
  [Console]::Error.WriteLine($message)
  exit $(if ($isBlocked) { 2 } else { 3 })
} finally {
  if ($presentation) { try { $presentation.Close() } catch {}; Release-ComObject -Object $presentation }
  if ($powerPoint) { try { $powerPoint.Quit() } catch {}; Release-ComObject -Object $powerPoint }
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}
