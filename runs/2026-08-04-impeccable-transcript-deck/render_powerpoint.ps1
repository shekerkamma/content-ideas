param(
  [Parameter(Mandatory=$true)][string]$InputPptx,
  [Parameter(Mandatory=$true)][string]$OutputDir
)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
$ppt = $null
try { $ppt = [Runtime.InteropServices.Marshal]::GetActiveObject("PowerPoint.Application") } catch {}
if ($null -eq $ppt) { $ppt = New-Object -ComObject PowerPoint.Application }
$presentation = $null
$inputName = [IO.Path]::GetFileName($InputPptx)
for ($i = 1; $i -le $ppt.Presentations.Count; $i++) {
  if ($ppt.Presentations.Item($i).Name -eq $inputName) { $presentation = $ppt.Presentations.Item($i); break }
}
if ($null -eq $presentation) { $presentation = $ppt.Presentations.Open($InputPptx, $true, $false, $false) }
$presentation.Export($OutputDir, "PNG", 1920, 1080)
$presentation.Close()
Write-Output "Rendered $InputPptx to $OutputDir"
