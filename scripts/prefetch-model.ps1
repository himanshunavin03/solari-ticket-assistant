# Optional dependency-free prefetch while Python dependencies install.
# The Python download command still verifies model loading and real encoding.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$modelId = 'sentence-transformers/all-MiniLM-L6-v2'
$revision = '1110a243fdf4706b3f48f1d95db1a4f5529b4d41'
$metadata = Invoke-RestMethod "https://huggingface.co/api/models/$modelId/revision/${revision}?blobs=true"
if ($metadata.sha -ne $revision) { throw 'Unexpected model revision' }
$snapshot = Join-Path $projectRoot ".cache/models/models--sentence-transformers--all-MiniLM-L6-v2/snapshots/$revision"
$files = @('modules.json','config.json','config_sentence_transformers.json','sentence_bert_config.json',
    'tokenizer.json','tokenizer_config.json','vocab.txt','special_tokens_map.json','1_Pooling/config.json','model.safetensors')
foreach ($file in $files) {
    $entry = $metadata.siblings | Where-Object { $_.rfilename -eq $file }
    if (!$entry) { continue }
    $destination = Join-Path $snapshot $file
    New-Item -ItemType Directory -Force (Split-Path $destination -Parent) | Out-Null
    if (!(Test-Path -LiteralPath $destination)) {
        & curl.exe --fail --location --silent --show-error --retry 3 --retry-all-errors --max-time 1200 --output "$destination.partial" "https://huggingface.co/$modelId/resolve/$revision/$file"
        if ($LASTEXITCODE -ne 0) { throw "Download failed: $file" }
        if ($entry.lfs.sha256 -and ((Get-FileHash "$destination.partial").Hash.ToLower() -ne $entry.lfs.sha256)) { throw "Checksum mismatch: $file" }
        Move-Item -LiteralPath "$destination.partial" -Destination $destination
    }
}
Write-Output 'Pinned model files prefetched. Run python -m scripts.download_model to verify actual loading.'
