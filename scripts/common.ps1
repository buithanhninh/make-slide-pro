Set-StrictMode -Version Latest

$script:MakeSlideProUtf8 = [System.Text.UTF8Encoding]::new($false)
$script:MakeSlideProPathComparison = if ($PSVersionTable.Platform -eq 'Win32NT' -or $env:OS -eq 'Windows_NT') { [System.StringComparison]::OrdinalIgnoreCase } else { [System.StringComparison]::Ordinal }

function Get-NormalizedFullPath {
  param([Parameter(Mandatory = $true)][string]$Path)
  $fullPath = [System.IO.Path]::GetFullPath($Path)
  $root = [System.IO.Path]::GetPathRoot($fullPath)
  if ($root -and $fullPath.Equals($root, $script:MakeSlideProPathComparison)) { return $root }
  return $fullPath.TrimEnd([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
}

function Test-PathsEqual {
  param(
    [Parameter(Mandatory = $true)][string]$FirstPath,
    [Parameter(Mandatory = $true)][string]$SecondPath
  )
  $first = Get-NormalizedFullPath -Path $FirstPath
  $second = Get-NormalizedFullPath -Path $SecondPath
  return $first.Equals($second, $script:MakeSlideProPathComparison)
}

function Test-StrictProperty {
  param([Parameter(Mandatory = $true)][object]$Object, [Parameter(Mandatory = $true)][string]$Name)
  if ($Object -is [System.Collections.IDictionary]) { return $Object.Contains($Name) }
  return $null -ne $Object.PSObject.Properties[$Name]
}

function Get-StrictPropertyValue {
  param([Parameter(Mandatory = $true)][object]$Object, [Parameter(Mandatory = $true)][string]$Name)
  if ($Object -is [System.Collections.IDictionary]) {
    if ($Object.Contains($Name)) { return $Object[$Name] }
    return $null
  }
  $property = $Object.PSObject.Properties[$Name]
  if ($null -ne $property) { return $property.Value }
  return $null
}

function Test-PathInsideDirectory {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [Parameter(Mandatory = $true)][string]$Directory
  )
  $candidate = Get-NormalizedFullPath -Path $Path
  $root = (Get-NormalizedFullPath -Path $Directory) + [System.IO.Path]::DirectorySeparatorChar
  return $candidate.StartsWith($root, $script:MakeSlideProPathComparison)
}

function Assert-NewOutputPath {
  param(
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [string[]]$ProtectedPaths = @(),
    [string]$Label = 'OUTPUT'
  )
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  Assert-NoReparseAncestors -Path $resolvedOutput
  foreach ($protectedPath in @($ProtectedPaths | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) })) {
    if (Test-PathsEqual -FirstPath $resolvedOutput -SecondPath $protectedPath) {
      throw "${Label}_PATH_COLLISION:$resolvedOutput"
    }
  }
  if (Test-Path -LiteralPath $resolvedOutput) {
    throw "${Label}_ALREADY_EXISTS:$resolvedOutput"
  }
  return $resolvedOutput
}

function Assert-OutputPathDistinct {
  param(
    [Parameter(Mandatory = $true)][string]$OutputPath,
    [string[]]$ProtectedPaths = @(),
    [string]$Label = 'OUTPUT'
  )
  $resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
  Assert-NoReparseAncestors -Path $resolvedOutput
  foreach ($protectedPath in @($ProtectedPaths | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) })) {
    if (Test-PathsEqual -FirstPath $resolvedOutput -SecondPath $protectedPath) {
      throw "${Label}_PATH_COLLISION:$resolvedOutput"
    }
  }
  return $resolvedOutput
}

function Assert-NoReparseAncestors {
  param([Parameter(Mandatory = $true)][string]$Path)
  $current = Get-NormalizedFullPath -Path $Path
  while ($current) {
    if (Test-Path -LiteralPath $current) {
      $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
      if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
        throw "PATH_REPARSE_POINT_NOT_ALLOWED:$current"
      }
    }
    $parent = [System.IO.Path]::GetDirectoryName($current)
    if ([string]::IsNullOrEmpty($parent) -or $parent.Equals($current, $script:MakeSlideProPathComparison)) { break }
    $current = $parent
  }
}

function Assert-RegularFilePath {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [string]$Label = 'FILE'
  )
  $resolved = Get-NormalizedFullPath -Path $Path
  Assert-NoReparseAncestors -Path $resolved
  if (-not (Test-Path -LiteralPath $resolved -PathType Leaf)) { throw "${Label}_MISSING:$resolved" }
  $item = Get-Item -LiteralPath $resolved -Force -ErrorAction Stop
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "${Label}_REPARSE_POINT_NOT_ALLOWED:$resolved" }
  return $resolved
}

function Ensure-ParentDirectory {
  param([Parameter(Mandatory = $true)][string]$Path)
  $parent = Split-Path -Parent $Path
  if ($parent) {
    Assert-NoReparseAncestors -Path $parent
    [System.IO.Directory]::CreateDirectory($parent) | Out-Null
    Assert-NoReparseAncestors -Path $parent
  }
}

function Assert-MutableJsonTargetSafe {
  param([Parameter(Mandatory = $true)][string]$Path)
  $resolvedPath = Get-NormalizedFullPath -Path $Path
  Assert-NoReparseAncestors -Path $resolvedPath
  if (Test-Path -LiteralPath $resolvedPath) {
    $item = Get-Item -LiteralPath $resolvedPath -Force -ErrorAction Stop
    if ($item.PSIsContainer) { throw "MUTABLE_JSON_TARGET_NOT_FILE:$resolvedPath" }
  }
  return $resolvedPath
}

