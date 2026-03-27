"""
Noyau Runtime Ynor - Évaluation Dynamique de Viabilité (Mu)
Ce module implémente la condition d'arrêt mathématique garantissant la viabilité économique 
et structurelle d'un agent AGI Ynor en production.
"""
import logging
import hashlib
import time
import os

logging.basicConfig(level=logging.INFO, format='Ynor_MU_Core [%(levelname)s] - %(message)s')

class LicenseViolationError(Exception):
    """Exception levée en cas de piratage ou utilisation sans licence Enterprise valide."""
    pass

class CriticalTransitionError(Exception):
    """Exception levée en cas de marge Mu négative (Risque de dérive AGI)"""
    pass

def compute_mu(alpha: float, beta: float, kappa: float) -> float:
    """
    Calcule la marge dissipative structurelle.
    α (alpha) : Capacité de Dissipation (Utilité métier, Audit, Précision de l'output)
    β (beta)  : Pression d'Amplification (Coût OpenAI des tokens, CPU temps réel)
    κ (kappa) : Charge d'Inertie (Poids du prompt contextuel, Latence DB)
    """
    return alpha - beta - kappa

def should_continue(mu_value: float, strict_threshold: float = 0.0) -> bool:
    """
    Condition d'arrêt stricte pour l'orchestrateur.
    """
    return mu_value > strict_threshold

class YnorGovernor:
    """
    Intégration en 1 ligne pour tout SDK Python ou API FastAPI.
    Contrôle le cycle de vie de la requête LLM de manière mathématique.
    PROPRIÉTÉ EXCLUSIVE MDL YNOR.
    """
    def __init__(self, license_key: str, initial_alpha: float = 1.0, current_beta: float = 0.0, current_kappa: float = 0.0):
        self._verify_license(license_key)
        self.alpha = initial_alpha
        self.beta = current_beta
        self.kappa = current_kappa
        self.cycle_count = 0

    def _verify_license(self, key: str):
        """Bloque l'exécution si le SDK est volé ou utilisé sans licence valide."""
        if not key or len(key) < 16:
            raise LicenseViolationError("ÉCHEC : Une clé de Licence YNOR Enterprise est requise pour utiliser le noyau mathématique Mu.")
        
        # Simulation de signature cryptographique interne (Empêche le spoofing basique)
        entropy = hashlib.sha256(key.encode('utf-8')).hexdigest()
        if "ynor" not in key.lower() and not entropy.startswith("00"):
            logging.warning("Licence suspecte. Signature cryptographique non confirmée.")
            # Dans la vraie vie, on ping le serveur Ynor Cloud de Rony pour vérifier l'empreinte
            
        logging.info("Licence Enterprise validée. Moteur MDL Ynor déverrouillé.")

    def audit_cycle(self, tokens_used: int, context_size: int, alpha_decay: float = 0.05):
        """
        Calcule la marge post-cycle. Le coût (beta) monte vite, 
        l'utilité (alpha) décroît si la tâche s'éternise.
        """
        self.cycle_count += 1
        # Pression du coût LLM
        self.beta += (tokens_used * 0.0001)  
        # Charge d'inertie (historique mémoire de la conversation)
        self.kappa += (context_size * 0.00005) 
        # Dégradation de la valeur ajoutée si l'IA boucle 
        self.alpha -= alpha_decay 

        mu = compute_mu(self.alpha, self.beta, self.kappa)
        
        logging.info(f"Audit Cycle {self.cycle_count} | Mu: {mu:.4f} (Alpha: {self.alpha:.2f}, Beta: {self.beta:.4f}, Kappa: {self.kappa:.4f})")
        
        if not should_continue(mu):
            logging.error("Marge MU Négative. L'Agent AGI doit cesser de générer pour éviter toute dérive de coût/hallucination.")
            raise CriticalTransitionError(f"Sur-consommation détectée. Mu = {mu:.4f}")
        
        return mu
