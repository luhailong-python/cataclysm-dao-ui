param(
    [int]$Width = 1600,
    [int]$Height = 900
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
Push-Location -LiteralPath $projectRoot
try {
    python -m app --width $Width --height $Height
    if ($LASTEXITCODE -ne 0) { throw "Launcher exited with code $LASTEXITCODE" }
} finally {
    Pop-Location
}