function Write-JsonFileMutable {
  param(
    [Parameter(Mandatory = $true)][object]$Value,
    [Parameter(Mandatory = $true)][string]$Path,
    [int]$Depth = 30
  )
  $resolvedPath = Get-NormalizedFullPath -Path $Path
  Ensure-ParentDirectory -Path $resolvedPath
  [void](Assert-MutableJsonTargetSafe -Path $resolvedPath)
  $json = $Value | ConvertTo-Json -Depth $Depth
  $parent = [System.IO.Path]::GetDirectoryName($resolvedPath)
  $temporaryPath = Join-Path $parent ('.' + [System.IO.Path]::GetFileName($resolvedPath) + '.tmp-' + [guid]::NewGuid().ToString('N'))
  $stream = $null
  try {
    $stream = [System.IO.File]::Open($temporaryPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    $writer = [System.IO.StreamWriter]::new($stream, $script:MakeSlideProUtf8)
    try { $writer.Write($json); $writer.Flush() } finally { $writer.Dispose(); $stream = $null }
    [void](Assert-RegularFilePath -Path $temporaryPath -Label 'MUTABLE_JSON_TEMP')
    [void](Assert-MutableJsonTargetSafe -Path $resolvedPath)
    [System.IO.File]::Move($temporaryPath, $resolvedPath, $true)
    [void](Assert-RegularFilePath -Path $resolvedPath -Label 'MUTABLE_JSON_TARGET')
  } finally {
    if ($stream) { $stream.Dispose() }
    if (Test-Path -LiteralPath $temporaryPath) {
      try {
        $temporaryItem = Get-Item -LiteralPath $temporaryPath -Force -ErrorAction Stop
        if (-not $temporaryItem.PSIsContainer -and ($temporaryItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) {
          [System.IO.File]::Delete($temporaryPath)
        }
      } catch {}
    }
  }
}

function Write-JsonFileNew {
  param(
    [Parameter(Mandatory = $true)][object]$Value,
    [Parameter(Mandatory = $true)][string]$Path,
    [int]$Depth = 30
  )
  $resolvedPath = Get-NormalizedFullPath -Path $Path
  Ensure-ParentDirectory -Path $resolvedPath
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedPath))
  $json = $Value | ConvertTo-Json -Depth $Depth
  $stream = $null
  try {
    $stream = [System.IO.File]::Open($resolvedPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    $writer = [System.IO.StreamWriter]::new($stream, $script:MakeSlideProUtf8)
    try { $writer.Write($json); $writer.Flush() } finally { $writer.Dispose(); $stream = $null }
  } finally {
    if ($stream) { $stream.Dispose() }
  }
}

function Write-TextFileNew {
  param(
    [Parameter(Mandatory = $true)][AllowEmptyString()][string]$Text,
    [Parameter(Mandatory = $true)][string]$Path
  )
  $resolvedPath = Get-NormalizedFullPath -Path $Path
  Ensure-ParentDirectory -Path $resolvedPath
  [void](Assert-NewOutputPath -OutputPath $resolvedPath -Label 'TEXT_OUTPUT')
  $parent = [System.IO.Path]::GetDirectoryName($resolvedPath)
  $temporaryPath = Join-Path $parent ('.' + [System.IO.Path]::GetFileName($resolvedPath) + '.tmp-' + [guid]::NewGuid().ToString('N'))
  $stream = $null
  try {
    $stream = [System.IO.File]::Open($temporaryPath, [System.IO.FileMode]::CreateNew, [System.IO.FileAccess]::Write, [System.IO.FileShare]::None)
    $writer = [System.IO.StreamWriter]::new($stream, $script:MakeSlideProUtf8)
    try { $writer.Write($Text); $writer.Flush() } finally { $writer.Dispose(); $stream = $null }
    [void](Assert-RegularFilePath -Path $temporaryPath -Label 'TEXT_OUTPUT_TEMP')
    [void](Assert-NewOutputPath -OutputPath $resolvedPath -Label 'TEXT_OUTPUT')
    [System.IO.File]::Move($temporaryPath, $resolvedPath, $false)
    [void](Assert-RegularFilePath -Path $resolvedPath -Label 'TEXT_OUTPUT')
  } finally {
    if ($stream) { $stream.Dispose() }
    if (Test-Path -LiteralPath $temporaryPath) {
      try {
        $temporaryItem = Get-Item -LiteralPath $temporaryPath -Force -ErrorAction Stop
        if (-not $temporaryItem.PSIsContainer -and ($temporaryItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq 0) {
          [System.IO.File]::Delete($temporaryPath)
        }
      } catch {}
    }
  }
}

function Read-JsonFile {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [long]$MaximumBytes = 67108864
  )
  $resolvedPath = Assert-RegularFilePath -Path $Path -Label 'JSON'
  $inputSize = [long](Get-Item -LiteralPath $resolvedPath -Force -ErrorAction Stop).Length
  if ($inputSize -gt $MaximumBytes) { throw "JSON_INPUT_TOO_LARGE:${inputSize}:limit=$MaximumBytes" }
  $rawJson = [System.IO.File]::ReadAllText($resolvedPath, [System.Text.Encoding]::UTF8)
  $document = $null
  try {
    $options = [System.Text.Json.JsonDocumentOptions]::new()
    $options.AllowTrailingCommas = $false
    $options.CommentHandling = [System.Text.Json.JsonCommentHandling]::Disallow
    $options.MaxDepth = 128
    $document = [System.Text.Json.JsonDocument]::Parse($rawJson, $options)
    Test-JsonElementStrict -Element $document.RootElement -JsonPath '$'
  } catch {
    throw "INVALID_JSON:${resolvedPath}:$($_.Exception.Message)"
  } finally {
    if ($document) { $document.Dispose() }
  }
  return $rawJson | ConvertFrom-Json -Depth 128
}

function ConvertTo-NativeReportInteger {
  param(
    [object]$Value,
    [int]$Minimum,
    [int]$Maximum,
    [string]$ErrorCode
  )
  if ($null -eq $Value -or $Value -is [bool] -or $Value -is [string]) { throw $ErrorCode }
  $candidate = 0.0
  if (-not [double]::TryParse([string]$Value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$candidate) -or [double]::IsNaN($candidate) -or [double]::IsInfinity($candidate) -or [Math]::Truncate($candidate) -ne $candidate -or $candidate -lt $Minimum -or $candidate -gt $Maximum) {
    throw $ErrorCode
  }
  return [int]$candidate
}

function Assert-NativeReportFindings {
  param(
    [object]$Findings,
    [string]$InvalidErrorCode,
    [string]$CriticalErrorCode
  )
  if ($Findings -isnot [System.Array]) { throw $InvalidErrorCode }
  foreach ($finding in @($Findings)) {
    if ($null -eq $finding -or $finding -is [System.Array] -or $finding -is [string] -or $finding -is [ValueType]) { throw $InvalidErrorCode }
    if (-not (Test-StrictProperty -Object $finding -Name 'severity') -or -not (Test-StrictProperty -Object $finding -Name 'code') -or -not (Test-StrictProperty -Object $finding -Name 'detail')) { throw $InvalidErrorCode }
    $severityValue = Get-StrictPropertyValue -Object $finding -Name 'severity'
    $codeValue = Get-StrictPropertyValue -Object $finding -Name 'code'
    $detailValue = Get-StrictPropertyValue -Object $finding -Name 'detail'
    if ($severityValue -isnot [string] -or $severityValue -notin @('P0', 'P1', 'P2', 'P3', 'INFO')) { throw $InvalidErrorCode }
    if ($codeValue -isnot [string] -or [string]$codeValue -notmatch '^[A-Z][A-Z0-9_]{2,}$') { throw $InvalidErrorCode }
    if ($detailValue -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$detailValue)) { throw $InvalidErrorCode }
    if (Test-StrictProperty -Object $finding -Name 'slide') {
      $slideValue = Get-StrictPropertyValue -Object $finding -Name 'slide'
      if ($null -ne $slideValue -and $slideValue -isnot [int] -and $slideValue -isnot [long] -and $slideValue -isnot [double]) { throw $InvalidErrorCode }
      if ($null -ne $slideValue) { [void](ConvertTo-NativeReportInteger -Value $slideValue -Minimum 1 -Maximum 100000 -ErrorCode $InvalidErrorCode) }
    }
    if (Test-StrictProperty -Object $finding -Name 'object') {
      $objectValue = Get-StrictPropertyValue -Object $finding -Name 'object'
      if ($null -ne $objectValue -and $objectValue -isnot [string]) { throw $InvalidErrorCode }
    }
    if (Test-StrictProperty -Object $finding -Name 'evidence') {
      $evidenceValue = Get-StrictPropertyValue -Object $finding -Name 'evidence'
      if ($evidenceValue -isnot [System.Array] -or @($evidenceValue | Where-Object { $_ -isnot [string] -or [string]::IsNullOrWhiteSpace([string]$_) }).Count -gt 0) { throw $InvalidErrorCode }
    }
    if (Test-StrictProperty -Object $finding -Name 'status') {
      $statusValue = Get-StrictPropertyValue -Object $finding -Name 'status'
      if ($statusValue -isnot [string] -or $statusValue -notin @('OPEN', 'RESOLVED', 'ACCEPTED', 'WAIVED')) { throw $InvalidErrorCode }
    }
    $severity = [string]$severityValue
    if ($severity -in @('P0', 'P1')) { throw $CriticalErrorCode }
  }
}

