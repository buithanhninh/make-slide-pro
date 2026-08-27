$ErrorActionPreference = 'Stop'
$skillRoot = if ($env:MAKE_SLIDE_PRO_ROOT) { $env:MAKE_SLIDE_PRO_ROOT } else { (Resolve-Path (Join-Path $PSScriptRoot '..')).Path }
$auditScript = Join-Path $skillRoot 'scripts\audit-native-layout.ps1'
if (-not (Test-Path -LiteralPath $auditScript)) {
  throw "Missing audit script: $auditScript"
}

$workspace = Join-Path ([System.IO.Path]::GetTempPath()) ("make-slide-pro-layout-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $workspace | Out-Null
$badDeck = Join-Path $workspace 'bad-layout.pptx'
$goodDeck = Join-Path $workspace 'good-layout.pptx'
$badReport = Join-Path $workspace 'bad-report.json'
$goodReport = Join-Path $workspace 'good-report.json'
$autoDeck = Join-Path $workspace 'auto-advance.pptx'
$motionReport = Join-Path $workspace 'motion-report.json'
$typeDeck = Join-Path $workspace 'wrapped-title.pptx'
$typeReport = Join-Path $workspace 'type-report.json'
$pdfPath = Join-Path $workspace 'good-layout.pdf'
$pdfReport = Join-Path $workspace 'pdf-report.json'

$powerPoint = $null
$badPresentation = $null
$goodPresentation = $null
$autoPresentation = $null
$typePresentation = $null
try {
  $powerPoint = New-Object -ComObject PowerPoint.Application
  $powerPoint.Visible = 1

  $badPresentation = $powerPoint.Presentations.Add()
  $badSlide = $badPresentation.Slides.Add(1, 12)
  $badShape = $badSlide.Shapes.AddTextbox(1, 40, 40, 80, 18)
  $badShape.TextFrame2.AutoSize = 0
  $badShape.TextFrame2.WordWrap = -1
  $badShape.TextFrame2.TextRange.Text = 'Nội dung rất dài chắc chắn tràn khỏi hộp chữ nhỏ.'
  $badShape.TextFrame2.TextRange.Font.Size = 28
  $badPresentation.SaveAs($badDeck)
  $badPresentation.Close()
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($badShape)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($badSlide)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($badPresentation)
  $badPresentation = $null

  $goodPresentation = $powerPoint.Presentations.Add()
  $goodSlide = $goodPresentation.Slides.Add(1, 12)
  $goodShape = $goodSlide.Shapes.AddTextbox(1, 40, 40, 520, 80)
  $goodShape.TextFrame2.AutoSize = 0
  $goodShape.TextFrame2.WordWrap = -1
  $goodShape.TextFrame2.TextRange.Text = 'Nội dung nằm cân trong hộp chữ.'
  $goodShape.TextFrame2.TextRange.Font.Size = 24
  $goodPresentation.SaveAs($goodDeck)
  $goodPresentation.Close()
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($goodShape)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($goodSlide)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($goodPresentation)
  $goodPresentation = $null

  $autoPresentation = $powerPoint.Presentations.Add()
  $autoSlide = $autoPresentation.Slides.Add(1, 12)
  $autoSlide.SlideShowTransition.AdvanceOnClick = -1
  $autoSlide.SlideShowTransition.AdvanceOnTime = -1
  $autoSlide.SlideShowTransition.AdvanceTime = 2
  $autoPresentation.SaveAs($autoDeck)
  $autoPresentation.Close()
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($autoSlide)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($autoPresentation)
  $autoPresentation = $null

  $typePresentation = $powerPoint.Presentations.Add()
  $typeSlide = $typePresentation.Slides.Add(1, 12)
  $typeShape = $typeSlide.Shapes.AddTextbox(1, 40, 40, 700, 100)
  $typeShape.Name = 'A01_TITLE'
  $typeShape.TextFrame2.TextRange.Text = "Chiến lược tăng trưởng`rđến năm 2030"
  $typeShape.TextFrame2.TextRange.Font.Name = 'Arial'
  $typeShape.TextFrame2.TextRange.Font.Size = 20
  $typePresentation.SaveAs($typeDeck)
  $typePresentation.Close()
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($typeShape)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($typeSlide)
  [void][Runtime.InteropServices.Marshal]::ReleaseComObject($typePresentation)
  $typePresentation = $null
} finally {
  if ($badPresentation) { $badPresentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($badPresentation) }
  if ($goodPresentation) { $goodPresentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($goodPresentation) }
  if ($autoPresentation) { $autoPresentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($autoPresentation) }
  if ($typePresentation) { $typePresentation.Close(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($typePresentation) }
  if ($powerPoint) { $powerPoint.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint) }
}

$pwsh = (Get-Command pwsh).Source
& $pwsh -NoLogo -NoProfile -File $auditScript -DeckPath $badDeck -OutputPath $badReport
if ($LASTEXITCODE -ne 2) { throw "Bad deck should exit 2, got $LASTEXITCODE" }
$bad = Get-Content -LiteralPath $badReport -Raw | ConvertFrom-Json
if ($bad.status -ne 'BLOCKED') { throw 'Bad deck should be BLOCKED.' }
if (-not ($bad.findings | Where-Object code -eq 'TEXT_OVERFLOW')) { throw 'Bad deck missing TEXT_OVERFLOW finding.' }

& $pwsh -NoLogo -NoProfile -File $auditScript -DeckPath $goodDeck -OutputPath $goodReport
if ($LASTEXITCODE -ne 0) { throw "Good deck should exit 0, got $LASTEXITCODE" }
$good = Get-Content -LiteralPath $goodReport -Raw | ConvertFrom-Json
if ($good.status -ne 'PASS') { throw 'Good deck should PASS.' }

$renderPdfScript = Join-Path $skillRoot 'scripts\render-pdf.ps1'
& $pwsh -NoLogo -NoProfile -File $renderPdfScript -DeckPath $goodDeck -OutputPath $pdfPath -ReportPath $pdfReport
if ($LASTEXITCODE -ne 0) { throw "Native PDF render should exit 0, got $LASTEXITCODE" }
$pdf = Get-Content -LiteralPath $pdfReport -Raw | ConvertFrom-Json
if ($pdf.status -ne 'PASS') { throw 'Native PDF render should PASS.' }
if (-not (Test-Path -LiteralPath $pdfPath -PathType Leaf)) { throw 'Native PDF render output missing.' }
$pdfBytes = [System.IO.File]::ReadAllBytes($pdfPath)
if ($pdfBytes.Length -lt 5 -or [System.Text.Encoding]::ASCII.GetString($pdfBytes, 0, 5) -ne '%PDF-') { throw 'Native PDF render output signature invalid.' }
if ($pdf.source_sha256_before -ne $pdf.source_sha256_after) { throw 'Native PDF render changed source deck.' }

$motionScript = Join-Path $skillRoot 'scripts\audit-motion.ps1'
& $pwsh -NoLogo -NoProfile -File $motionScript -DeckPath $autoDeck -OutputPath $motionReport
if ($LASTEXITCODE -ne 2) { throw "Auto-advance deck should exit 2, got $LASTEXITCODE" }
$motion = Get-Content -LiteralPath $motionReport -Raw | ConvertFrom-Json
if (-not ($motion.findings | Where-Object code -eq 'ACCIDENTAL_AUTO_ADVANCE')) { throw 'Auto-advance deck missing ACCIDENTAL_AUTO_ADVANCE finding.' }

$typographyScript = Join-Path $skillRoot 'scripts\audit-typography.ps1'
& $pwsh -NoLogo -NoProfile -File $typographyScript -DeckPath $typeDeck -OutputPath $typeReport -AllowedFonts 'Arial'
if ($LASTEXITCODE -ne 2) { throw "Wrapped title deck should exit 2, got $LASTEXITCODE" }
$type = Get-Content -LiteralPath $typeReport -Raw | ConvertFrom-Json
if (-not ($type.findings | Where-Object code -eq 'TITLE_WRAP_RISK')) { throw 'Wrapped title deck missing TITLE_WRAP_RISK finding.' }
$smallTitle = @($type.findings | Where-Object code -eq 'FONT_TOO_SMALL' | Where-Object object -eq 'A01_TITLE')
if ($smallTitle.Count -ne 1 -or $smallTitle[0].severity -ne 'P1') { throw 'Small title must produce one P1 FONT_TOO_SMALL finding.' }

Remove-Item -LiteralPath $workspace -Recurse -Force
Write-Output 'Native layout tests passed.'
