# CI GUIDE

## Objectif
Expliquer comment la validation continue du corpus est structuree dans les workflows existants.

## Workflows Visibles
### `mdl_full_check.yml`
- declenchement: `push` et `pull_request` sur `main` et `master`
- plateforme: `ubuntu-latest`
- Python: `3.10`
- etapes: installation, pytest, audit scientifique, execution notebook, auto-push du notebook execute

### `ynor_ci.yml`
- declenchement: `push` et `pull_request` sur `main`
- plateforme: `ubuntu-latest`
- Python: `3.10`
- etapes: installation, tests unitaires, validation core, scan de securite, build du SDK

## Ce Que La CI Valide Deja
- tests `pytest`
- robustesse mu
- audit scientifique
- execution reproductible d un notebook
- scan de secrets simples
- generation du SDK securise

## Ordre Recommande
1. tests unitaires et integration
2. audit de robustesse
3. audit de reproductibilite
4. build du SDK
5. checks de securite
6. execution notebook si le contexte le permet

## Points D Attention
- `mdl_full_check.yml` tente un auto-push de notebook; cela suppose une authentification GitHub valide
- `ynor_ci.yml` effectue un grep de secrets de type `SK-`, ce qui reste un garde-fou simple mais incomplet
- les chemins d exécution doivent etre cohérents entre la racine du repo et les sous-modules

## Bonne Pratique
- garder les tests sans dependance a des etats persistants externes
- isoler les fichiers de runtime dans les tests
- fixer les seeds pour les scripts de reference
- limiter les effets de bord en CI

## Matrice Minimale CI
- unit tests
- integration API
- validation scientifique
- scan de securite
- build SDK

