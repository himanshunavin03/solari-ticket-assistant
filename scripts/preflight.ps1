param([string]$Python = '.\.venv\Scripts\python.exe')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location $projectRoot
try {
    Write-Output "Active shell Python: $((Get-Command python).Source)"
    & python --version
    if ($LASTEXITCODE -ne 0) { throw 'Active Python unavailable' }
    # Does not install packages, download weights, change PATH, or use system services.
    & $Python -m scripts.preflight
    if ($LASTEXITCODE -ne 0) { throw 'Preflight failed; see specific check above.' }
} finally { Pop-Location }
