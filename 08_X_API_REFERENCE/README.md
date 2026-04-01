# 08_X_API_REFERENCE - YNOR V10.2.0 TOTAL DIAMOND

Ce répertoire contient la documentation statique de l'API Souveraine **MDL Ynor V10.2.0**.

Il s'adresse aux ingénieurs systèmes et développeurs externes ayant acquis une **Licence Commerciale MDL active** afin de s'intégrer au *Conseil du Logos*.

## Fichiers inclus
- `openapi.json` : Schéma canonique de l'architecture REST du Triumvirat. Intégrable directement dans n'importe quel générateur Swagger/Postman.

## Points d'intégration clés :
Tous les endpoints exigent un en-tête d'authentification propriétaire `X-MDL-Ynor-License`. Toute infraction désactive le pipeline.
