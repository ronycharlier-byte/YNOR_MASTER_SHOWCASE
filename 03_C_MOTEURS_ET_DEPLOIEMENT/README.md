# 03 C MOTEURS ET DEPLOIEMENT

## Role
Branche operationnelle du corpus: moteurs actifs, API, dashboards, scripts de lancement et couche de distribution technique.

## Ce Que Cette Branche Contient
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_04_DEPLOYMENT_AND_API/ynor_api_server.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_04_DEPLOYMENT_AND_API/ynor_dashboard_ui.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/app.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/streamlit_dashboard.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/ynor_dashboard_v2.py`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/start_mdl_servers.ps1`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/start_mdl_servers_cf.ps1`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/start_mdl_ngrok.ps1`
- `01_SOURCE_IMPLANTEE/MDL_Ynor_Framework/_06_SCRIPTS_AND_DASHBOARDS/stop_mdl_servers.ps1`

## Fonction
Cette branche sert a transformer le corpus theoriquement complet en systeme utilisable:
- exposer une API
- fournir une interface de pilotage
- encadrer les secrets et les quotas
- instrumenter les logs et la telemetrie
- preparer les paquets de deploiement

## Entrypoints Principaux
- API locale: `uvicorn ynor_api_server:app --host 0.0.0.0 --port 8492`
- Dashboard de supervision: `http://localhost:8493`
- Dashboard API natif: `http://localhost:8492/dashboard`
- Status rapide: `http://localhost:8492/status`

## Documents De Reference
- [API_CONTRACT.md](./API_CONTRACT.md)
- [DEPLOYMENT_PLAYBOOK.md](./DEPLOYMENT_PLAYBOOK.md)
- [DASHBOARD_SPEC.md](./DASHBOARD_SPEC.md)
- [OBSERVABILITY_AND_LOGS.md](./OBSERVABILITY_AND_LOGS.md)
- [RELEASE_PIPELINE.md](./RELEASE_PIPELINE.md)

## Principe De Lecture
Lire d abord la couche d exposition, puis la couche de controle, puis les scripts de lancement. La branche doit rester lisible comme un systeme, pas comme un tas de fichiers de service.
