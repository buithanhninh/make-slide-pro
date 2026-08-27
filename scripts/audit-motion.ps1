param(
  [Parameter(Mandatory = $true)][string]$DeckPath,
  [Parameter(Mandatory = $true)][string]$OutputPath,
  [int]$MaximumEffectsPerSlide = 40
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$msoTrue = -1
$findings = [System.Collections.Generic.List[object]]::new()
$slides = [System.Collections.Generic.List[object]]::new()
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

function ConvertTo-FiniteDouble {
  param([object]$Value, [double]$Minimum, [double]$Maximum, [string]$Label)
  if ($null -eq $Value -or $Value -is [bool] -or $Value -is [string]) { throw "INVALID_NUMBER:$Label" }
  $candidate = 0.0
  if (-not [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate) -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or $candidate -lt $Minimum -or $candidate -gt $Maximum) { throw "INVALID_NUMBER:$Label" }
  return $candidate
}

try {
  $resolvedDeck = Assert-RegularFilePath -Path $DeckPath -Label 'DECK'
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($resolvedDeck) -Label 'AUDIT_OUTPUT')
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  if ($MaximumEffectsPerSlide -lt 1 -or $MaximumEffectsPerSlide -gt 100) { throw 'INVALID_MAXIMUM_EFFECTS_PER_SLIDE' }
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
    $sequence = $null
    $transition = $null
    try {
      $slide = $presentation.Slides.Item($slideIndex)
      $sequence = $slide.TimeLine.MainSequence
      $transition = $slide.SlideShowTransition
      $effectCount = [int]$sequence.Count
      $advanceOnTime = [bool]$transition.AdvanceOnTime
      $advanceOnClick = [bool]$transition.AdvanceOnClick
      $advanceTime = ConvertTo-FiniteDouble -Value $transition.AdvanceTime -Minimum 0 -Maximum 86400 -Label "advance_time:slide=$slideIndex"
      if ($advanceOnTime) { Add-Finding -Severity 'P0' -Code 'ACCIDENTAL_AUTO_ADVANCE' -Slide $slideIndex -Object '' -Detail "AdvanceTime=$advanceTime" }
      if (-not $advanceOnClick) { Add-Finding -Severity 'P1' -Code 'CLICK_ADVANCE_DISABLED' -Slide $slideIndex -Object '' -Detail 'AdvanceOnClick=false' }
      if ($advanceTime -gt 0) { Add-Finding -Severity 'P1' -Code 'HIDDEN_ADVANCE_TIME' -Slide $slideIndex -Object '' -Detail "AdvanceTime=$advanceTime" }
      if ($effectCount -gt $MaximumEffectsPerSlide) { Add-Finding -Severity 'P1' -Code 'EXCESSIVE_EFFECT_COUNT' -Slide $slideIndex -Object '' -Detail "effects=$effectCount limit=$MaximumEffectsPerSlide" }
      $effects = [System.Collections.Generic.List[object]]::new()
      for ($effectIndex = 1; $effectIndex -le $effectCount; $effectIndex += 1) {
        $effect = $null
        $effectShape = $null
        try {
          $effect = $sequence.Item($effectIndex)
          $shapeName = ''
          try {
            $effectShape = $effect.Shape
            $shapeName = [string]$effectShape.Name
          } catch {
            Add-Finding -Severity 'P1' -Code 'MOTION_SHAPE_MISSING' -Slide $slideIndex -Object '' -Detail "effect=$effectIndex"
          }
          if ([string]::IsNullOrWhiteSpace($shapeName)) { Add-Finding -Severity 'P1' -Code 'MOTION_SHAPE_MISSING' -Slide $slideIndex -Object '' -Detail "effect=$effectIndex" }
          $duration = ConvertTo-FiniteDouble -Value $effect.Timing.Duration -Minimum 0.001 -Maximum 10 -Label "duration:slide=$slideIndex;effect=$effectIndex"
          $delay = ConvertTo-FiniteDouble -Value $effect.Timing.TriggerDelayTime -Minimum 0 -Maximum 10 -Label "delay:slide=$slideIndex;effect=$effectIndex"
          $triggerType = [int]$effect.Timing.TriggerType
          if ($triggerType -notin @(1, 2, 3)) { Add-Finding -Severity 'P1' -Code 'MOTION_TRIGGER_INVALID' -Slide $slideIndex -Object $shapeName -Detail "trigger=$triggerType" }
          $effects.Add([ordered]@{ index = $effectIndex; shape = $shapeName; effect_type = [int]$effect.EffectType; trigger_type = $triggerType; duration = $duration; delay = $delay })
        } catch {
          if ($_.Exception.Message -match '^INVALID_NUMBER:') { Add-Finding -Severity 'P1' -Code 'MOTION_TIMING_INVALID' -Slide $slideIndex -Object '' -Detail $_.Exception.Message }
          else { throw }
        } finally {
          Release-ComObject -Object $effectShape
          Release-ComObject -Object $effect
        }
      }
      $slides.Add([ordered]@{ slide = $slideIndex; effect_count = $effectCount; transition = [int]$transition.EntryEffect; advance_on_click = $advanceOnClick; advance_on_time = $advanceOnTime; advance_time = $advanceTime; effects = @($effects) })
    } finally {
      Release-ComObject -Object $transition
      Release-ComObject -Object $sequence
      Release-ComObject -Object $slide
    }
  }
  $sourceHashAfter = (Get-FileHash -LiteralPath $resolvedDeck -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($sourceHashBefore -ne $sourceHashAfter) { throw 'SOURCE_CHANGED_DURING_MOTION_AUDIT' }
  $criticalCount = @($findings | Where-Object { $_.severity -in @('P0', 'P1') }).Count
  $report = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    deck_path = $resolvedDeck
    deck_sha256_before = $sourceHashBefore
    deck_sha256_after = $sourceHashAfter
    status = if ($criticalCount -gt 0) { 'BLOCKED' } else { 'PASS' }
    slide_count = $slideCount
    maximum_effects_per_slide = $MaximumEffectsPerSlide
    findings = @($findings)
    slides = @($slides)
  }
  Write-JsonFileNew -Value $report -Path $resolvedOutput
  $report | ConvertTo-Json -Depth 30
  if ($report.status -eq 'BLOCKED') { exit 2 }
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $isBlocked = $message -match '^(SOURCE_CHANGED|AUDIT_OUTPUT|INVALID_MAXIMUM|INVALID_NUMBER|.*COLLISION|.*ALREADY_EXISTS|.*REPARSE_POINT|DECK_CONTAINS_NO_SLIDES)'
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
