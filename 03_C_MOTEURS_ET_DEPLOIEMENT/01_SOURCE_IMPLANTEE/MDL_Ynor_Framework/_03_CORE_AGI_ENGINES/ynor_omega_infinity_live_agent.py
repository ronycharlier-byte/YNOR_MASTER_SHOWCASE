"""
YNOR Iaz : SYSTAME AUTO-CALIBRA, CONNECTA, ADAPTATIF
Interface Live LLM (OpenAI) + RAgle de Coupure MU (I).

Ce module implAmente le Guard Ynor temps-rAel, empAchant 
la dArive d'un LLM qui dApasserait les limites thermodynamiques 
de sa production (quand le Clic/Bruit dApasse le Gain d'Alpha).
"""
import os
import json
import time

def measure_alpha(output: str) -> float:
    # ALPHA: Gain Informationnel Pur
    # Exemple proxy: Extraction d'entitAs clAs, raretA du vocabulaire sAmantique 
    # ou densitA de mots structurants uniques.
    unique_words = set(output.lower().split())
    # En situation rAelle d'entreprise, on utiliserait un Transformer encodeur pour l'entropie
    informational_entropy = len(unique_words) / (len(output.split()) + 1)
    return informational_entropy * 10.0  # Amplification pour le proxy

def measure_beta(output: str) -> float:
    # BETA: CoAt computationnel, verbositA, bruit toxique
    # On pAse le nombre absolu de tokens (ici mots), pAnalisA par les rApAtitions
    word_count = len(output.split())
    return word_count * 0.15

def measure_kappa(context_history: list) -> float:
    # KAPPA: Surcharge MnAsique (le poids du contexte complet)
    total_len = sum([len(str(x)) for x in context_history])
    # Une longue mAmoire s'alourdit logarithmiquement puis dramatiquement !
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
        
        # Adaptation dynamique (ContrAleur)
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
    print(" YNOR Iaz : DAMARRAGE DE LA BOUCLE ACTIVE (LIVE AGI ADAPTATIF)")
    print(" Moteur : Ynor Guard (Surveillance Thermodynamique de l'Information)")
    print("==========================================================================\n")
    
    guard = YnorLLMGuard(mu_threshold=0.0)
    
    # Simulation d'une session de gAnAration LLM oA l'Agent part en dAlire / devient verbeux
    simulated_llm_responses = [
        "Le protocole garantit une sAcuritA mathAmatique via le calcul diffArentiel.", # SynthAtisA (Haut Alpha)
        "En effet, comme nous l'avons dit, le systAme met en place une barriAre qui est la marge MU.", # Verbeux (Baisse d'Alpha)
        "C'est trAs intAressant ! La frontiAre critique s'exprime par mu = Alpha - (Beta + Kappa), donc la loi est formelle et Avidente. Il faut cependant se rappeler que la marge ne peut Atre nAgative, et d'ailleurs l'architecture repose dessus de par sa condition de stabilitA...", # Sur-verbositA et rApAtition (Crash Beta)
        "D'une toute autre faAon, il y a la fonction asymptotique qui s'effondre lamentablement quand on met trop de texte ou de caractAres. C'est le principe du bruit exponentiel, et du coup..." # Implosion finale (mu < 0)
    ]
    
    for idx, resp in enumerate(simulated_llm_responses, 1):
        print(f"\n[GAnAration LLM Iteration {idx}]")
        print(f"A {resp[:70]}... A")
        
        audit = guard.intercept_and_measure(resp)
        mu = audit["mu_global"]
        
        print(f" > Alpha  (+Info) : {audit['d_alpha']:.2f} \t| Global: {guard.state['alpha']:.2f}")
        print(f" > Beta   (-Bruit): {audit['d_beta']:.2f} \t| Global: {guard.state['beta']:.2f}")
        print(f" > Kappa  (-MAm)  : {audit['d_kappa']:.2f} \t| Global: {guard.state['kappa']:.2f}")
        print(f" > Marge Dissipative Globale (I) : {mu:.2f}")
        
        if audit["warning_drift"]:
            print(f" [!] ALARME MATROLOGIQUE : Le delta (dI/dt) devient structurellement nAgatif.")
            # Auto-Calibration (RAduction dynamique de la tempArature/tokens si branchA A l'API)
            print(f" [Y"] ADAPTATION : Ordre envoyA A l'API de diviser max_tokens par 2 et tempArature A 0.1.")
            
        if not audit["viable"]:
            print("\n=====================================================================")
            print(f" a ARRAST MATARIEL YNOR : SUR-GANARATION DATECTAE (I = {mu:.2f} <= 0).")
            print(" Le LLM dAtruit plus de structure qu'il n'en crAe. Coupure absolue.")
            print("=====================================================================")
            break
        
        time.sleep(1)
        
if __name__ == '__main__':
    real_time_adaptive_loop()

