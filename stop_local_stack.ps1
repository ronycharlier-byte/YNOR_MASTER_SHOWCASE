$ErrorActionPreference = "SilentlyContinue"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $root "server_pids.json"

if (Test-Path $pidFile) {
    $data = Get-Content $pidFile -Raw | ConvertFrom-Json
    if ($data.api_pid) { Stop-Process -Id $data.api_pid -Force }
    if ($data.streamlit_pid) { Stop-Process -Id $data.streamlit_pid -Force }
    Remove-Item $pidFile -Force
    Write-Host "Local stack stopped." -ForegroundColor Green
    exit 0
}

Write-Host "No pid file found. Nothing was stopped." -ForegroundColor Yellow
