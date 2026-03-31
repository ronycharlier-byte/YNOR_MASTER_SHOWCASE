# MDL Ynor Corpus API

Cette application expose le corpus documentaire au travers d'une API FastAPI unifiee.

## Lancement

```bash
uvicorn api_app:app --host 0.0.0.0 --port 8492
```

Si vous preferez conserver le runtime historique, l'API originale reste disponible dans la branche `03_C_MOTEURS_ET_DEPLOIEMENT/01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_04_DEPLOYMENT_AND_API/ynor_api_server.py`.

## Surfaces principales

- `/` : tableau de bord du corpus
- `/api/corpus/summary` : statistiques globales
- `/api/corpus/files` : inventaire page
- `/api/corpus/search` : recherche textuelle
- `/api/corpus/file/{path}` : lecture ou telechargement d'un fichier
- `/api/corpus/preview/{path}` : metadonnees et apercu
- `/api/corpus/manifests` : manifests de reference
- `/status` : etat du moteur herite
- `/dashboard` : tableau de bord historique

## Regle de securite

Les fichiers sensibles sont indexes en metadonnees, mais leurs contenus sont rediges.

## Licence

Ce depot est distribue sous licence proprietaire.
Toute utilisation commerciale, redistribution, adaptation ou integration
dans un produit, un service ou une offre remuneree requiert une autorisation
ecrite prealable.

Licences commerciales disponibles sur demande.
