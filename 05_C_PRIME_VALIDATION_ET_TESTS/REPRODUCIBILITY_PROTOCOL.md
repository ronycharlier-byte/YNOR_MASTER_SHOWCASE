# REPRODUCIBILITY PROTOCOL

## Objectif
Definir comment rejouer les audits du corpus avec un maximum de determinisme.

## Principes
- fixer les graines aleatoires quand le script le permet
- isoler les fichiers temporaires
- garder les entrees de test compactes
- rendre le chemin de travail explicite
- separer les validations deterministes des benchmarks stochastiques

## Protocoles Observes
### Validation scientifique
- script: `hardcore_validation.py`
- graine par defaut: `42`
- comportement attendu: `mu` proche de `1.4`

### Experience de mutation
- script: `run_experiment.py`
- graine par defaut: `101`
- comportement attendu: passage d un etat instable a un etat plus stable

### Test d integration partageable
- script: `tests/test_shareable_mu_audit.py`
- stockage isole via `tmp_path`
- comportement attendu: lien public cree et evenements traces

## Point Sensible
Le benchmark global `mdl_ynor_ultimate_benchmark_v3.py` melange des mesures structurelles et des tirages aleatoires pour certaines composantes. Il est donc utile comme audit de tendance, mais pas comme reference numerique parfaitement deterministic sans ajustement supplementaire.

## Procedure Recommandee
1. Fixer `PYTHONHASHSEED` si besoin.
2. Fixer les graines numpy dans les scripts qui le permettent.
3. Isoler les fichiers JSON de runtime dans un repertoire temporaire.
4. Lancer les tests unitaires.
5. Lancer les audits de robustesse.
6. Comparer les resultats avec les sorties de reference.

## Sorties A Conserver
- rapport pytest
- JSON d audit si produit
- traces de benchmark
- journaux d erreur si un test echoue

## Regle D Or
Un test est reproductible seulement si ses donnees, ses graines et son espace d ecriture sont tous controles.

