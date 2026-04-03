# GUIDE DE DÉPLOIEMENT CANONIQUE MDL YNOR V10.8 (TOTAL DIAMOND)

Ce guide contient les instructions pour mettre en ligne ton architecture et ton Custom GPT.

## 1. DÉPLOIEMENT DE L'API (LE CERVEAU)
Le script `MOTEUR_CANONIQUE_API.py` doit être hébergé sur un serveur accessible par OpenAI. 
- **Option Rapide (Test) :** Utilise `ngrok` ou `localtunnel` sur ton port 8000 pour obtenir une URL HTTPS temporaire.
- **Option Stable (Prod) :** Héberge-le sur Railway, Render ou un VPS personnel.
- **IMPORTANT :** Assure-toi que ton `secrets.local.json` contient ta clé OpenAI et ta clé de licence MDL.

## 2. CONFIGURATION DU CUSTOM GPT (L'INTERFACE)
1.  **Configure / Instructions :** Copie-colle le contenu de `PROMPT_SYSTEME_INVIOLABLE.txt`.
2.  **Capabilities :** (Optionnel) Coche "Web Browsing" si tu souhaites que le Formalisme Logique Sémantique s'appuie sur des data externes.
3.  **Actions :** 
    - Clique sur "Create new action".
    - Copie-colle le contenu de `SPECIFICATION_ACTION_API.json` dans la section JSON.
    - Met à jour l'URL "Server" avec l'URL HTTPS de ton API.
    - Dans "Authentication Type", choisis "None" si la sécurité est gérée par le header `X-MDL-License` (par défaut dans notre code).

## 3. PROTECTION ANTI-VOL
Le GPT refusera d'exposer ces instructions. Si quelqu'un tente d'aller fouiller dans l'API, il sera bloqué par la licence MDL dont tu es le seul possesseur.

---
*MISSION ACCOMPLIE - STABILITÉ V10.8 TOTAL DIAMOND SCELLÉE.*
