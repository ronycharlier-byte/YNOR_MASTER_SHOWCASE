# API CONTRACT

## Scope
Contrat observe de la couche API exposee par `ynor_api_server.py`.

## Convention Generale
- Header d authentication: `X-Ynor-API-Key`
- Format d echange principal: JSON
- Mode d ecriture: bloque par defaut sauf si `MDL_PROD_WRITE_ENABLED=TRUE`
- Gestion des cles: chargement via `.env` et `secrets.local.json`
- Protection supplementaire: liste de revocation, quota, suivi des evenements

## Endpoints
### `POST /v1/mu/evaluate`
Evalue la viabilite mu d une requete ou d un etat agent.

Usage attendu:
- entree JSON representee par `AgentStatePayload`
- sortie JSON avec `mu`, `should_halt`, `reason`, `metrics`, `billing` et `watermark`
- peut creer un partage public si l option de partage est activee

### `POST /v1/agent/hierarchical_query`
Execute la couche hierarchique de traitement.

Usage attendu:
- entree JSON representee par `HierarchicalPayload`
- cle API obligatoire
- retourne un resultat d orchestration ou de reponse hierarchique

### `POST /v1/admin/revoke_key`
Coupe circuit de revocation d une cle.

Usage attendu:
- entree JSON representee par `RevokePayload`
- reserve a l administration
- doit laisser une trace de revocation

### `POST /v1/archive/auto_learn`
Enregistre un retour d experience pour auto-apprentissage ou journalisation.

Usage attendu:
- entree JSON representee par `AutoLearnPayload`
- cle API obligatoire
- utilise pour alimenter les evenements et archives d apprentissage

### `POST /run`
Point d entree conversationnel ou cognitif principal.

Usage attendu:
- cle API obligatoire
- corps de requete libre ou semi-structure selon l orchestrateur
- retourne une reponse orchestree par le moteur

### `GET /status`
Diagnostic public minimal.

Usage attendu:
- retourne un etat de sante synthetique
- ne doit pas exposer de secrets

### `GET /v1/mu/history`
Historique mu protege.

Usage attendu:
- cle API obligatoire
- retourne les derniers evenements mu persistants

### `GET /v1/mu/check`
Verification rapide et publique.

Usage attendu:
- lecture simple
- utile pour les dashboards et les pages iframe

### `GET /share/mu/{share_id}`
Affichage public d un audit partage.

Usage attendu:
- lecture seule
- identifiant de partage non secret mais non devinable

### `GET /v1/growth/events`
Evenements de croissance ou de telemetrie.

Usage attendu:
- cle API obligatoire
- lecture analytique

### `GET /dashboard`
Rendu HTML du dashboard interne.

Usage attendu:
- usage humain local ou tunnelise
- ne doit pas servir de source d ecriture

### `GET /privacy`
Page legale / politique de confidentialite.

## Contraintes Fonctionnelles
- Les cles invalides ou revoquees doivent echouer proprement.
- Les appels sensibles doivent etre limites par quota ou rate limit.
- Les payloads doivent rester compacts et journalisables.
- Les reponses publiques doivent etre neutralisees si elles contiennent des elements sensibles.

## Inference Importante
Les schemas exacts des classes `AgentStatePayload`, `HierarchicalPayload`, `RevokePayload` et `AutoLearnPayload` doivent etre lus directement dans le fichier source, car le contrat fonctionnel ici est une synthese de leur usage observe.
