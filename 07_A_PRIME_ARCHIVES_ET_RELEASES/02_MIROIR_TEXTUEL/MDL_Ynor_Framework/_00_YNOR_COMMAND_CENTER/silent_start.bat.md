# MIROIR TEXTUEL - silent_start.bat

Source : MDL_Ynor_Framework\_00_YNOR_COMMAND_CENTER\silent_start.bat
Taille : 239 octets
SHA256 : 4e35a7567d4f8dddb14a53fdaee13d670f3094e746aa606fad941e24a52e9c0c

```text
@echo off
:: Ce script lance l'API Cloud Ynor sans afficher de fenetre visible
cd /d "C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API"
python -m uvicorn ynor_api_server:app --port 8492 --host 0.0.0.0

```