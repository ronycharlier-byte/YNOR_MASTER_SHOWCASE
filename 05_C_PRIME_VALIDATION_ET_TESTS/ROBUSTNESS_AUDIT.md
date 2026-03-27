# ROBUSTNESS AUDIT

## Objet
Synthese de robustesse pour les fonctions et surfaces de `C` deja visibles dans la branche miroir.

## Observations Sur Le Calcul Mu
Le test `test_mdl_robustness.py` couvre:
- un cas standard
- un cas d amplification extreme
- un etat nul
- un cas non lineaire
- un cas haute dimension

Inference raisonnable:
- le coeur numerique de `YnorSystem.measure_dissipative_margin` est considere comme critique
- la gestion des limites doit rester explicite, surtout pour les etats nuls et les dimensions elevees

## Observations Sur Les Partages Publics
Le test `test_shareable_mu_audit.py` montre que:
- un appel a `/v1/mu/evaluate?share=true` doit produire une structure de partage
- la page publique doit afficher l audit et son watermark
- les evenements de croissance doivent conserver les traces de partage et de consultation

## Observations Sur Les Scripts De Recherche
Les scripts `hardcore_validation.py` et `run_experiment.py` indiquent que:
- la robustesse attendue n est pas purement statique
- les graines servent a comparer des etats avant et apres transformation
- la stabilite mu est la mesure directrice

## Points De Fragilite
- certaines mesures de benchmark restent aleatoires si la graine n est pas forcee
- les fichiers de runtime peuvent se melanger aux fichiers source si l isolation est insuffisante
- la CI peut varier si les dependances ou les chemins ne sont pas locks

## Recommandations
1. figer les seeds pour les scripts de reference
2. rediriger les fichiers d audit vers des repertoires temporaires
3. ajouter des tests de cle invalide et de cle revoquee
4. ajouter des tests de payload vide et d erreur de schema
5. ajouter un test de non regression sur `/status`

## Verdict
La base de robustesse est deja presente, mais elle doit etre durcie sur les bords: erreurs d entree, etats vides, calculs concurrentiels et reproductibilite des audits globaux.

