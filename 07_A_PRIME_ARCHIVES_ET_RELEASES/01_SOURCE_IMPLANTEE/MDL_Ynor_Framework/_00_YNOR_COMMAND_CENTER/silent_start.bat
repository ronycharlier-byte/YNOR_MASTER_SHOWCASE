@echo off
:: Ce script lance l'API Cloud Ynor sans afficher de fenetre visible
cd /d "C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API"
python -m uvicorn ynor_api_server:app --port 8492 --host 0.0.0.0



