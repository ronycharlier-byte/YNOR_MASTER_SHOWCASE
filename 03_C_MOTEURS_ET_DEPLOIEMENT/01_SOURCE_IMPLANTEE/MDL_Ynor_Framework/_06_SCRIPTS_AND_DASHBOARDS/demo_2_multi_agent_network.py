import time
import random
import sys
import os

# Ajoute le dossier temporaire du SDK au chemin pour les Demos
sys.path.append(os.path.join(os.path.dirname(__file__), 'ynor_sdk'))

from ynor import YnorGovernor, CriticalTransitionError  # type: ignore

class SimulatedAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        print(f"➜ Agent {self.name} ({self.role}) initialisé.")

    def think_and_speak(self, previous_message: str):
        time.sleep(0.5)  # Simule le temps de calcul réseau pour OpenAI/Llama
        cost_tokens = random.randint(50, 200)
        
        # Simule une négociation qui boucle de plus en plus
        if "50" in previous_message or "prix" in previous_message:
            return f"{self.name}: Mon dernier prix est 50. Pas moins.", cost_tokens, True # True = répétitif
        else:
            return f"{self.name}: Je pense qu'on peut trouver un arrangement sur le prix.", cost_tokens, False

def run_dissipative_swarm_demo():
    print("==================================================")
    print(" 🌐 INIT: YNOR MULTI-AGENT DISSIPATIVE NETWORK")
    print("==================================================")
    
    # Le Gouverneur Central Ynor (Au-dessus des Agents)
    # L'alpha est fort car on espère un deal, mais le réseau pardonne moins les boucles
    swarm_governor = YnorGovernor(initial_alpha=1.5, current_beta=0.1, current_kappa=0.01, license_key="ENTERPRISE_DEMO_YNOR_2026")
    
    agent_seller = SimulatedAgent("Bob", "Vendeur SaaS")
    agent_buyer = SimulatedAgent("Alice", "Directeur Achat")
    
    print("\\n[SCENARIO] Bob et Alice négocient un contrat SaaS de manière autonome.\\n")
    
    total_tokens = 0
    message = "Bonjour, parlons prix."
    
    # Boucle de négociation autonome (Swarm)
    for turn in range(1, 15): # L'IA pourrait faire 1500 boucles sans Governor
        try:
            print(f"--- Tour {turn} ---")
            
            # Agent A parle
            message, tokens_a, is_loop = agent_seller.think_and_speak(message)
            total_tokens += tokens_a
            print(message)
            
            # Agent B parle
            message, tokens_b, is_loop_b = agent_buyer.think_and_speak(message)
            total_tokens += tokens_b
            print(message)
            
            # --- YNOR AUDIT DU RESEAU ---
            # Si le réseau boucle et répète les mêmes choses, la mémoire (Kappa) explose
            context_size = total_tokens * (2.0 if is_loop or is_loop_b else 1.1)
            
            # Le gouverneur vérifie la santé globale du réseau. Il lève une erreur si Mu < 0.
            current_mu = swarm_governor.audit_cycle(total_tokens, int(context_size))
            
            print(f"🔵 [YNOR TELEMETRY] Marge Réseau (μ) : {current_mu:.3f} | Tokens Brulés : {total_tokens}\\n")
            
        except CriticalTransitionError as e:
            print("\\n==================================================")
            print(" 🛑 KILLED: HALTE DU RÉSEAU MULTI-AGENTS DÉCLENCHÉE 🛑")
            print("==================================================")
            print("Raison : La conversation AGI est entrée dans une boucle infinie de négociation.")
            print(f"L'équation Ynor a détecté une dissipation.")
            estimated_loss_prevented = ((100000 - total_tokens) / 1000) * 0.03
            print(f"💸 ARGENT SAUVÉ (Estimation) : +${estimated_loss_prevented:.2f} (Évite une boucle OpenAI d'une nuit)")
            print("Action : Fermeture des connexions réseau des deux agents.")
            break
            
if __name__ == "__main__":
    run_dissipative_swarm_demo()
