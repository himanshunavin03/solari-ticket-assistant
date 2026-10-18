$ErrorActionPreference = 'Stop'
# Installs a project-local runtime only. Does not change system PATH or Node.
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtimeDirectory = Join-Path $projectRoot '.runtime'
$nodeVersion = '22.23.2'
$archiveName = "node-v$nodeVersion-win-x64.zip"
$nodeDirectory = Join-Path $runtimeDirectory "node-v$nodeVersion-win-x64"
New-Item -ItemType Directory -Force $runtimeDirectory | Out-Null
if (!(Test-Path (Join-Path $nodeDirectory 'node.exe'))) {
    $archivePath = Join-Path $runtimeDirectory $archiveName
    Invoke-WebRequest "https://nodejs.org/dist/v$nodeVersion/$archiveName" -OutFile $archivePath
    $sums = (Invoke-WebRequest "https://nodejs.org/dist/v$nodeVersion/SHASUMS256.txt").Content
    $line = ($sums -split "`n" | Where-Object { $_.Trim().EndsWith("  $archiveName") })
    if (!$line -or ((Get-FileHash $archivePath -Algorithm SHA256).Hash.ToLower() -ne ($line -split '\s+')[0])) {
        throw 'Node archive checksum mismatch; do not use the download.'
    }
    Expand-Archive -LiteralPath $archivePath -DestinationPath $runtimeDirectory -Force
}
& (Join-Path $nodeDirectory 'node.exe') --version
Write-Output "In each shell, run: `$env:Path = '$nodeDirectory;' + `$env:Path"
