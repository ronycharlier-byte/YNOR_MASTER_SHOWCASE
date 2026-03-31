# Diagnostic du corpus

## Statut Actuel
- Le corpus est maintenant indexe de maniere plus fiable, avec un suivi explicite des doublons, des couches derivees et des fichiers versionnes.
- Le noyau `04_X_NOYAU_MEMOIRE` dispose d'une entree lisible via `README.md`.
- Les branches `03_C_MOTEURS_ET_DEPLOIEMENT` et `05_C_PRIME_VALIDATION_ET_TESTS` sont presentes et navigables, mais elles restent fortement surrepresentees par des miroirs et des artefacts generes.

## 1. Ce qui manquait vraiment
- Le probleme principal n'est plus l'absence materielle des branches, mais l'absence d'une lecture de qualite au niveau de l'index.
- Le corpus avait besoin d'un comptage clair des doublons logiques, des couches miroir et des variantes de version.
- Sans cette couche, le lecteur voyait un corpus volumineux mais ne pouvait pas distinguer proprement source, derive et archive.
- Les cartes et les points d'entree doivent donc etre compris comme une hierarchie de lecture, pas comme une simple liste de fichiers.

## 2. Bruit technique a isoler
- Les repertoires techniques `\.git`, `\.venv`, `\.pytest_cache`, `\.uv-cache`, `__pycache__` et `logs` doivent rester hors de la diffusion editoriale.
- Les caches, journaux, copies de build, exports temporaires et dossiers miroir ne doivent pas etre comptes comme du contenu canonique.
- Dans certaines branches, le bruit vient surtout des copies textuelles automatiques de fichiers binaires, des `.md.md`, des `.pdf.md`, des `.json.md` et des `.fractale.md`.
- Ce bruit n'est pas forcement une erreur si le corpus sert d'archive de travail, mais il doit etre balise comme derive.

## 3. Doublons et variantes
- Le scan global actuel du depot montre `1 784` fichiers.
- `129` groupes de hachages sont dupliques, pour `367` entrees impliquees, soit `20,6 %` du corpus scanne.
- `23` fichiers sont redactes comme sensibles.
- `150` fichiers sont marques comme versionnes ou fortement historises.
- La vraie dette de maintenance est donc la consolidation des copies, la nomination canonique et la separation visible entre source, miroir et export.
- La valeur academique ne doit pas etre deduite de la seule masse documentaire: elle depend aussi de la verification externe, encore limitee a ce stade.

## 4. Ce qu'il faut normaliser
- Une seule source canonique par document.
- Une seule version miroir textuelle par source, avec alias si necessaire.
- Une separation stable entre diffusion publique, travail interne et archive.
- Une normalisation d'encodage et de typographie pour tous les points d'entree publics.

## Conclusion
- Le corpus est dense et exploitable.
- Les faiblesses restantes sont surtout la redondance, la surcharge de versions et le melange des couches.
- La correction utile n'est pas de supprimer l'historique, mais de le rendre lisible, mesurable et filtrable.
- La couche de preuve interne est solide; la validation externe reste a renforcer.

## Priorites recommandees
- Marquer explicitement les couches miroir et les exports comme derives.
- Stabiliser une source canonique par document.
- Exposer les doublons et les versions dans les tableaux de bord et les API.
- Continuer l'harmonisation typographique des fichiers publics.

## Remediation Appliquee
- La vue par defaut de l'API et de l'accueil utilise maintenant le corpus canonique dedoublonne.
- Les fichiers derives, les versions et les miroirs restent accessibles pour audit, mais ils ne polluent plus la lecture principale.
- Un endpoint de clusters de doublons permet de retrouver les repetitions du corpus brut sans les confondre avec la vue canonique.
- Les totaux visibles distinguent desormais le corpus source, le corpus canonique et la charge d'archive.
