@echo off
title YNOR CLOUD DEPLOYMENT PORTAL
color 0B
setlocal enabledelayedexpansion

echo ==========================================================
echo        YNOR CORE - ACTIVATION DU DEPLOIEMENT CLOUD
echo ==========================================================
echo.
echo [*] Initialisation du depot Git local...
git init

echo.
echo [*] Indexation des fichiers (Securisee par .gitignore)...
git add .

echo.
echo [*] Creation du snapshot de déploiement...
git commit -m "Deployment of MDL Ynor Cloud-Ready Version v2.1"

echo.
echo [*] Branche par defaut: main
git branch -M main

echo.
echo ----------------------------------------------------------
echo        PROCHAINE ETAPE : CONFIGURER VOTRE REPO GITHUB
echo ----------------------------------------------------------
echo.
echo 1. Creez un depot VIDE sur GitHub (ex: Ynor-API-Cloud)
echo 2. Copiez l'URL HTTPS du depot (ex: https://github.com/votre_nom/repo.git)
echo.
set /p giturl="Collez l'URL de votre depot GitHub ici : "

if "!giturl!"=="" (
    echo [!] ERREUR: Aucune URL saisie. Recommencez.
    pause
    goto eof
)

git remote add origin !giturl!
echo.
echo [*] Envoi des donnees vers le nuage (Pushing to main)...
git push -u origin main --force

echo.
echo ==========================================================
echo        [SUCCESS] CODE ENVOYE VERS GITHUB !
echo ==========================================================
echo.
echo Allez maintenant sur Render.com > New Web Service > Connect Repo.
echo N'oubliez pas d'ajouter YNOR_API_KEY et OPENAI_API_KEY dans l'onglet Environment.
pause

:eof
exit
