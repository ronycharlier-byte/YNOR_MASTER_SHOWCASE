# Diagnostic du corpus

## 1. Ce qui manque dans l'index
- Les deux branches `03_C_MOTEURS_ET_DEPLOIEMENT` et `05_C_PRIME_VALIDATION_ET_TESTS` existent sur disque avec leur `00_NODE.md`, leur rôle, leur miroir et leur inventaire local.
- Elles ne sont pas comptées dans `node_counts` du manifest maître: `03_C` et `05_C'` y sont absentes, alors que `01_A`, `02_B`, `04_X`, `06_B'` et `07_A'` sont présentes.
- Elles sont donc déclarées comme axes dans `node_labels`, mais pas intégrées comme nœuds mesurés dans la synthèse globale.
- Le récapitulatif final ne les cite pas comme branches internes navigables, ce qui rend la lecture chiastique incomplète.
- La carte visuelle et l'index maître ne les exposent pas comme points d'entrée de premier niveau, donc elles sont présentes matériellement mais invisibles dans le graphe documentaire global.
- Le centre `04_X_NOYAU_MEMOIRE` a bien un point d'entrée local, mais il n'a pas de `README.md` racine aussi lisible que les autres branches; son point d'entrée reste uniquement le `00_NODE.md`.

## 2. Ce qui est du bruit à exclure
- Les répertoires techniques `\.git`, `\.venv`, `\.pytest_cache`, `\.uv-cache`, `__pycache__` et `logs` apparaissent dans les inventaires de certaines branches.
- Ces éléments sont utiles pour le développement ou l'exécution locale, mais ils ne devraient pas être mélangés au corpus éditorial ou de diffusion.
- Les caches et binaire compilés `*.pyc`, les environnements virtuels, les traces de logs et les fichiers temporaires polluent la lisibilité et faussent les statistiques si on les compte comme du contenu documentaire.
- Dans `05_C_PRIME_VALIDATION_ET_TESTS`, le bruit est particulièrement fort parce que l'inventaire local mélange tests, cache, environnement virtuel et artefacts de build.
- Dans `03_C_MOTEURS_ET_DEPLOIEMENT`, le bruit est plus ciblé, mais la présence d'un `.git` embarqué dans le miroir textuel est un signal clair de contamination du corpus par des métadonnées techniques.
- Ce bruit ne doit pas être supprimé sans précaution si tu t'en sers comme archive de travail, mais il faut le marquer comme non éditorial.

## 3. Ce qui est dupliqué et devrait être normalisé
- Plusieurs sources apparaissent deux fois dans `manifest_step7_master_index.json`, souvent sous une version source et une version miroir ou souveraine très proche.
- Les doublons visibles portent notamment sur `Sovereign_Unification_Phase_III_Manuscrit.tex`, `Sovereign_Millennium_Dissipative_Stability_Proof.tex`, `Sovereign_Scientific_White_Paper_v3.md`, `SOVEREIGN_MASTER_PROMPT_V3.txt`, `PHASE_IV_ACCESS_CARD.tex` et `SUBMISSION_CHECKLIST.md`.
- Des fichiers de la famille `_RELEASES/GOLDEN_MASTER_PHASE_III_SOUVERAINE` reviennent aussi en double dans le manifest, ce qui suggère une répétition volontaire mais non normalisée.
- Certaines sources canonisées existent sous plusieurs variantes d'encodage ou de nommage, ce qui crée des doublons logiques même quand les noms diffèrent légèrement.
- Exemples de normalisation utile: une seule source canonique par document, une seule version miroir textuelle, et des alias explicitement marqués pour les variantes souveraines, PDF, TEX ou MD.
- La normalisation devrait aussi harmoniser les noms avec accentuation correcte et supprimer les formes corrompues de type `—` ou des accents brisés lorsqu'elles servent à l'affichage public.

## Conclusion
- Le corpus n'est pas vide: il est dense et bien structuré.
- Le vrai manque est l'alignement entre la matière locale et la couche d'indexation globale.
- Le vrai bruit est l'empreinte des outils de travail mélangée au corpus de diffusion.
- La vraie dette de maintenance est la normalisation des doublons et des variantes de nommage.

## Priorités recommandées
- Réintégrer `03_C_MOTEURS_ET_DEPLOIEMENT` et `05_C_PRIME_VALIDATION_ET_TESTS` dans l'index maître, la carte visuelle et le récapitulatif final.
- Séparer les artefacts techniques du corpus éditorial.
- Dédupliquer les sources répétées et établir une source canonique par document.
- Harmoniser l'encodage et les noms de fichiers exposés au lecteur.
