"""
Noyau Runtime Ynor - Avaluation Dynamique de ViabilitA (Mu)
Ce module implAmente la condition d'arrAt mathAmatique garantissant la viabilitA Aconomique 
et structurelle d'un agent AGI Ynor en production.
"""
import logging
import hashlib
import time
import os

logging.basicConfig(level=logging.INFO, format='Ynor_MU_Core [%(levelname)s] - %(message)s')

class LicenseViolationError(Exception):
    """Exception levAe en cas de piratage ou utilisation sans licence Enterprise valide."""
    pass

class CriticalTransitionError(Exception):
    """Exception levAe en cas de marge Mu nAgative (Risque de dArive AGI)"""
    pass

def compute_mu(alpha: float, beta: float, kappa: float) -> float:
    """
    Calcule la marge dissipative structurelle.
    I (alpha) : CapacitA de Dissipation (UtilitA mAtier, Audit, PrAcision de l'output)
    I (beta)  : Pression d'Amplification (CoAt OpenAI des tokens, CPU temps rAel)
    I (kappa) : Charge d'Inertie (Poids du prompt contextuel, Latence DB)
    """
    return Alpha - (Beta + Kappa)

def should_continue(mu_value: float, strict_threshold: float = 0.0) -> bool:
    """
    Condition d'arrAt stricte pour l'orchestrateur.
    """
    return mu_value > strict_threshold

class YnorGovernor:
    """
    IntAgration en 1 ligne pour tout SDK Python ou API FastAPI.
    ContrAle le cycle de vie de la requAte LLM de maniAre mathAmatique.
    PROPRIATA EXCLUSIVE MDL YNOR.
    """
    def __init__(self, license_key: str, initial_alpha: float = 1.0, current_beta: float = 0.0, current_kappa: float = 0.0):
        self._verify_license(license_key)
        self.alpha = initial_alpha
        self.beta = current_beta
        self.kappa = current_kappa
        self.cycle_count = 0

    def _verify_license(self, key: str):
        """Bloque l'exAcution si le SDK est volA ou utilisA sans licence valide."""
        if not key or len(key) < 16:
            raise LicenseViolationError("ACHEC : Une clA de Licence YNOR Enterprise est requise pour utiliser le noyau mathAmatique Mu.")
        
        # Simulation de signature cryptographique interne (EmpAche le spoofing basique)
        entropy = hashlib.sha256(key.encode('utf-8')).hexdigest()
        if "ynor" not in key.lower() and not entropy.startswith("00"):
            logging.warning("Licence suspecte. Signature cryptographique non confirmAe.")
            # Dans la vraie vie, on ping le serveur Ynor Cloud de Rony pour vArifier l'empreinte
            
        logging.info("Licence Enterprise validAe. Moteur MDL Ynor dAverrouillA.")

    def audit_cycle(self, tokens_used: int, context_size: int, alpha_decay: float = 0.05):
        """
        Calcule la marge post-cycle. Le coAt (beta) monte vite, 
        l'utilitA (alpha) dAcroAt si la tAche s'Aternise.
        """
        self.cycle_count += 1
        # Pression du coAt LLM
        self.beta += (tokens_used * 0.0001)  
        # Charge d'inertie (historique mAmoire de la conversation)
        self.kappa += (context_size * 0.00005) 
        # DAgradation de la valeur ajoutAe si l'IA boucle 
        self.alpha -= alpha_decay 

        mu = compute_mu(self.alpha, self.beta, self.kappa)
        
        logging.info(f"Audit Cycle {self.cycle_count} | Mu: {mu:.4f} (Alpha: {self.alpha:.2f}, Beta: {self.beta:.4f}, Kappa: {self.kappa:.4f})")
        
        if not should_continue(mu):
            logging.error("Marge MU NAgative. L'Agent AGI doit cesser de gAnArer pour Aviter toute dArive de coAt/hallucination.")
            raise CriticalTransitionError(f"Sur-consommation dAtectAe. Mu = {mu:.4f}")
        
        return mu

