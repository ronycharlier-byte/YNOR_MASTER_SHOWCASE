# ARCHIVE DUPLICATES INDEX YNOR

## Objet
Identifier les couches les plus bruyantes du corpus brut et les traiter comme archive, pas comme lecture principale.

## Etat
- Corpus brut scanne : `1826` fichiers
- Clusters de doublons bruts : `136`
- Entrees concernees par doublons bruts : `381`
- Candidats archive/derive : `933`
- Corpus canonique expose par defaut : `677` fichiers

## Classes D'artefacts A Archiver En Priorite
- miroirs textuels
- exports de rewrite
- doublons de releases
- `*.md.md`
- `*.fractale.md`
- `*.backup.md`
- `*.json.md`
- `*.pdf.md`
- `*.tex.md`
- `*.bin.md`
- sorties `*.out`

## Regle De Purge Prudente
1. Garder un seul representant canonique par hash pour la lecture ordinaire.
2. Conserver les derives en archive seulement si un usage de preuve ou de traçabilité l'exige.
3. Ne pas exposer les miroirs et exports dans les points d'entree publics.
4. Preferer l'exclusion de la vue canonique a la suppression sauvage.

## Point D'acces
- `/api/corpus/archive`
- `/api/corpus/duplicates?scope=raw`

## Conclusion
Le corpus gagne en nettete quand les redondances bruyantes deviennent des artefacts d'archive, non des objets de navigation quotidienne.
