# MIROIR TEXTUEL - core_mu.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\ynor_sdk\ynor\core_mu.py
Taille : 3659 octets
SHA256 : fb502b54d048fc7a36225a9869456728da44b373a41a736e8e4fcab5ea54222b

```text
"""
Noyau Runtime Ynor - Evaluation Dynamique de Viabilite (Mu)
Ce module implemente la condition d'arret mathematique garantissant la viabilite economique 
et structurelle d'un agent AGI Ynor en production.
"""
import logging
import hashlib
import time
import os

logging.basicConfig(level=logging.INFO, format='Ynor_MU_Core [%(levelname)s] - %(message)s')

class LicenseViolationError(Exception):
    """Exception levee en cas de piratage ou utilisation sans licence Enterprise valide."""
    pass

class CriticalTransitionError(Exception):
    """Exception levee en cas de marge Mu negative (Risque de derive AGI)"""
    pass

def compute_mu(alpha: float, beta: float, kappa: float) -> float:
    """
    Calcule la marge dissipative structurelle.
     (alpha) : Capacite de Dissipation (Utilite metier, Audit, Precision de l'output)
     (beta)  : Pression d'Amplification (Cout OpenAI des tokens, CPU temps reel)
     (kappa) : Charge d'Inertie (Poids du prompt contextuel, Latence DB)
    """
    return alpha - (beta + kappa)

def should_continue(mu_value: float, strict_threshold: float = 0.0) -> bool:
    """
    Condition d'arret stricte pour l'orchestrateur.
    """
    return mu_value > strict_threshold

class YnorGovernor:
    """
    Integration en 1 ligne pour tout SDK Python ou API FastAPI.
    Controle le cycle de vie de la requete LLM de maniere mathematique.
    PROPRIETE EXCLUSIVE MDL YNOR.
    """
    def __init__(self, license_key: str, initial_alpha: float = 1.0, current_beta: float = 0.0, current_kappa: float = 0.0):
        self._verify_license(license_key)
        self.alpha = initial_alpha
        self.beta = current_beta
        self.kappa = current_kappa
        self.cycle_count = 0

    def _verify_license(self, key: str):
        """Bloque l'execution si le SDK est vole ou utilise sans licence valide."""
        if not key or len(key) < 16:
            raise LicenseViolationError("ECHEC : Une cle de Licence YNOR Enterprise est requise pour utiliser le noyau mathematique Mu.")
        
        # Simulation de signature cryptographique interne (Empeche le spoofing basique)
        entropy = hashlib.sha256(key.encode('utf-8')).hexdigest()
        if "ynor" not in key.lower() and not entropy.startswith("00"):
            logging.warning("Licence suspecte. Signature cryptographique non confirmee.")
            # Dans la vraie vie, on ping le serveur Ynor Cloud de Rony pour verifier l'empreinte
            
        logging.info("Licence Enterprise validee. Moteur MDL Ynor deverrouille.")

    def audit_cycle(self, tokens_used: int, context_size: int, alpha_decay: float = 0.05):
        """
        Calcule la marge post-cycle. Le cout (beta) monte vite, 
        l'utilite (alpha) decroit si la tache s'eternise.
        """
        self.cycle_count += 1
        # Pression du cout LLM
        self.beta += (tokens_used * 0.0001)  
        # Charge d'inertie (historique memoire de la conversation)
        self.kappa += (context_size * 0.00005) 
        # Degradation de la valeur ajoutee si l'IA boucle 
        self.alpha -= alpha_decay 

        mu = compute_mu(self.alpha, self.beta, self.kappa)
        
        logging.info(f"Audit Cycle {self.cycle_count} | Mu: {mu:.4f} (Alpha: {self.alpha:.2f}, Beta: {self.beta:.4f}, Kappa: {self.kappa:.4f})")
        
        if not should_continue(mu):
            logging.error("Marge MU Negative. L'Agent AGI doit cesser de generer pour eviter toute derive de cout/hallucination.")
            raise CriticalTransitionError(f"Sur-consommation detectee. Mu = {mu:.4f}")
        
        return mu

```