# TEST MATRIX

## Vue D Ensemble
La matrice couvre les tests actuellement visibles dans le corpus et les extensions naturelles a ajouter pour solidifier `C`.

## Tests Existants
### `tests/test_mdl_robustness.py`
- cible: `YnorSystem.measure_dissipative_margin`
- couverture: calcul mu, amplification extreme, etat nul, non linearite, haute dimension
- type: test unitaire de robustesse numerique

### `tests/test_shareable_mu_audit.py`
- cible: `POST /v1/mu/evaluate`, `GET /share/mu/{share_id}`, `GET /v1/growth/events`
- couverture: creation d un partage public, affichage de la page partagee, journalisation des evenements
- type: test d integration API

## Benchmarks et Audits Existants
### `hardcore_validation.py`
- cible: audit scientifique de stabilite
- point fixe: seed `42`
- resultat attendu: `mu` proche de `1.4`

### `run_experiment.py`
- cible: mutation d un systeme instable vers un systeme stable
- point fixe: seed `101`
- resultat attendu: amelioration de `mu`

### `mdl_ynor_ultimate_benchmark_v3.py`
- cible: audit global du corpus
- axes: structure, mathematique, geophysique, quant finance, knowledge sync, hardware
- remarque: le script utilise des appels aleatoires pour certaines mesures, donc il doit etre isole si on cherche une reproductibilite stricte

## Extensions Recommandees
### Robustesse API
- verifier les clees invalides
- verifier les clees revoquees
- verifier les limites de quota
- verifier les reponses sur payload vide ou mal forme

### Robustesse Donnees
- verifier les ecritures concurrentes sur les fichiers JSON
- verifier les retours quand un fichier de log manque
- verifier la reprise apres corruption de fichier temporaire

### Robustesse Dashboard
- verifier `/dashboard`
- verifier le dashboard Streamlit sans API distante
- verifier le monitor HTML si les logs sont absents

### Robustesse CI
- verifier que les workflows s arretent proprement si les dependances sont absentes
- verifier que les tests ne depandent pas d etats persistants hors sandbox

## Grille D Evaluation
- `PASS`: le comportement attendu est stable et observable
- `FAIL`: le comportement attendu n est pas respecte
- `FLAKY`: le comportement depend d un hasard non controle
- `BLOCKED`: le test ne peut pas s executer sans precondition externe

## Priorite
1. robustesse du calcul mu
2. robustesse des partageables publics
3. robustesse des chemins de lecture/ecriture
4. robustesse CI et benchmark

