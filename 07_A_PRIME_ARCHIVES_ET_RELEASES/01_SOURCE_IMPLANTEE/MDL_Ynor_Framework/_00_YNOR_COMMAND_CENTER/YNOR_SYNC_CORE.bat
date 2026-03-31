@echo off
setlocal
title YNOR CORE BRAIN SYNC

echo ========================================================
echo         YNOR CORE - MISE  JOUR DU CERVEAU AGI
echo ========================================================
echo.
echo [1] - AJOUTER UNE EXPRIENCE / CHAT LOG (Ouvrir le Journal)
echo [2] - SYNCHRONISER LA CONNAISSANCE (Lancer l'Indexeur)
echo [3] - VOIR LES PROTOCOLES DE SCURIT
echo [4] - QUITTER
echo.

set /p choice="Action (1-4) : "

if "%choice%"=="1" (
    echo.
    echo [*] Ouverture du journal d'experience...
    start notepad "c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES\MDL_YNOR_CUSTOMER_EXPERIENCE_LOGS.md"
    echo [!] Une fois vos logs colles et enregistres, relancez ce script et faites [2].
    pause
    goto end
)

if "%choice%"=="2" (
    echo.
    echo [*] Lancement de l'indexation globale (mu-scaling)...
    cd /d "c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_YNOR_GPT_KNOWLEDGE"
    python update_knowledge.py
    echo.
    echo [OK] Cerveau AGI a jour et synchronise.
    pause
    goto end
)

if "%choice%"=="3" (
    echo.
    echo [*] Affichage des protocoles de securite actuels...
    type "c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_00_YNOR_COMMAND_CENTER\mdl_ynor_manifesto_governance.json"
    pause
    goto end
)

if "%choice%"=="4" exit

:end
exit



