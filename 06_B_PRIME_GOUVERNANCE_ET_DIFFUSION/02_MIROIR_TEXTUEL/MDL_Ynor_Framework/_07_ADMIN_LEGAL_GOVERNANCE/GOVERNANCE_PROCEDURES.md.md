# MIROIR TEXTUEL - GOVERNANCE_PROCEDURES.md

Source : MDL_Ynor_Framework\_07_ADMIN_LEGAL_GOVERNANCE\GOVERNANCE_PROCEDURES.md
Taille : 1432 octets
SHA256 : ad26ed4c54642644a7db907eddff9f3f7b60beb36e27e8c3a442baabaf19e6ee

```text
# 🏛️ PROCÉDURES DE GOUVERNANCE & AUDIT (MDL YNOR)
**Version :** 2.3.0-PROD | **Auteurs :** Charlier Rony

---

## 🔒 1. GOUVERNANCE DES SECRETS (VAULT-READY)
MDL Ynor a migré d'une authentification hardcodée vers une gestion par variables d'environnement (`.env`).

### 1.1 Rotation des Clés
*   **Rotation des API Keys (LLM) :** Tous les 90 jours ou en cas d'anomalie dissipative ($\mu < 0.2$ persistante).
*   **Rotation du MASTER_AUTH :** À chaque mise à jour majeure du manifeste (`mdl_global_knowledge.json`).

## ⚖️ 2. PROTOCOLE D'AUDIT EXTERNE
L'audit est géré via le script `request_audit_access.py`.

### 2.1 Critères Reviewer
*   **Audit Scientifique :** Doit fournir une preuve d'affiliation académique (CNRS, INRIA, ENS etc.).
*   **Audit Sécurité :** Doit posséder une certification (OSCP, CISSP) ou être un partenaire auditeur tier-1.

### 2.2 Accès Reviewer
L'accès est accordé via un **Activation Code** temporaire lié à l'IP du reviewer.

## 🚩 3. CONFINEMENT DU SYSTÈME (CONFINEMENT-IRL)
Les agents autonomes (`AutonomousIRLYnorAgent`) sont bridés par défaut :
*   `READ_ONLY_MODE = TRUE`
*   Toute tentative d'écriture hors sandbox est bloquée et consignée dans `mdl_audit_trail.log`.
*   Un humain doit explicitement basculer `MDL_ALLOW_WRITE=TRUE` pour autoriser une mutation structurelle.

---
*Ce document forme la base de la confiance opérationnelle du système Ynor.*

```