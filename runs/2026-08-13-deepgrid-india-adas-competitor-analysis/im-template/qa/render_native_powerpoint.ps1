$ErrorActionPreference = "Stop"
$renderDir = "C:\Temp\deepgrid-80-native-manual\slides"
$targetName = "DeepGrid-Semi-Competitor-Dossiers-80-Slide-Detailed-Anatomy-v7-draft.pptx"

if (Test-Path $renderDir) {
    Remove-Item $renderDir -Recurse -Force
}
New-Item -ItemType Directory -Path $renderDir | Out-Null

$powerPoint = [Runtime.InteropServices.Marshal]::GetActiveObject("PowerPoint.Application")
$presentation = $null
for ($index = 1; $index -le $powerPoint.Presentations.Count; $index++) {
    $candidate = $powerPoint.Presentations.Item($index)
    if ($candidate.Name -eq $targetName) {
        $presentation = $candidate
        break
    }
}
if ($null -eq $presentation) {
    throw "Open target presentation not found: $targetName"
}
$presentation.Export($renderDir, "PNG", 1920, 1080)
Write-Output ("NATIVE_SLIDES=" + $presentation.Slides.Count)
