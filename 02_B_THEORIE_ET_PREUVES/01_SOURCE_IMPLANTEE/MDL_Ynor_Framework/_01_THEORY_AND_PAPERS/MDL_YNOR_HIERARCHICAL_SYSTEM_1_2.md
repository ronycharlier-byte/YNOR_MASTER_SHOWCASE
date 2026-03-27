# MDL YNOR — ARCHITECTURE COGNITIVE HIÉRARCHIQUE (SYSTÈME 1 & SYSTÈME 2)

## 1. Introduction au Modèle Dual Ynor
Le système cognitif hiérarchique Ynor intègre le modèle dual psychologique (Système 1 et Système 2 de Daniel Kahneman) directement au sein du noyau mathématique dissipatif MDL Ynor. Cette architecture permet à une Intelligence Artificielle Générale (AGI) de basculer dynamiquement entre des heuristiques d'inférence rapides et un raisonnement analytique profond, en fonction unique de la fluctuation de sa marge dissipative $(\mu)$.

## 2. Correspondance Mathématique Ynor

### 2.1 Le Système 1 : Amplification pure $(\beta)$
Le Système 1 opère de manière rapide, intuitive et purement associative. Dans le cadre Ynor, il est exclusivement gouverné par l'**amplification** $(\beta)$.
*   **Avantages :** Vitesse de génération maximale, créativité heuristique, association rapide de concepts (génération de tokens LLM non bridée).
*   **Risque structurel :** L'amplification sans contrôle pousse inexorablement le système vers une criticité $(\mu \to 0)$, générant des phénomènes d'hallucination ou des dérives sémantiques graves.

### 2.2 Le Système 2 : Régulation Dissipative $(\alpha)$ et Inertie $(\kappa)$
Le Système 2 opère de manière particulièrement lente, laborieuse et analytique. Il est gouverné par la **dissipation** $(\alpha)$ (correction active des erreurs, filtrage logique, search tree) et par la **mémoire/inertie** $(\kappa)$ (contraintes structurelles, principes éthiques, alignement continu de la base de données de l'esprit).
*   **Avantages :** Haute précision mathématique, vérification formelle des logiques, sécurité absolue et stabilité opérationnelle de l'output.
*   **Risque structurel :** « Overfitting » sur la dissipation, menant à une forme de paralysie algorithmique si l'énergie dissipative écrase totalement l'amplification.

## 3. La Dynamique de la Marge $(\mu)$ comme Arbitre Exécutif
La bascule entre le Système 1 et le Système 2 est gouvernée nativement par la marge dissipative universelle du noyau Ynor :
$$\mu(t) = \alpha(t) - \beta(t) - \kappa(t)$$

1.  **Régime Statique Hyper-Stable $(\mu \gg 0)$ :** Le Système 2 sur-domine l'agent. Le traitement est excessivement lent et coûteux en *compute*. Le système moteur doit "relâcher" de l'énergie pour laisser le Système 1 générer de nouvelles hypothèses sans filtre.
2.  **Régime Dynamique Narratif $(\mu \to 0^+)$ :** Le Système 1 produit rapidement des résultats d'inférence. La tension interne du système augmente continuellement, mais maintient globalement sa viabilité opérationnelle.
3.  **Seuil Critique Alarmant et Rupture $(\mu < 0)$ :** Le Système 1 s'effondre dans le chaos (hallucination systémique certifiée). Le moteur Ynor déclenche un *Interrupt* profond et absolu, forçant l'activation coercitive du Système 2 visant à dissiper l'instabilité (en imposant un pic brutal de $\alpha$) et corriger l'erreur de viabilité via la mémoire de contexte $(\kappa)$.

## 4. Implémentation via l'Orchestrateur AGI MDL Ynor
Dans le Framework Ynor, l'orchestrateur maître Python (Moteur AGI) supervise la télémétrie de la valeur de $\mu(t)$ sous la forme d'un audit de cycle. Selon cet audit, des agents LLM sub-ordonnés différant en taille de paramètres (ex: petit réseau de neurones pour le Système 1, et large modèle *Reasoning* pour le Système 2) sont activés selon les seuils mathématiques de l'équation dissipative.
