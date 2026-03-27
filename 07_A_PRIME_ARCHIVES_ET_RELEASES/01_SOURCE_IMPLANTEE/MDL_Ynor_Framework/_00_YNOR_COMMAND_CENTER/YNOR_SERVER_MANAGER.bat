@echo off
setlocal
cd /d "%~dp0"

IF "%1"=="AUTO" GOTO auto_start

:menu
cls
echo ==========================================
echo    MDL YNOR - SYSTEM COMMAND CENTER (v3.1)
echo          MILLENNIUM EDITION
echo ==========================================
echo [1] - Verifier Environnement (Dep)
echo [2] - Lancer API Ynor (Localhost:8492)
echo [3] - Lancer Dashboard (Admin Panel)
echo [4] - Lancer les Tests (Validation)
echo [5] - Creer le Pont Internet (Ngrok)
echo [6] - Sync GPT Upload (ZIP)
echo [7] - CONFIGURER DEMARRAGE AUTO (Windows)
echo [0] - Quitter
echo ==========================================
set /p opt="Choix : "

if "%opt%"=="1" goto dep
if "%opt%"=="2" goto api
if "%opt%"=="3" goto dash
if "%opt%"=="4" goto test
if "%opt%"=="5" goto ngrok
if "%opt%"=="6" goto sync
if "%opt%"=="7" goto register_task
if "%opt%"=="0" exit
goto menu

:auto_start
echo [AUTO] Activation du Noyau MDL Ynor...
start "Ynor API" /min cmd /c "uvicorn _04_DEPLOYMENT_AND_API.ynor_api_server:app --host 127.0.0.1 --port 8492"
timeout /t 5
start "Ynor Ngrok" /min cmd /c "ngrok http --domain=mdlynor.ngrok-free.app 8492"
exit

:api
start "Ynor API" cmd /k "uvicorn _04_DEPLOYMENT_AND_API.ynor_api_server:app --host 127.0.0.1 --port 8492"
goto menu

:ngrok
start "Ynor Ngrok" cmd /k "ngrok http --domain=mdlynor.ngrok-free.app 8492"
goto menu

:register_task
echo Configuration du demarrage automatique de Windows...
powershell -Command "$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/c \"%~dp0YNOR_SERVER_MANAGER.bat\" AUTO'; $trigger = New-ScheduledTaskTrigger -AtLogOn; Register-ScheduledTask -Action $action -Trigger $trigger -TaskName 'MDLYnor_AutoStart' -Description 'Lancement automatique du noyau AGI MDL Ynor' -Force"
echo Tache 'MDLYnor_AutoStart' enregistree avec succes !
pause
goto menu

:dep
pip install -r requirements.txt
pause
goto menu

:dash
start http://localhost:8492/dashboard
goto menu

:test
pytest
pause
goto menu

:sync
copy "_04_DEPLOYMENT_AND_API\GPT_ACTION_SCHEMA.yaml" "MDL_YNOR_GPT_UPLOAD_V3\GPT_ACTION_SCHEMA.yaml" /y
powershell -Command "Compress-Archive -Path MDL_YNOR_GPT_UPLOAD_V3\* -DestinationPath MDL_YNOR_GPT_UPLOAD_V3.zip -Force"
echo ZIP Synchronise.
pause
goto menu
