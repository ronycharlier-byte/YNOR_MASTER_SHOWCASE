# BENCHMARK REPORT

## But
Centraliser les points de benchmark visibles dans le corpus et clarifier ce qu ils mesurent.

## Benchmarks Visibles
### `hardcore_validation.py`
- finalite: audit scientifique simple du calcul mu
- signal attendu: `mu` autour de `1.4`
- usage: verification rapide de la formule de base

### `run_experiment.py`
- finalite: montrer qu une mutation structurelle peut stabiliser un systeme
- signal attendu: progression entre `mu_initial` et `mu_mutated`
- usage: demonstration reproducible de stabilisation

### `ynor_functional_analysis_benchmark.py`
- finalite: audit de raisonnement mathematique de pointe (Schrodinger alpha/x^2)
- signal attendu: identification exacte des seuils -1/4 et 3/4
- usage: benchmark FrontierMath de souverainete intellectuelle

### `mdl_ynor_ultimate_benchmark_v3.py`
- finalite: audit global du corpus
- axes: structure, mathematique, geophysique, quant finance, knowledge sync, performance I/O
- usage: score canonique global et rapport JSON

### `BENCHMARK_FRONTIER_MATH.md`
- finalite: benchmark externe de haut niveau (Epoch AI)
- axes: raisonnement mathematique avance, preuve vs heuristique
- usage: evaluation du raisonnement sous forte complexite

## Ce Que Le Benchmark Mesure
- presence des modules critiques
- coherence mu
- presence de la base de connaissance
- capacite de lecture et ecriture (I/O)
- precision du raisonnement formel (Schrodinger)
- comportement du systeme dans des cas de charge simples

## Limites
- le benchmark global est plus proche d un audit composite que d un benchmark strictement scientifique
- certaines composantes utilisent des tirages aleatoires
- la partie hardware est partiellement mockee dans le code lu

## Format De Sortie
- console texte pour la lecture humaine
- JSON pour l archivage machine si produit
- trace de duree pour comparaison de performance

## Utilisation Recommandee
1. lancer d abord le test unitaire de robustesse
2. lancer ensuite la validation scientifique
3. lancer l experience de mutation
4. lancer le benchmark global
5. referer a FrontierMath pour l evaluation du raisonnement mathematique de pointe

## Lecture Du Resultat
- `OPTIMAL`: corpus solide
- `SECURE`: corpus acceptable mais a surveiller
- `DEGRADED`: des zones de fragilite persistent

