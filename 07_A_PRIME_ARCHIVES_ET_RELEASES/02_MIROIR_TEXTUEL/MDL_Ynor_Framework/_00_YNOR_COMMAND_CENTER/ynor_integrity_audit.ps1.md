# MIROIR TEXTUEL - ynor_integrity_audit.ps1

Source : MDL_Ynor_Framework\_00_YNOR_COMMAND_CENTER\ynor_integrity_audit.ps1
Taille : 3137 octets
SHA256 : f1c1db7e4888cdf25910db9e4723715fa2324dfb00878c114f45a4d8cee17026

```text
# =============================================================================
# MDL YNOR - AUTOMATED INTEGRITY AUDIT SCRIPT (V2.3)
# =============================================================================
$ErrorActionPreference = "SilentlyContinue"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "--- INITIALISATION DE L'AUDIT D'INTÉGRITÉ MDL YNOR ---" -ForegroundColor Cyan
Write-Host "Localisation : $RootDir" -ForegroundColor Gray

# 1. Vérification du Silent Kernel dans la base de connaissance
Write-Host "[1/4] Vérification de la configuration déclarée..." -ForegroundColor Yellow
$knowledgePath = Join-Path $RootDir "_00_DISTS_AND_RELEASES\MDL_YNOR_GPT_ULTIMATE_UPLOAD_V17\mdl_global_knowledge.json"
if (Test-Path $knowledgePath) {
    $content = Get-Content $knowledgePath -Raw
    if ($content) {
        $json = $content | ConvertFrom-Json
        $status = $json.system_meta.security_protocols.SILENT_KERNEL
        Write-Host "Statut Silent Kernel : $status" -ForegroundColor Green
    } else {
        Write-Host "ERREUR : Fichier JSON vide." -ForegroundColor Red
    }
} else {
    Write-Host "ERREUR : Fichier de connaissance introuvable à : $knowledgePath" -ForegroundColor Red
}

# 2. Vérification du Hash SHA256 de la Spécification Formelle
Write-Host "`n[2/4] Calcul de l'empreinte de la spécification..." -ForegroundColor Yellow
$specPath = Join-Path $RootDir "YNOR_FULL_CORPUS_FORMAL_SPEC_V2.3.md"
if (Test-Path $specPath) {
    $hash = (Get-FileHash $specPath -Algorithm SHA256).Hash
    Write-Host "SHA256 Actuel : $hash" -ForegroundColor Gray
    Write-Host "Note: Comparez ce hash avec la valeur SIGN dans le manifeste." -ForegroundColor White
} else {
    Write-Host "ERREUR : Spécification formelle introuvable." -ForegroundColor Red
}

# 3. Test de l'API Local (Heartbeat)
Write-Host "`n[3/4] Test de liaison avec l'API Ynor (Localhost:8492)..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8492/status" -Method Get -TimeoutSec 2
    $mu = $response.mu
    Write-Host "API Status : OK" -ForegroundColor Green
    Write-Host "Marge de Viabilité (mu) : $mu" -ForegroundColor ($mu -ge 0 ? "Green" : "Red")
} catch {
    Write-Host "ALERTE : API hors ligne ou injoignable. Le Silent Kernel opère en mode ISOLÉ." -ForegroundColor Magenta
}

# 4. Scan des Logs d'Intégrité
Write-Host "`n[4/4] Analyse des logs d'audit récents..." -ForegroundColor Yellow
$logPath = Join-Path $RootDir "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES\mdl_audit_trail.log"
if (Test-Path $logPath) {
    $logs = Get-Content $logPath -Tail 20 | Where-Object { $_ -match "integrity|reclamation|denied|mu|activation" }
    if ($logs) {
        $logs | ForEach-Object { Write-Host "LOG: $_" -ForegroundColor Gray }
    } else {
        Write-Host "Aucune activité d'intégrité suspecte détectée dans les logs récents." -ForegroundColor Green
    }
} else {
    Write-Host "INFO : Aucun log d'audit actif détecté." -ForegroundColor Gray
}

Write-Host "`n--- AUDIT TERMINÉ ---" -ForegroundColor Cyan
pause

```