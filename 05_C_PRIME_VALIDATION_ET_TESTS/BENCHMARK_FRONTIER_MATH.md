# BENCHMARK EXISTANT — FRONTIERMATH

## Présentation
**Nom du benchmark :** FrontierMath
**Nature :** Benchmark existant de raisonnement mathématique avancé. Il a été conçu autour de problèmes originaux, non publiés, afin de limiter au maximum la contamination par mémorisation et de tester un raisonnement réellement soutenu.

## Fondement
FrontierMath est structuré en plusieurs niveaux de difficulté (“tiers”), allant de l'olympiade de haut niveau à la recherche pure :
- **Tiers 1–3 (Base Set) :** 300 problèmes couvrant la théorie des nombres, la géométrie algébrique, l'analyse réelle et la combinatoire.
    - **Tier 1 :** Équivalent aux problèmes d'olympiades nationales/internationales.
    - **Tiers 2 & 3 :** Expertise de niveau master/doctorat (résolution par un expert en plusieurs heures/jours).
- **Tier 4 (Expansion Set) :** 50 problèmes de niveau recherche (résolution par un expert en plusieurs semaines).

## Métriques d'Évaluation (Epoch AI)
Le benchmark évalue la difficulté selon trois axes :
- **Background (1-5) :** Niveau de connaissances (1: Lycée, 3: Licence, 5: Recherche).
- **Creativity :** Temps estimé pour identifier l'idée clé de la solution.
- **Execution :** Temps estimé pour finaliser la preuve/calcul après l'idée clé.

## Pourquoi c’est l’un des plus durs
- **Problèmes originaux :** Conçus pour être "Guess-Proof" et éviter la contamination (Zero-shot contamination).
- **Tool-Assisted :** Les modèles ont accès à des environnements de calcul (Python) pour vérifier leurs étapes, testant ainsi la capacité à utiliser des outils de manière rigoureuse.
- **Difficulté extrême :** Atteint le niveau de la recherche mathématique contemporaine.

## Objectif au sein de l'Architecure MDL Ynor
Tester si un système est capable de :
- Raisonner sous forte complexité.
- Maintenir une cohérence longue sur des preuves multi-étapes.
- Éviter les hallucinations mathématiques.
- Produire une preuve valide ou reconnaître rigoureusement qu’elle ne ferme pas.
- Ne rien affirmer au-delà de ce qui est effectivement démontré.

---
*Note : Ce benchmark est considéré comme l'un des standards les plus exigeants pour l'évaluation de l'AGI mathématique.*