function Assert-NativeVisualCoverageBinding {
  param(
    [Parameter(Mandatory = $true)][object]$Metadata,
    [Parameter(Mandatory = $true)][string]$ExpectedDeckPath,
    [Parameter(Mandatory = $true)][string]$ExpectedDeckHash,
    [string]$Label = 'visual_assets_verified'
  )
  if ($null -eq $Metadata -or $Metadata -is [System.Array] -or $Metadata -is [string] -or $Metadata -is [ValueType]) { throw "NATIVE_VISUAL_BINDING_MISSING:$Label" }
  $allowedFields = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::Ordinal)
  foreach ($fieldName in @('native_bindings_verified', 'native_visual_coverage_report_path', 'native_visual_coverage_report_sha256', 'native_visual_coverage_deck_sha256')) { [void]$allowedFields.Add($fieldName) }
  $metadataFieldNames = if ($Metadata -is [System.Collections.IDictionary]) { @($Metadata.Keys | ForEach-Object { [string]$_ }) } else { @($Metadata.PSObject.Properties | ForEach-Object { [string]$_.Name }) }
  foreach ($fieldName in $metadataFieldNames) {
    if (-not $allowedFields.Contains($fieldName)) { throw "NATIVE_VISUAL_BINDING_UNKNOWN_FIELD:${Label}:$fieldName" }
  }
  $nativeBindingsVerifiedValue = Get-StrictPropertyValue -Object $Metadata -Name 'native_bindings_verified'
  if (-not (Test-StrictProperty -Object $Metadata -Name 'native_bindings_verified') -or $nativeBindingsVerifiedValue -isnot [bool] -or -not [bool]$nativeBindingsVerifiedValue) { throw "NATIVE_VISUAL_BINDING_NOT_VERIFIED:$Label" }
  $reportPathValue = if (Test-StrictProperty -Object $Metadata -Name 'native_visual_coverage_report_path') { [string](Get-StrictPropertyValue -Object $Metadata -Name 'native_visual_coverage_report_path') } else { '' }
  $reportHashValue = if (Test-StrictProperty -Object $Metadata -Name 'native_visual_coverage_report_sha256') { [string](Get-StrictPropertyValue -Object $Metadata -Name 'native_visual_coverage_report_sha256') } else { '' }
  $reportDeckHashValue = if (Test-StrictProperty -Object $Metadata -Name 'native_visual_coverage_deck_sha256') { [string](Get-StrictPropertyValue -Object $Metadata -Name 'native_visual_coverage_deck_sha256') } else { '' }
  if ([string]::IsNullOrWhiteSpace($reportPathValue) -or $reportHashValue -notmatch '^[0-9a-fA-F]{64}$' -or $reportDeckHashValue -notmatch '^[0-9a-fA-F]{64}$') { throw "NATIVE_VISUAL_BINDING_INVALID:$Label" }
  if ($reportDeckHashValue -ine $ExpectedDeckHash) { throw "NATIVE_VISUAL_COVERAGE_DECK_HASH_MISMATCH:$Label" }
  $reportPath = Assert-RegularFilePath -Path $reportPathValue -Label "NATIVE_VISUAL_COVERAGE_REPORT_$Label"
  $actualReportHash = (Get-FileHash -LiteralPath $reportPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actualReportHash -ine $reportHashValue) { throw "NATIVE_VISUAL_COVERAGE_REPORT_HASH_MISMATCH:$Label" }
  $coverage = Read-JsonFile -Path $reportPath
  if ($null -eq $coverage -or $coverage -is [System.Array] -or $coverage -is [string] -or $coverage -is [ValueType]) { throw "NATIVE_VISUAL_COVERAGE_REPORT_INVALID:$Label" }
  if (-not $coverage.PSObject.Properties['schema_version'] -or [string]$coverage.schema_version -ne '1.0') { throw "NATIVE_VISUAL_COVERAGE_SCHEMA_VERSION_INVALID:$Label" }
  if ([string]$coverage.status -ne 'PASS' -or $coverage.native_bindings_required -isnot [bool] -or -not [bool]$coverage.native_bindings_required -or $coverage.native_bindings_verified -isnot [bool] -or -not [bool]$coverage.native_bindings_verified) { throw "NATIVE_VISUAL_COVERAGE_NOT_PASS:$Label" }
  Assert-NativeReportFindings -Findings $coverage.findings -InvalidErrorCode "NATIVE_VISUAL_COVERAGE_FINDINGS_INVALID:$Label" -CriticalErrorCode "NATIVE_VISUAL_COVERAGE_CRITICAL_FINDINGS:$Label"
  $coverageSlideCount = ConvertTo-NativeReportInteger -Value $coverage.slide_count -Minimum 1 -Maximum 100000 -ErrorCode "NATIVE_VISUAL_COVERAGE_SLIDE_COUNT_INVALID:$Label"
  $blueprintsPathValue = if ($coverage.PSObject.Properties['blueprints_path']) { [string]$coverage.blueprints_path } else { '' }
  $blueprintsHashValue = if ($coverage.PSObject.Properties['blueprints_sha256']) { [string]$coverage.blueprints_sha256 } else { '' }
  if ([string]::IsNullOrWhiteSpace($blueprintsPathValue) -or $blueprintsHashValue -notmatch '^[0-9a-fA-F]{64}$') { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_BINDING_MISSING:$Label" }
  $resolvedBlueprintsPath = Assert-RegularFilePath -Path $blueprintsPathValue -Label "NATIVE_VISUAL_BLUEPRINTS_$Label"
  if ((Get-FileHash -LiteralPath $resolvedBlueprintsPath -Algorithm SHA256).Hash.ToLowerInvariant() -ine $blueprintsHashValue) { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_HASH_MISMATCH:$Label" }
  $blueprints = Read-JsonFile -Path $resolvedBlueprintsPath
  if ($null -eq $blueprints -or $blueprints -is [System.Array] -or $blueprints -is [string] -or $blueprints -is [ValueType] -or [string]$blueprints.schema_version -ne '1.0' -or $blueprints.slides -isnot [System.Array]) { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_INVALID:$Label" }
  if (@($blueprints.slides).Count -ne $coverageSlideCount) { throw "NATIVE_VISUAL_COVERAGE_SLIDE_COUNT_MISMATCH:$Label" }
  $blueprintSlideNumbers = [System.Collections.Generic.HashSet[int]]::new()
  foreach ($blueprintSlide in @($blueprints.slides)) {
    if ($null -eq $blueprintSlide -or $blueprintSlide -is [System.Array] -or $blueprintSlide -is [string] -or $blueprintSlide -is [ValueType]) { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_INVALID:$Label" }
    $blueprintSlideNumber = ConvertTo-NativeReportInteger -Value $blueprintSlide.slide_number -Minimum 1 -Maximum $coverageSlideCount -ErrorCode "NATIVE_VISUAL_COVERAGE_BLUEPRINT_SEQUENCE_INVALID:$Label"
    if (-not $blueprintSlideNumbers.Add($blueprintSlideNumber)) { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_SEQUENCE_INVALID:$Label" }
  }
  for ($slideNumber = 1; $slideNumber -le $coverageSlideCount; $slideNumber += 1) {
    if (-not $blueprintSlideNumbers.Contains($slideNumber)) { throw "NATIVE_VISUAL_COVERAGE_BLUEPRINT_SEQUENCE_INVALID:$Label" }
  }
  $assetsPathValue = if ($coverage.PSObject.Properties['assets_path']) { [string]$coverage.assets_path } else { '' }
  $assetsHashValue = if ($coverage.PSObject.Properties['assets_sha256']) { [string]$coverage.assets_sha256 } else { '' }
  if ([string]::IsNullOrWhiteSpace($assetsPathValue) -or $assetsHashValue -notmatch '^[0-9a-fA-F]{64}$') { throw "NATIVE_VISUAL_COVERAGE_ASSETS_BINDING_MISSING:$Label" }
  $resolvedAssetsPath = Assert-RegularFilePath -Path $assetsPathValue -Label "NATIVE_VISUAL_ASSETS_$Label"
  if ((Get-FileHash -LiteralPath $resolvedAssetsPath -Algorithm SHA256).Hash.ToLowerInvariant() -ine $assetsHashValue) { throw "NATIVE_VISUAL_COVERAGE_ASSETS_HASH_MISMATCH:$Label" }
  $assets = Read-JsonFile -Path $resolvedAssetsPath
  if ($null -eq $assets -or $assets -is [System.Array] -or $assets -is [string] -or $assets -is [ValueType] -or [string]$assets.schema_version -ne '1.0' -or $assets.assets -isnot [System.Array]) { throw "NATIVE_VISUAL_COVERAGE_ASSETS_INVALID:$Label" }
  if (-not (Test-PathsEqual -FirstPath ([string]$coverage.native_deck_path) -SecondPath $ExpectedDeckPath)) { throw "NATIVE_VISUAL_COVERAGE_DECK_PATH_MISMATCH:$Label" }
  if ([string]$coverage.native_deck_sha256 -notmatch '^[0-9a-fA-F]{64}$' -or [string]$coverage.native_deck_sha256 -ine $ExpectedDeckHash) { throw "NATIVE_VISUAL_COVERAGE_DECK_HASH_MISMATCH:$Label" }
  $layoutPath = if ($coverage.PSObject.Properties['native_layout_report_path']) { [string]$coverage.native_layout_report_path } else { '' }
  $layoutHash = if ($coverage.PSObject.Properties['native_layout_report_sha256']) { [string]$coverage.native_layout_report_sha256 } else { '' }
  if ([string]::IsNullOrWhiteSpace($layoutPath) -or $layoutHash -notmatch '^[0-9a-fA-F]{64}$') { throw "NATIVE_LAYOUT_REPORT_BINDING_MISSING:$Label" }
  $resolvedLayoutPath = Assert-RegularFilePath -Path $layoutPath -Label "NATIVE_LAYOUT_REPORT_$Label"
  $actualLayoutHash = (Get-FileHash -LiteralPath $resolvedLayoutPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actualLayoutHash -ine $layoutHash) { throw "NATIVE_LAYOUT_REPORT_HASH_MISMATCH:$Label" }
  $layout = Read-JsonFile -Path $resolvedLayoutPath
  if ($null -eq $layout -or $layout -is [System.Array] -or $layout -is [string] -or $layout -is [ValueType]) { throw "NATIVE_LAYOUT_REPORT_INVALID:$Label" }
  if (-not $layout.PSObject.Properties['schema_version'] -or [string]$layout.schema_version -ne '1.0') { throw "NATIVE_LAYOUT_REPORT_SCHEMA_VERSION_INVALID:$Label" }
  if ([string]$layout.deck_sha256 -notmatch '^[0-9a-fA-F]{64}$' -or [string]$layout.deck_sha256 -ine $ExpectedDeckHash) { throw "NATIVE_LAYOUT_REPORT_DECK_HASH_MISMATCH:$Label" }
  if ([string]$layout.status -ne 'PASS' -or [string]$layout.deck_sha256_before -notmatch '^[0-9a-fA-F]{64}$' -or [string]$layout.deck_sha256_after -notmatch '^[0-9a-fA-F]{64}$' -or [string]$layout.deck_sha256_before -ine $ExpectedDeckHash -or [string]$layout.deck_sha256_after -ine $ExpectedDeckHash) { throw "NATIVE_LAYOUT_REPORT_NOT_PASS:$Label" }
  if (-not (Test-PathsEqual -FirstPath ([string]$layout.deck_path) -SecondPath $ExpectedDeckPath)) { throw "NATIVE_LAYOUT_REPORT_DECK_PATH_MISMATCH:$Label" }
  if ($layout.slides -isnot [System.Array] -or @($layout.slides).Count -lt 1) { throw "NATIVE_LAYOUT_REPORT_SLIDES_MISSING:$Label" }
  Assert-NativeReportFindings -Findings $layout.findings -InvalidErrorCode "NATIVE_LAYOUT_REPORT_FINDINGS_INVALID:$Label" -CriticalErrorCode "NATIVE_LAYOUT_REPORT_CRITICAL_FINDINGS:$Label"
  $layoutSlideCount = ConvertTo-NativeReportInteger -Value $layout.slide_count -Minimum 1 -Maximum 100000 -ErrorCode "NATIVE_LAYOUT_REPORT_SLIDE_COUNT_INVALID:$Label"
  if ($layoutSlideCount -ne @($layout.slides).Count) { throw "NATIVE_LAYOUT_REPORT_SLIDE_COUNT_INVALID:$Label" }
  $layoutSlideNumbers = [System.Collections.Generic.HashSet[int]]::new()
  foreach ($layoutSlide in @($layout.slides)) {
    if ($null -eq $layoutSlide -or $layoutSlide -is [System.Array] -or $layoutSlide -is [string] -or $layoutSlide -is [ValueType] -or $layoutSlide.objects -isnot [System.Array]) { throw "NATIVE_LAYOUT_REPORT_SLIDE_RECORD_INVALID:$Label" }
    $layoutSlideNumber = ConvertTo-NativeReportInteger -Value $layoutSlide.slide -Minimum 1 -Maximum $layoutSlideCount -ErrorCode "NATIVE_LAYOUT_REPORT_SLIDE_SEQUENCE_INVALID:$Label"
    if (-not $layoutSlideNumbers.Add($layoutSlideNumber)) { throw "NATIVE_LAYOUT_REPORT_SLIDE_SEQUENCE_INVALID:$Label" }
    $shapeCount = ConvertTo-NativeReportInteger -Value $layoutSlide.shape_count -Minimum 0 -Maximum 1000000 -ErrorCode "NATIVE_LAYOUT_REPORT_SHAPE_COUNT_INVALID:$Label"
    if ($shapeCount -ne @($layoutSlide.objects).Count) { throw "NATIVE_LAYOUT_REPORT_SHAPE_COUNT_MISMATCH:$Label" }
    $objectNames = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($layoutObject in @($layoutSlide.objects)) {
      if ($null -eq $layoutObject -or $layoutObject -is [System.Array] -or $layoutObject -is [string] -or $layoutObject -is [ValueType] -or [string]::IsNullOrWhiteSpace([string]$layoutObject.name) -or -not $objectNames.Add([string]$layoutObject.name)) { throw "NATIVE_LAYOUT_REPORT_OBJECT_RECORD_INVALID:$Label" }
    }
  }
  for ($slideNumber = 1; $slideNumber -le $layoutSlideCount; $slideNumber += 1) {
    if (-not $layoutSlideNumbers.Contains($slideNumber)) { throw "NATIVE_LAYOUT_REPORT_SLIDE_SEQUENCE_INVALID:$Label" }
  }
  if ($layoutSlideCount -ne $coverageSlideCount) { throw "NATIVE_VISUAL_COVERAGE_SLIDE_COUNT_MISMATCH:$Label" }
  return [ordered]@{
    native_bindings_verified = $true
    native_visual_coverage_report_path = $reportPath
    native_visual_coverage_report_sha256 = $actualReportHash
    native_visual_coverage_deck_sha256 = $ExpectedDeckHash.ToLowerInvariant()
  }
}

function Test-JsonElementStrict {
  param(
    [Parameter(Mandatory = $true)][System.Text.Json.JsonElement]$Element,
    [Parameter(Mandatory = $true)][string]$JsonPath
  )
  if ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Object) {
    $seen = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($property in $Element.EnumerateObject()) {
      if (-not $seen.Add($property.Name)) { throw "DUPLICATE_JSON_PROPERTY:$JsonPath.$($property.Name)" }
      Test-JsonElementStrict -Element $property.Value -JsonPath "$JsonPath.$($property.Name)"
    }
  } elseif ($Element.ValueKind -eq [System.Text.Json.JsonValueKind]::Array) {
    $index = 0
    foreach ($item in $Element.EnumerateArray()) {
      Test-JsonElementStrict -Element $item -JsonPath "$JsonPath[$index]"
      $index += 1
    }
  }
}

function Release-ComObject {
  param([object]$Object)
  if ($null -ne $Object -and [Runtime.InteropServices.Marshal]::IsComObject($Object)) {
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($Object)
  }
}

function Set-PowerPointSafeAutomation {
  param([Parameter(Mandatory = $true)][object]$Application)
  try {
    $Application.AutomationSecurity = 3
  } catch {
    throw "POWERPOINT_AUTOMATION_SECURITY_UNAVAILABLE:$($_.Exception.Message)"
  }
  try { $Application.DisplayAlerts = 1 } catch {}
}

function Get-DefaultCacheRoot {
  if ($env:MAKE_SLIDE_PRO_CACHE) {
    return [System.IO.Path]::GetFullPath($env:MAKE_SLIDE_PRO_CACHE)
  }
  $codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
  return Join-Path $codexHome 'cache\make-slide-pro'
}

function Get-FilePrefixBytes {
  param(
    [Parameter(Mandatory = $true)][string]$Path,
    [int]$Count = 512
  )
  $stream = [System.IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
  try {
    if ($Count -lt 0) { throw 'Byte count must be non-negative.' }
    $lengthToRead = [int][Math]::Min([long]$Count, [Math]::Max([long]0, [long]$stream.Length))
    $buffer = [byte[]]::new($lengthToRead)
    if ($buffer.Length -gt 0) {
      [void]$stream.Read($buffer, 0, $buffer.Length)
    }
    return ,$buffer
  } finally {
    $stream.Dispose()
  }
}

function Test-BytesPrefix {
  param([byte[]]$Bytes, [byte[]]$Prefix)
  if ($null -eq $Bytes -or $null -eq $Prefix) { return $false }
  if ($Bytes.Length -lt $Prefix.Length) { return $false }
  for ($index = 0; $index -lt $Prefix.Length; $index += 1) {
    if ($Bytes[$index] -ne $Prefix[$index]) { return $false }
  }
  return $true
}

function Get-ZipOfficeFormat {
  param([Parameter(Mandatory = $true)][string]$Path)
  Add-Type -AssemblyName System.IO.Compression -ErrorAction SilentlyContinue
  $stream = $null
  $archive = $null
  try {
    $stream = [System.IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
    $archive = [System.IO.Compression.ZipArchive]::new($stream, [System.IO.Compression.ZipArchiveMode]::Read, $false)
    $names = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($entry in $archive.Entries) { [void]$names.Add($entry.FullName) }
    if ($names.Contains('ppt/presentation.xml')) {
      $presentationFormat = if ($names.Contains('ppt/vbaProject.bin')) { 'PPTM' } else { 'PPTX' }
      return $presentationFormat
    }
    if ($names.Contains('word/document.xml')) {
      $documentFormat = if ($names.Contains('word/vbaProject.bin')) { 'DOCM' } else { 'DOCX' }
      return $documentFormat
    }
    if ($names.Contains('xl/workbook.xml')) {
      $spreadsheetFormat = if ($names.Contains('xl/vbaProject.bin')) { 'XLSM' } else { 'XLSX' }
      return $spreadsheetFormat
    }
    if ($names.Contains('mimetype')) {
      $entry = $archive.GetEntry('mimetype')
      if ($entry) {
        $reader = [System.IO.StreamReader]::new($entry.Open())
        try {
          $mime = $reader.ReadToEnd()
          if ($mime -match 'presentation') { return 'ODP' }
          if ($mime -match 'spreadsheet') { return 'ODS' }
        } finally {
          $reader.Dispose()
        }
      }
    }
    return 'ZIP'
  } catch {
    return 'ZIP_CORRUPT'
  } finally {
    if ($archive) { $archive.Dispose() }
    if ($stream) { $stream.Dispose() }
  }
}

function Get-DetectedFileFormat {
  param([Parameter(Mandatory = $true)][string]$Path)
  $extension = [System.IO.Path]::GetExtension($Path).ToLowerInvariant()
  $bytes = Get-FilePrefixBytes -Path $Path -Count 4096
  if ((Test-BytesPrefix $bytes ([byte[]](0x50, 0x4B, 0x03, 0x04))) -or
      (Test-BytesPrefix $bytes ([byte[]](0x50, 0x4B, 0x05, 0x06))) -or
      (Test-BytesPrefix $bytes ([byte[]](0x50, 0x4B, 0x07, 0x08)))) { return Get-ZipOfficeFormat -Path $Path }
  if (Test-BytesPrefix $bytes ([byte[]](0x25, 0x50, 0x44, 0x46, 0x2D))) { return 'PDF' }
  if (Test-BytesPrefix $bytes ([byte[]](0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1))) {
    $oleFormat = switch ($extension) {
      '.ppt' { 'PPT' }
      '.doc' { 'DOC' }
      '.xls' { 'XLS' }
      default { 'OLE_OFFICE' }
    }
    return $oleFormat
  }
  if (Test-BytesPrefix $bytes ([byte[]](0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))) { return 'PNG' }
  if (Test-BytesPrefix $bytes ([byte[]](0xFF, 0xD8, 0xFF))) { return 'JPEG' }
  if (Test-BytesPrefix $bytes ([byte[]](0x47, 0x49, 0x46, 0x38))) { return 'GIF' }
  if ((Test-BytesPrefix $bytes ([byte[]](0x49, 0x49, 0x2A, 0x00))) -or (Test-BytesPrefix $bytes ([byte[]](0x4D, 0x4D, 0x00, 0x2A)))) { return 'TIFF' }
  if (Test-BytesPrefix $bytes ([byte[]](0x42, 0x4D))) { return 'BMP' }
  if (Test-BytesPrefix $bytes ([byte[]](0x66, 0x4C, 0x61, 0x43))) { return 'FLAC' }
  if (Test-BytesPrefix $bytes ([byte[]](0x4F, 0x67, 0x67, 0x53))) { return 'OGG' }
  if ($bytes.Length -ge 12 -and [System.Text.Encoding]::ASCII.GetString($bytes, 0, 4) -eq 'RIFF') {
    $riffType = [System.Text.Encoding]::ASCII.GetString($bytes, 8, 4)
    if ($riffType -eq 'WAVE') { return 'WAV' }
    if ($riffType -eq 'WEBP') { return 'WEBP' }
    if ($riffType -eq 'AVI ') { return 'AVI' }
  }
  if (Test-BytesPrefix $bytes ([byte[]](0x49, 0x44, 0x33))) { return 'MP3' }
  if ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFF -and (($bytes[1] -band 0xF6) -eq 0xF0)) { return 'AAC' }
  if ($bytes.Length -ge 2 -and $bytes[0] -eq 0xFF -and (($bytes[1] -band 0xE0) -eq 0xE0) -and (($bytes[1] -band 0x06) -ne 0)) { return 'MP3' }
  if ($bytes.Length -ge 12 -and [System.Text.Encoding]::ASCII.GetString($bytes, 4, 4) -eq 'ftyp') {
    $mp4Format = if ($extension -in @('.m4a', '.aac')) { 'M4A' } else { 'MP4' }
    return $mp4Format
  }
  if (Test-BytesPrefix $bytes ([byte[]](0x1A, 0x45, 0xDF, 0xA3))) {
    $matroskaFormat = if ($extension -eq '.webm') { 'WEBM' } else { 'MKV' }
    return $matroskaFormat
  }
  if (Test-BytesPrefix $bytes ([byte[]](0x37, 0x7A, 0xBC, 0xAF, 0x27, 0x1C))) { return '7Z' }
  if (Test-BytesPrefix $bytes ([byte[]](0x52, 0x61, 0x72, 0x21))) { return 'RAR' }
  $sample = if ($bytes.Length -gt 0) { [System.Text.Encoding]::UTF8.GetString($bytes) } else { '' }
  $trimmed = $sample.TrimStart([char]0xFEFF, [char]0x0000, [char]0x0009, [char]0x000A, [char]0x000D, [char]0x0020)
  if ($trimmed -match '^<svg\b') { return 'SVG' }
  if ($extension -eq '.json' -and $trimmed -match '^[\{\[]') { return 'JSON' }
  if ($extension -eq '.xml' -and $trimmed -match '^<') { return 'XML' }
  if ($extension -eq '.html' -or $extension -eq '.htm') { return 'HTML' }
  if ($extension -eq '.md') { return 'MARKDOWN' }
  if ($extension -eq '.csv') { return 'CSV' }
  if ($extension -eq '.tsv') { return 'TSV' }
  if (-not ($bytes -contains 0)) { return 'TEXT' }
  return 'UNKNOWN'
}

function Get-ExpectedFormatsForExtension {
  param([string]$Extension)
  $extension = $Extension.ToLowerInvariant()
  $map = @{
    '.pptx' = @('PPTX'); '.pptm' = @('PPTM'); '.ppt' = @('PPT'); '.ppsx' = @('PPTX'); '.potx' = @('PPTX'); '.odp' = @('ODP')
    '.docx' = @('DOCX'); '.docm' = @('DOCM'); '.doc' = @('DOC'); '.rtf' = @('TEXT')
    '.xlsx' = @('XLSX'); '.xlsm' = @('XLSM'); '.xls' = @('XLS'); '.ods' = @('ODS')
    '.pdf' = @('PDF'); '.txt' = @('TEXT'); '.md' = @('MARKDOWN', 'TEXT'); '.html' = @('HTML', 'TEXT'); '.htm' = @('HTML', 'TEXT')
    '.csv' = @('CSV', 'TEXT'); '.tsv' = @('TSV', 'TEXT'); '.json' = @('JSON', 'TEXT'); '.xml' = @('XML', 'TEXT')
    '.png' = @('PNG'); '.jpg' = @('JPEG'); '.jpeg' = @('JPEG'); '.gif' = @('GIF'); '.tif' = @('TIFF'); '.tiff' = @('TIFF'); '.bmp' = @('BMP'); '.webp' = @('WEBP'); '.svg' = @('SVG', 'TEXT')
    '.mp3' = @('MP3'); '.wav' = @('WAV'); '.m4a' = @('M4A', 'MP4'); '.aac' = @('AAC'); '.flac' = @('FLAC'); '.ogg' = @('OGG')
    '.mp4' = @('MP4'); '.mov' = @('MP4'); '.mkv' = @('MKV'); '.avi' = @('AVI'); '.webm' = @('WEBM')
    '.zip' = @('ZIP', 'PPTX', 'PPTM', 'DOCX', 'DOCM', 'XLSX', 'XLSM', 'ODP', 'ODS'); '.7z' = @('7Z'); '.rar' = @('RAR')
  }
  $expectedFormats = if ($map.ContainsKey($extension)) { $map[$extension] } else { @() }
  return $expectedFormats
}

function Get-DefaultSourceRole {
  param([string]$DetectedFormat, [string]$Extension)
  if ($DetectedFormat -in @('PPTX', 'PPTM', 'PPT', 'ODP')) {
    $presentationRole = if ($Extension -eq '.potx') { 'TEMPLATE' } else { 'PREVIOUS_DECK' }
    return $presentationRole
  }
  if ($DetectedFormat -in @('XLSX', 'XLSM', 'XLS', 'ODS', 'CSV', 'TSV', 'JSON', 'XML')) { return 'DATA_AUTHORITY' }
  if ($DetectedFormat -in @('PNG', 'JPEG', 'GIF', 'TIFF', 'BMP', 'WEBP', 'SVG', 'MP3', 'WAV', 'M4A', 'AAC', 'FLAC', 'OGG', 'MP4', 'MKV', 'AVI', 'WEBM')) { return 'MEDIA_ASSET' }
  if ($DetectedFormat -in @('ZIP', '7Z', 'RAR', 'ZIP_CORRUPT')) { return 'PRIMARY_CONTENT' }
  return 'PRIMARY_CONTENT'
}
