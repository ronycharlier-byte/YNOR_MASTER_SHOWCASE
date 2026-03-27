# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Script d'arret des serveurs MDL Ynor
# =============================================================================

$workDir = "C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework"
$pidFile = "$workDir\server_pids.json"

if (Test-Path $pidFile) {
    $pids = Get-Content $pidFile | ConvertFrom-Json
    
    Write-Host "Arret du serveur Uvicorn (PID: $($pids.uvicorn_pid))..." -ForegroundColor Yellow
    Stop-Process -Id $pids.uvicorn_pid -Force -ErrorAction SilentlyContinue
    
    Write-Host "Arret de ngrok (PID: $($pids.ngrok_pid))..." -ForegroundColor Yellow
    Stop-Process -Id $pids.ngrok_pid -Force -ErrorAction SilentlyContinue
    
    Remove-Item $pidFile -Force
    Write-Host "Tous les serveurs ont ete arretes." -ForegroundColor Green
} else {
    Write-Host "Aucun serveur actif trouve (pas de server_pids.json)." -ForegroundColor Red
    
    # Fallback : tuer par nom de processus
    Write-Host "Tentative d'arret par nom de processus..." -ForegroundColor Yellow
    Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process -Name "ngrok" -ErrorAction SilentlyContinue | Stop-Process -Force
    Write-Host "Processus arretes." -ForegroundColor Green
}
