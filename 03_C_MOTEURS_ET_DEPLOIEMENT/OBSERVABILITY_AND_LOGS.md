# OBSERVABILITY AND LOGS

## Objectif
Definir ce qui doit etre observe, journalise et relu pour que `C` reste diagnostiable.

## Sources De Telemetrie
- `usage_stats.json`
- `mu_audit_history.json`
- `shared_audits.json`
- `growth_events.json`
- `revocation_list.json`
- logs `uvicorn_*.log`
- logs `uvicorn_errors_*.log`
- logs `ngrok_*.log`
- logs `cloudflare_errors_*.log`
- `mdl_security_audit.log`

## Signaux Importants
- nombre d appels API
- erreurs de validation
- cles revoquees
- taux de partage public
- historique des scores mu
- presence de divergences
- statut du tunnel externe

## Endpoints Utiles
- `GET /status`
- `GET /v1/mu/check`
- `GET /v1/mu/history`
- `GET /v1/growth/events`
- `GET /share/mu/{share_id}`

## Ce Qu On Doit Pouvoir Diagnostiquer
- un moteur qui ne demarre pas
- une cle API refusee
- un quota atteint
- un partage public absent
- un dashboard qui ne se rafraichit plus
- un tunnel coupe

## Regles De Journalisation
- horodater chaque evenement important
- masquer les cles partiellement
- tronquer les journaux volumineux
- conserver des fichiers lisibles par session

## Bonnes Pratiques
- separer logs applicatifs et logs d erreur
- surveiller le fichier de PID si un script le produit
- utiliser des traces courtes mais exploitables
- preferer des indicateurs de sante simples et stables

## Inference
La structure exacte des journaux derives peut varier selon le script de lancement utilise. Cette page decrit le socle commun observable dans les fichiers de la branche.
