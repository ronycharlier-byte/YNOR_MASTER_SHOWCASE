# RELEASE PIPELINE

## Objectif
Faire passer la branche `C` du mode local au mode distribuable sans casser la coherence operationnelle.

## Pipeline Recommande
1. Developper ou ajuster le moteur.
2. Valider localement via `status`, `mu/check` et le dashboard.
3. Examiner les logs.
4. Verifier les secrets et la revocation.
5. Construire le paquet de distribution.
6. Archiver la version de reference.

## Artefacts De Distribution Observes
- `Dockerfile`
- `requirements.txt`
- `ynor_api_server.py`
- `ynor_dashboard_ui.py`
- `ynor_sdk/`
- `build_secure_sdk.py`
- `PUSH_TO_CLOUD.bat`

## Routines A Garder Stables
- port API
- nom de l en-tete d authentification
- format des fichiers de logs
- structure des reponses API
- presence de la page `/dashboard`

## Ce Qu Une Release Doit Garantir
- demarrage reproductible
- comportement documente
- acces limite et trace
- absence de secrets dans le paquet
- compatibilite avec le monitor et le terminal

## Controles Avant Tag
- l API se lance
- le dashboard s affiche
- le tunnel marche si demande
- les tests de `C'` ont ete passes
- l archive finale pointe vers le bon commit ou le bon ensemble de fichiers

## Relation Avec `A'`
Cette pipeline est une passerelle vers la branche archive/release. Elle ne remplace pas `A'`, mais prepare la sortie propre du corpus.
