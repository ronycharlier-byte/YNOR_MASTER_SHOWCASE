---
STATUS: CANONICAL | V11.13.0 | AUDIT: CERTIFIED | FINAL CONSOLIDATED REVIEW / V11.13.0
---

# GUIDE OPERATIONNEL DES MOTEURS YNOR

## Objet
Ce document decrit les procedures minimales pour demarrer, verifier et maintenir les moteurs YNOR dans un cadre de test reproductible.

## 1. Demarrage du service
1. Ouvrir le repertoire racine du framework.
2. Lancer `YNOR_SERVER_MANAGER.bat`.
3. Choisir l'option de demarrage standard pour initialiser l'API, les services locaux et les verifications de base.

## 2. Exposition de l'interface de test
1. Utiliser l'option de publication locale quand une adresse HTTPS temporaire est requise.
2. Copier l'URL de session fournie par le service.
3. Mettre a jour les parametres du schema d'action seulement si le point d'entree a change.

## 3. Protocoles de demonstration
1. Executer les scripts de demonstration depuis le sous-repertoire de test approprie.
2. Noter les entrees, les sorties et les conditions d'arret.
3. Conserver les resultats de console et les journaux generes pendant l'execution.

## 4. Regles de validation
- Verifier l'encodage UTF-8 sans BOM avant toute publication.
- Confirmer que les chemins de fichiers cites correspondent aux artefacts reels.
- Reproduire chaque execution avec les memes parametres avant diffusion.

## 5. Sortie attendue
Un moteur documente de cette maniere peut etre relu, execute et audite sans reference commerciale ni terminologie promotionnelle.
