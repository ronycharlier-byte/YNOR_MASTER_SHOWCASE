# MIROIR TEXTUEL - start_mdl_servers_cf.ps1

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\start_mdl_servers_cf.ps1
Taille : 2864 octets
SHA256 : 3877dfc718472425cf40e7064e42275b5df0916a63a560760c9aacddf8d15300

```text
# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Script de demarrage automatique des serveurs MDL Ynor (Version Cloudflare)
# =============================================================================

$workDir = "C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework"
$logDir = "$workDir\logs"

# Creer le dossier de logs s'il n'existe pas
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   MDL YNOR - DEMARRAGE (CLOUDFLARE TUNNEL)" -ForegroundColor Cyan
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

# --- 2. Lancer le tunnel Cloudflare ---
Write-Host "[2/2] Demarrage du tunnel Cloudflare (api.mdlstrategy.com)..." -ForegroundColor Yellow

$cfProcess = Start-Process -FilePath "cloudflared" `
    -ArgumentList "tunnel --config $workDir\config.yml run mdl-ynor-tunnel" `
    -WorkingDirectory $workDir `
    -WindowStyle Hidden `
    -RedirectStandardOutput "$logDir\cloudflare_$timestamp.log" `
    -RedirectStandardError "$logDir\cloudflare_errors_$timestamp.log" `
    -PassThru

Write-Host "   Cloudflare Tunnel lance (PID: $($cfProcess.Id))" -ForegroundColor Green

# --- Confirmation ---
Write-Host "`n=============================================" -ForegroundColor Green
Write-Host "   TOUS LES SERVEURS SONT EN LIGNE" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "   API locale    : http://localhost:8492" -ForegroundColor White
Write-Host "   API publique  : https://api.mdlstrategy.com" -ForegroundColor White
Write-Host "   Logs          : $logDir" -ForegroundColor Gray
Write-Host ""

# Sauvegarder les PIDs
@{
    uvicorn_pid = $apiProcess.Id
    cf_pid      = $cfProcess.Id
    started_at  = (Get-Date).ToString()
} | ConvertTo-Json | Out-File "$workDir\server_pids.json" -Encoding UTF8

Write-Host "PIDs sauvegardes dans server_pids.json" -ForegroundColor Gray

```