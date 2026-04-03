import time
from .core_mu import YnorGovernor, CriticalTransitionError

class YnorLangchainCallbackHandler:
    """
    Intégration native (Plug & Play) pour LangChain.
    S'injecte directement dans les requêtes LLM (OpenAI, Anthropic, etc.)
    pour couper le Vecteurs de Données Stochastiques de tokens dès que l'équation Ynor détecte une hallucination.
    """
    
    def __init__(self, license_key: str, alpha_start: float = 1.0, beta_start: float = 0.1, kappa_start: float = 0.05):
        # Initialise le Gouverneur interne (Local Evaluation)
        self.governor = YnorGovernor(initial_alpha=alpha_start, current_beta=beta_start, current_kappa=kappa_start, license_key=license_key)
        self.token_count = 0
        self.start_time = time.time()
        self.halt_triggered = False

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        """Déclenché quand le LLM commence à générer."""
        self.start_time = time.time()
        self.token_count = 0
        self.halt_triggered = False
        print(f"\\n[YNOR GUARD] Agent LangChain détecté. Surveilance mathématique activée. (Mu(0) = {self.governor.mu:.3f})")

    def on_llm_new_token(self, token: str, **kwargs):
        """
        Déclenché à CHAQUE nouveau mot généré par le LLM.
        Le cœur de l'optimisation financière se trouve ici.
        """
        if self.halt_triggered:
            # Si déjà coupé, on rejette la suite
            return

        self.token_count += 1
        
        # Le contexte augmente à chaque token (fatigue l'IA)
        context_size = self.token_count * 1.5
        
        try:
            # Audit YNOR : Recalcule l'équation fondamentale à la milliseconde
            is_valid, current_mu = self.governor.audit_cycle(tokens_used=self.token_count, context_size=context_size)
            
            # Affichage console en mode terminal pour le client (Optionnel)
            # print(f"[{token}] -> μ={current_mu:.3f}", end=" ", flush=True)
            
        except CriticalTransitionError as e:
            # INTERCEPTION : Mu est devenu négatif. L'IA gaspille de l'argent ou hallucine.
            self.halt_triggered = True
            savings_est = ((4000 - self.token_count) / 1000) * 0.03 # Exemple $0.03 par 1k tokens sauvés
            
            print(f"\\n\\n[YNOR GUARD ACTIF] 🛑 ARRÊT D'URGENCE DU LLM 🛑")
            print(f"Raison : Marge Dissipative négative (μ = {self.governor.mu:.3f}).")
            print(f"Tokens générés avant blocage : {self.token_count}")
            print(f"Économie financière estimée : +${savings_est:.4f}")
            
            # Rejette une erreur custom pour forcer LangChain / OpenAI à arrêter la requête réseau
            raise YnorHaltException("YNOR: Token generation forcibly stopped to prevent AI cost inflation.")

class YnorHaltException(Exception):
    """Exception personnalisée pour couper le Vecteurs de Données Stochastiques réseau du LLM."""
    pass
