param(
  [Parameter(Mandatory=$true)][string]$InputPptx,
  [Parameter(Mandatory=$true)][string]$OutputDir
)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$ppt = New-Object -ComObject PowerPoint.Application
$presentation = $null
try {
  Write-Output "Opening $InputPptx"
  $presentation = $ppt.Presentations.Open($InputPptx, $true, $false, $false)
  Write-Output "Exporting $OutputDir"
  $presentation.Export($OutputDir, "PNG", 1920, 1080)
  Write-Output "Rendered $InputPptx to $OutputDir"
}
finally {
  if ($null -ne $presentation) { $presentation.Close() }
  if ($null -ne $ppt) { $ppt.Quit() }
}
