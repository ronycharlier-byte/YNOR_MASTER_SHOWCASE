# DEPLOYMENT PLAYBOOK

## Objectif
Deployer la branche `C` de facon reproductible, en gardant le controle sur l API, le dashboard et les logs.

## Prerequis
- Python et dependances du projet
- fichier `.env` ou `secrets.local.json`
- cle `YNOR_API_KEY`
- cle optionnelle `YNOR_TEST_KEY`
- option de deploiement tunnelise si publication externe souhaitee

## Sequence Locale Recommandee
1. Verifier que le repertoire source est present.
2. Verifier les secrets locaux.
3. Lancer l API unifiee sur le port `8492`.
4. Ouvrir le dashboard Streamlit sur le port `8501`.
5. Valider `/api/corpus/status` et `/api/corpus/summary`.
6. Si besoin, ouvrir un tunnel `ngrok` ou `cloudflared`.

## Lancement Standard
### API
```bash
python -m uvicorn api_app:app --host 0.0.0.0 --port 8492
```

### Dashboard local
- `streamlit_dashboard.py` pour l exploration du corpus
- `app.py` pour l audit mu et la visualisation de viabilite
- `ynor_dashboard_v2.py` pour le monitor HTML/FastAPI

## Scripts De Travail
- `start_local_stack.ps1` lance l API et le dashboard Streamlit
- `stop_local_stack.ps1` arrete proprement les processus
- `start_mdl_servers.ps1` lance Uvicorn puis ngrok
- `start_mdl_servers_cf.ps1` lance Uvicorn puis Cloudflare Tunnel
- `start_mdl_ngrok.ps1` lance Uvicorn puis ngrok en mode secours
- `stop_mdl_servers.ps1` arrete proprement les processus

## Ports Observes
- API: `8492`
- Dashboard monitor: `8493`
- Tunnel externe: dependant du provider

## Strategie De Securite
- Ne jamais committer de secrets en clair.
- Garder le mode ecriture bloque sauf besoin explicite.
- Verifier les cles de revocation avant toute exposition externe.
- Preferer les usages locaux ou tunnelises avec acces limite.

## Checklist Avant Publication
- `/api/corpus/status` repond correctement.
- `/api/corpus/summary` charge sans erreur.
- Le dashboard Streamlit affiche les donnees du corpus.
- Les logs sont bien rediriges.
- Le fichier de PID est ecrit si un script de lancement le prevoit.
- Le tunnel public pointe bien vers le bon port.

## Incident Minimum
Si l API ne demarre pas:
- lire `uvicorn_errors_*.log`
- verifier la presence des variables d environnement
- confirmer que le port `8492` est libre
- relancer sans tunnel pour isoler le probleme
