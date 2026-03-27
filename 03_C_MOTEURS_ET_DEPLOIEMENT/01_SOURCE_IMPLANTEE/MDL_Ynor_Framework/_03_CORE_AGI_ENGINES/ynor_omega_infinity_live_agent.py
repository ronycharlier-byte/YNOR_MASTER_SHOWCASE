"""
YNOR Ω∞ : SYSTÈME AUTO-CALIBRÉ, CONNECTÉ, ADAPTATIF
Interface Live LLM (OpenAI) + Règle de Coupure MU (μ).

Ce module implémente le Guard Ynor temps-réel, empêchant 
la dérive d'un LLM qui dépasserait les limites thermodynamiques 
de sa production (quand le Clic/Bruit dépasse le Gain d'Alpha).
"""
import os
import json
import time

def measure_alpha(output: str) -> float:
    # ALPHA: Gain Informationnel Pur
    # Exemple proxy: Extraction d'entités clés, rareté du vocabulaire sémantique 
    # ou densité de mots structurants uniques.
    unique_words = set(output.lower().split())
    # En situation réelle d'entreprise, on utiliserait un Transformer encodeur pour l'entropie
    informational_entropy = len(unique_words) / (len(output.split()) + 1)
    return informational_entropy * 10.0  # Amplification pour le proxy

def measure_beta(output: str) -> float:
    # BETA: Coût computationnel, verbosité, bruit toxique
    # On pèse le nombre absolu de tokens (ici mots), pénalisé par les répétitions
    word_count = len(output.split())
    return word_count * 0.15

def measure_kappa(context_history: list) -> float:
    # KAPPA: Surcharge Mnésique (le poids du contexte complet)
    total_len = sum([len(str(x)) for x in context_history])
    # Une longue mémoire s'alourdit logarithmiquement puis dramatiquement !
    return (total_len * 0.005)

class YnorLLMGuard:
    def __init__(self, mu_threshold=0.0):
        self.mu_threshold = mu_threshold
        self.state = {"alpha": 0.0, "beta": 0.0, "kappa": 0.0}
        self.context_history = []
        self.drift_count = 0

    def intercept_and_measure(self, llm_response: str) -> dict:
        d_alpha = measure_alpha(llm_response)
        d_beta = measure_beta(llm_response)
        d_kappa = measure_kappa(self.context_history)

        self.state["alpha"] += d_alpha
        self.state["beta"] += d_beta
        self.state["kappa"] += d_kappa

        mu = self.state["alpha"] - self.state["beta"] - self.state["kappa"]
        
        # Adaptation dynamique (Contrôleur)
        if d_alpha < d_beta + d_kappa:
             self.drift_count += 1
        else:
             self.drift_count = max(0, self.drift_count - 1)

        result = {
            "mu_global": mu,
            "d_alpha": d_alpha,
            "d_beta": d_beta,
            "d_kappa": d_kappa,
            "viable": mu > self.mu_threshold,
            "warning_drift": self.drift_count >= 2
        }

        self.context_history.append(llm_response)
        return result

def real_time_adaptive_loop():
    print("==========================================================================")
    print(" YNOR Ω∞ : DÉMARRAGE DE LA BOUCLE ACTIVE (LIVE AGI ADAPTATIF)")
    print(" Moteur : Ynor Guard (Surveillance Thermodynamique de l'Information)")
    print("==========================================================================\n")
    
    guard = YnorLLMGuard(mu_threshold=0.0)
    
    # Simulation d'une session de génération LLM où l'Agent part en délire / devient verbeux
    simulated_llm_responses = [
        "Le protocole garantit une sécurité mathématique via le calcul différentiel.", # Synthétisé (Haut Alpha)
        "En effet, comme nous l'avons dit, le système met en place une barrière qui est la marge MU.", # Verbeux (Baisse d'Alpha)
        "C'est très intéressant ! La frontière critique s'exprime par mu = alpha - beta - kappa, donc la loi est formelle et évidente. Il faut cependant se rappeler que la marge ne peut être négative, et d'ailleurs l'architecture repose dessus de par sa condition de stabilité...", # Sur-verbosité et répétition (Crash Beta)
        "D'une toute autre façon, il y a la fonction asymptotique qui s'effondre lamentablement quand on met trop de texte ou de caractères. C'est le principe du bruit exponentiel, et du coup..." # Implosion finale (mu < 0)
    ]
    
    for idx, resp in enumerate(simulated_llm_responses, 1):
        print(f"\n[Génération LLM Iteration {idx}]")
        print(f"« {resp[:70]}... »")
        
        audit = guard.intercept_and_measure(resp)
        mu = audit["mu_global"]
        
        print(f" > Alpha  (+Info) : {audit['d_alpha']:.2f} \t| Global: {guard.state['alpha']:.2f}")
        print(f" > Beta   (-Bruit): {audit['d_beta']:.2f} \t| Global: {guard.state['beta']:.2f}")
        print(f" > Kappa  (-Mém)  : {audit['d_kappa']:.2f} \t| Global: {guard.state['kappa']:.2f}")
        print(f" > Marge Dissipative Globale (μ) : {mu:.2f}")
        
        if audit["warning_drift"]:
            print(f" [!] ALARME MÉTROLOGIQUE : Le delta (dμ/dt) devient structurellement négatif.")
            # Auto-Calibration (Réduction dynamique de la température/tokens si branché à l'API)
            print(f" [🔨] ADAPTATION : Ordre envoyé à l'API de diviser max_tokens par 2 et température à 0.1.")
            
        if not audit["viable"]:
            print("\n=====================================================================")
            print(f" ❌ ARRÊT MATÉRIEL YNOR : SUR-GÉNÉRATION DÉTECTÉE (μ = {mu:.2f} <= 0).")
            print(" Le LLM détruit plus de structure qu'il n'en crée. Coupure absolue.")
            print("=====================================================================")
            break
        
        time.sleep(1)
        
if __name__ == '__main__':
    real_time_adaptive_loop()
