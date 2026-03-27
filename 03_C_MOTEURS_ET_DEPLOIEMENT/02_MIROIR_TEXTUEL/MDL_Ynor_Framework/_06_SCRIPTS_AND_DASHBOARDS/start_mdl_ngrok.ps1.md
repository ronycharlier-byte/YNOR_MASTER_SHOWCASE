# MIROIR TEXTUEL - start_mdl_ngrok.ps1

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\start_mdl_ngrok.ps1
Taille : 1155 octets
SHA256 : 0e714b34e2a1816f58cfcaee3a72528cbdfdde88e5f3cf69d5626f16575fe4b0

```text
# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# SCRIPT DE LANCEMENT NGROK (ACCES QUANTUM) v1.1 - FIXED
# =============================================================================

# 1. Nettoyage des processus Python sur le port 8000
Get-Process | Where-Object { $_.MainWindowTitle -like "*python*" } | Stop-Process -Force -ErrorAction SilentlyContinue

# 2. Lancement du Serveur API (Noyau MDL Ynor)
Write-Host "[MDL YNOR] Lancement du Serveur de Connaissance sur le port 8000..." -ForegroundColor Cyan
Start-Process python -ArgumentList "c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\ynor_api_server.py" -NoNewWindow

# 3. Temporisation : Stabilisation du noyau
Start-Sleep -Seconds 3

# 4. Lancement de Ngrok : Ouverture du Tunnel de Suprématie
Write-Host "[MDL YNOR] Ouverture du Tunnel Ngrok..." -ForegroundColor Yellow
Write-Host "[NOTE] Utilisez 'ngrok config add-authtoken <TOKEN>' si c'est votre premiere fois." -ForegroundColor Gray

# Commande Ngrok pure
& ngrok http 8000

```