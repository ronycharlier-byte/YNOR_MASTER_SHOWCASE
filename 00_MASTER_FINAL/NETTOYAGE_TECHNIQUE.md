# NETTOYAGE TECHNIQUE

## Objet
Formaliser le traitement du bruit interne afin qu'il reste distinct du corpus de diffusion.

## Artefacts Internes A Isoler
- `.git`
- `.venv`
- `.pytest_cache`
- `.uv-cache`
- `__pycache__`
- `*.pyc`
- `*.log`
- `*.tmp`
- `logs`

## Regle
Les artefacts ci-dessus servent au travail, au test, a l'execution ou au diagnostic.
Ils ne doivent pas etre comptabilises comme contenu editorial ni exposes comme points de lecture publique.

## Usage Pratique
- Les conserver dans les espaces internes si necessaire.
- Les exclure des listes blanches de diffusion.
- Les faire apparaitre uniquement dans les documents de maintenance ou d'audit.

## Resultat Attendu
Le corpus editorial reste lisible, tandis que le bruit technique demeure localise et hors diffusion.

