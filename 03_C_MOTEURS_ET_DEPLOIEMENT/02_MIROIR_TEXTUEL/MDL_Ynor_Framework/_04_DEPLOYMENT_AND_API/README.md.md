# MIROIR TEXTUEL - README.md

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\README.md
Taille : 655 octets
SHA256 : 3986e7fd1ba8c5d6ea596192a8f23b73c5b48ade5c486c3ce0dec240172235ef

```text
# 📡 PÔLE DÉPLOIEMENT & API
**MDL YNOR FRAMEWORK**

Ce dossier contient l'infrastructure nécessaire pour exposer l'AGI Ynor au monde extérieur.

## 📁 CONTENU
- **`ynor_api_server.py`** : Serveur FastAPI principal gérant les audits mu et les requêtes stratégiques.
- **`ynor_sdk/`** : Client Python pour intégrer Ynor dans d'autres applications.
- **`Dockerfile`** : Configuration pour l'isolation et le déploiement Cloud.

## 🚀 LANCEMENT
```bash
uvicorn ynor_api_server:app --host 0.0.0.0 --port 8000
```

## 🔒 SÉCURITÉ
Le serveur utilise `python-dotenv`. Assurez-vous d'avoir configuré votre fichier `.env` à la racine du projet.

```