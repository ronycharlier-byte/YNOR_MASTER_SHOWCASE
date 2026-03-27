# MANIFESTE D'EXCLUSION DE DIFFUSION

## Objet
Ce manifeste definit les artefacts techniques qui ne doivent pas entrer dans la diffusion publique du corpus.

## Regle Generale
Tout element qui sert a executer, compiler, tester, journaliser ou isoler un environnement de travail reste interne.

## Elements Exclure
- `.git`
- `.venv`
- `.pytest_cache`
- `.uv-cache`
- `__pycache__`
- `*.pyc`
- `*.log`
- `*.tmp`
- `logs`

## Application
Ces elements:
- ne sont pas comptes comme contenu editorial
- ne sont pas inclus dans les paquets de diffusion
- peuvent rester presents dans les espaces de travail internes et les miroirs techniques

## Complement
Ce manifeste doit etre lu avec:
- `LISTE_BLANCHE_DIFFUSION_ET_PLAN_NETTOYAGE.md`
- `STRUCTURE_DE_LIVRAISON.md`
- `SUITE_CORPUS_ACTIONNELLE.md`

