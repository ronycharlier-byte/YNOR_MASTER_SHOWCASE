# LISTE BLANCHE DE DIFFUSION ET PLAN DE NETTOYAGE

## Objet
Ce document fixe deux choses:
1. ce qui peut sortir dans une diffusion propre
2. ce qui doit rester interne, technique ou archivé

Il sert de garde-fou pour éviter de mélanger corpus éditorial, artefacts de travail et caches d'execution.

## Liste Blanche De Diffusion
### Niveau Public
- `00_HOMEPAGE/HOMEPAGE_DU_CORPUS.md`
- `00_HOMEPAGE/SITE_MAP.md`
- `00_PUBLIC_BRIEF/PUBLIC_BRIEF.md`
- `00_PUBLIC_BRIEF/PRESENTATION_PUBLIQUE.md`

### Niveau Executive
- `00_EXECUTIVE_DIGEST/EXECUTIVE_DIGEST.md`
- `00_EXECUTIVE_DIGEST/FICHE_UNE_PAGE.md`

### Niveau Canonique
- `00_EDITION_CANONIQUE_FINALE/PORTAIL_CANONIQUE_FINAL.md`
- `00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/INDEX_MAITRE_FRACTAL_CHIASTIQUE.md`
- `00_EDITION_CANONIQUE_FINALE/01_DOCUMENTS_CENTRAUX/CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`

### Niveau Master
- `INDEX_MAITRE_FRACTAL_CHIASTIQUE.md`
- `CARTE_VISUELLE_FRACTALE_CHIASTIQUE.md`
- `RECAPITULATION_FINALE.md`
- `MANIFESTE_FRACTAL_CHIASTE_UNIVERSEL.md`

### Niveau Soumission
- `00_SUBMISSION_PACK/MANUSCRIT_FINAL.md`
- `00_SUBMISSION_PACK/LETTRE_DE_COUVERTURE.md`
- `00_SUBMISSION_PACK/JOURNAL_TARGETING.md`
- `00_SUBMISSION_PACK/RESUME_DE_SOUMISSION.md`
- `00_SUBMISSION_PACK/STRUCTURE_DE_LIVRAISON.md`

### Branches Documentaires A Garder Dans La Diffusion
- `01_A_FONDATION`
- `02_B_THEORIE_ET_PREUVES`
- `03_C_MOTEURS_ET_DEPLOIEMENT`
- `04_X_NOYAU_MEMOIRE`
- `05_C_PRIME_VALIDATION_ET_TESTS`
- `06_B_PRIME_GOUVERNANCE_ET_DIFFUSION`
- `07_A_PRIME_ARCHIVES_ET_RELEASES`

## Hors Diffusion
### Artefacts Techniques
- `.git`
- `.venv`
- `.pytest_cache`
- `.uv-cache`
- `__pycache__`
- `*.pyc`
- `*.log`
- `*.tmp`

### Journaux Et Traces
- `logs`
- tout fichier de trace ou de runtime non editorial

### Miroirs Techniques
- les copies textuelles de caches, logs et artefacts de build
- les dossiers miroir qui ne servent qu'a reproduire l'etat de travail

## Plan De Nettoyage
### Etape 1 - Isolation
- Marquer explicitement les repertoires techniques comme hors diffusion.
- Eviter de les compter dans les statistiques documentaires.
- Les conserver seulement dans les zones d'archive ou de travail interne.

### Etape 2 - Separation
- Distinguer corpus editorial et outillage.
- Ne pas melanger sources, caches, logs et environnements d'execution dans les inventaires publics.
- Conserver une frontiere nette entre texte publie et texte de travail.

### Etape 3 - Normalisation
- Garder une seule source canonique par document.
- Conserver une seule version miroir par source, avec alias si necessaire.
- Harmoniser les noms visibles et les encodages.

### Etape 4 - Filtrage
- Exclure les caches Python, les environnements virtuels et les journaux des packages de diffusion.
- Retirer les fichiers temporaires et les reliquats de build des dossiers publics.
- Verifier que les manifests ne comptent que le contenu editorial utile.

### Etape 5 - Verification
- Refaire un scan des couches visibles apres nettoyage.
- Verifier qu'aucun `__pycache__`, `.venv`, `.pytest_cache`, `.uv-cache`, `.git` ou `logs` ne remonte dans la diffusion.
- Confirmer que les points d'entree publics restent lisibles et coherents.

## Regle Pratique
Si un fichier sert a exécuter, tester, compiler, journaliser ou mettre au point le corpus, il reste interne.
Si un fichier sert a lire, comprendre, diffuser ou remettre le corpus, il peut entrer dans la liste blanche.

## Synthese
- Diffusion: documents de lecture, d'index, de navigation, de synthese et de soumission.
- Interne: caches, logs, environnements virtuels, depots embarques, fichiers temporaires et artefacts techniques.

