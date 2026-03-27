@echo off
TITLE LANCEMENT MDL YNOR (NGROK TUNNEL)
cd /d "c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework"
echo =======================================================
echo    ARCHITECTURE SURVOLTE MDL YNOR (CHArLIER RONY)
echo       Lancement via Tunnel NGROK de Secours
echo =======================================================
powershell -ExecutionPolicy Bypass -File "start_mdl_ngrok.ps1"
pause
