# MIROIR TEXTUEL - start_mdl_servers.ps1

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\start_mdl_servers.ps1
Taille : 2987 octets
SHA256 : 3d0e82d31179cdd7b30de180cbef4ee84654568fbc206f6381cec933aa0ef855

```text
# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Script de demarrage automatique des serveurs MDL Ynor
# =============================================================================

$workDir = "C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework"
$logDir = "$workDir\logs"

# Creer le dossier de logs s'il n'existe pas
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   MDL YNOR - DEMARRAGE DES SERVEURS" -ForegroundColor Cyan
Write-Host "   $(Get-Date)" -ForegroundColor Gray
Write-Host "=============================================" -ForegroundColor Cyan

# --- 1. Lancer le serveur FastAPI (Uvicorn) ---
Write-Host "`n[1/2] Demarrage du serveur API (Uvicorn port 8492)..." -ForegroundColor Yellow

$apiProcess = Start-Process -FilePath "python" `
    -ArgumentList "-m uvicorn ynor_api_server:app --host 0.0.0.0 --port 8492" `
    -WorkingDirectory $workDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput "$logDir\uvicorn_$timestamp.log" `
    -RedirectStandardError "$logDir\uvicorn_errors_$timestamp.log" `
    -PassThru

Write-Host "   API lancee (PID: $($apiProcess.Id))" -ForegroundColor Green

# Attendre que le serveur demarre
Start-Sleep -Seconds 3

# --- 2. Lancer le tunnel ngrok ---
Write-Host "[2/2] Demarrage du tunnel ngrok..." -ForegroundColor Yellow

$ngrokProcess = Start-Process -FilePath "ngrok" `
    -ArgumentList "http 8492 --url=https://mdlynor.ngrok-free.app --log=stdout" `
    -WorkingDirectory $workDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput "$logDir\ngrok_$timestamp.log" `
    -RedirectStandardError "$logDir\ngrok_errors_$timestamp.log" `
    -PassThru

Write-Host "   ngrok lance (PID: $($ngrokProcess.Id))" -ForegroundColor Green

# --- Confirmation ---
Write-Host "`n=============================================" -ForegroundColor Green
Write-Host "   TOUS LES SERVEURS SONT EN LIGNE" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "   API locale    : http://localhost:8492" -ForegroundColor White
Write-Host "   API publique  : https://mdlynor.ngrok-free.app" -ForegroundColor White
Write-Host "   Logs          : $logDir" -ForegroundColor Gray
Write-Host ""
Write-Host "   PID Uvicorn   : $($apiProcess.Id)" -ForegroundColor Gray
Write-Host "   PID ngrok     : $($ngrokProcess.Id)" -ForegroundColor Gray
Write-Host ""

# Sauvegarder les PIDs pour pouvoir les arreter plus tard
@{
    uvicorn_pid = $apiProcess.Id
    ngrok_pid   = $ngrokProcess.Id
    started_at  = (Get-Date).ToString()
} | ConvertTo-Json | Out-File "$workDir\server_pids.json" -Encoding UTF8

Write-Host "PIDs sauvegardes dans server_pids.json" -ForegroundColor Gray

```