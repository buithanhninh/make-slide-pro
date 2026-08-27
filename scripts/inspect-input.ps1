param(
  [Parameter(Mandatory = $true)][string]$InputPath,
  [Parameter(Mandatory = $true)][string]$OutputPath
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'common.ps1')
$resolvedOutput = Get-NormalizedFullPath -Path $OutputPath
$resolved = $null
$outputIsSafe = $false
try {
  $inputCandidate = Get-NormalizedFullPath -Path $InputPath
  Assert-NoReparseAncestors -Path ([System.IO.Path]::GetDirectoryName($resolvedOutput))
  [void](Assert-NewOutputPath -OutputPath $resolvedOutput -ProtectedPaths @($inputCandidate) -Label 'INSPECT_OUTPUT')
  $outputIsSafe = $true
  $resolved = (Resolve-Path -LiteralPath $InputPath -ErrorAction Stop).Path
  Assert-NoReparseAncestors -Path $resolved
  $format = if (Test-Path -LiteralPath $resolved -PathType Leaf) { Get-DetectedFileFormat -Path $resolved } else { 'DIRECTORY' }
  $item = Get-Item -LiteralPath $resolved -Force -ErrorAction Stop
  if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { throw "INSPECT_INPUT_REPARSE_POINT_NOT_ALLOWED:$resolved" }
  $payload = [ordered]@{
    schema_version = '1.0'
    generated_at = (Get-Date).ToUniversalTime().ToString('o')
    path = $resolved
    kind = if ($item.PSIsContainer) { 'DIRECTORY' } else { 'FILE' }
    detected_format = $format
    extension = if ($item.PSIsContainer) { $null } else { $item.Extension.ToLowerInvariant() }
    size_bytes = if ($item.PSIsContainer) { $null } else { [long]$item.Length }
    sha256 = if ($item.PSIsContainer) { $null } else { (Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash.ToLowerInvariant() }
    adapter = switch ($format) {
      { $_ -in @('PPTX', 'PPTM', 'PPT', 'ODP') } { 'POWERPOINT'; break }
      { $_ -in @('DOCX', 'DOCM', 'DOC', 'TEXT', 'MARKDOWN', 'HTML') } { 'DOCUMENT'; break }
      { $_ -eq 'PDF' } { 'PDF'; break }
      { $_ -in @('XLSX', 'XLSM', 'XLS', 'ODS', 'CSV', 'TSV', 'JSON', 'XML') } { 'DATA'; break }
      { $_ -in @('MP3', 'WAV', 'M4A', 'AAC', 'FLAC', 'OGG') } { 'AUDIO'; break }
      { $_ -in @('MP4', 'MKV', 'AVI', 'WEBM') } { 'VIDEO'; break }
      { $_ -in @('PNG', 'JPEG', 'GIF', 'TIFF', 'BMP', 'WEBP', 'SVG') } { 'IMAGE'; break }
      { $_ -in @('ZIP', '7Z', 'RAR', 'ZIP_CORRUPT') } { 'ARCHIVE'; break }
      default { 'UNKNOWN' }
    }
    maturity_hint = switch ($format) {
      { $_ -in @('PPTX', 'PPTM', 'PPT', 'ODP') } { 'S4_EDITABLE_OR_FLATTENED_DECK'; break }
      { $_ -eq 'PDF' } { 'S3_FLAT_OR_REPORT'; break }
      { $_ -in @('DOCX', 'DOC', 'TEXT', 'MARKDOWN', 'HTML') } { 'S1_STRUCTURED_CONTENT'; break }
      { $_ -in @('XLSX', 'XLSM', 'XLS', 'ODS', 'CSV', 'TSV', 'JSON', 'XML') } { 'S1_DATA_SOURCE'; break }
      { $_ -in @('MP3', 'WAV', 'M4A', 'FLAC', 'OGG', 'MP4', 'MKV', 'AVI', 'WEBM') } { 'S0_MEDIA'; break }
      { $_ -in @('AAC') } { 'S0_MEDIA'; break }
      { $_ -in @('ZIP', '7Z', 'RAR', 'ZIP_CORRUPT') } { 'S0_ARCHIVE'; break }
      default { 'S0_UNKNOWN' }
    }
  }
  Write-JsonFileNew -Value $payload -Path $resolvedOutput
  $payload | ConvertTo-Json -Depth 10
} catch {
  $message = ($_.Exception.Message -replace '[\r\n]+', ' ').Trim()
  $status = if ($message -match '(?i)(PATH_COLLISION|ALREADY_EXISTS|REPARSE_POINT)') { 'BLOCKED' } else { 'UNVERIFIED' }
  if ($outputIsSafe -and -not (Test-Path -LiteralPath $resolvedOutput)) {
    $failure = [ordered]@{ schema_version = '1.0'; generated_at = (Get-Date).ToUniversalTime().ToString('o'); path = if ($resolved) { $resolved } else { $InputPath }; status = $status; error = $message }
    Write-JsonFileNew -Value $failure -Path $resolvedOutput
  }
  [Console]::Error.WriteLine($message)
  exit $(if ($status -eq 'BLOCKED') { 2 } else { 3 })
}
