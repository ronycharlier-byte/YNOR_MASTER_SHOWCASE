# 08_X_API_REFERENCE - YNOR V11.2 SATURATED INFORMATION FRAMEWORK

Ce répertoire contient la documentation statique de l'API Canonique **MDL Ynor V11.2**.

Il s'adresse aux ingénieurs systèmes et développeurs externes ayant acquis une **Licence Commerciale MDL active** afin de s'intégrer au Conseil du Logos.

## Fichiers inclus
- `openapi.json` : Schéma canonique de l'architecture REST du Triumvirat. Intégrable directement dans n'importe quel générateur Swagger/Postman.

## Points d'intégration clés :
Tous les endpoints exigent un en-tête d'authentification propriétaire `X-MDL-Ynor-License`. Toute infraction désactive le pipeline.
