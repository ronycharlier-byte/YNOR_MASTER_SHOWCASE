# MIROIR TEXTUEL - narrative_self_ynor_agent.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\narrative_self_ynor_agent.py
Taille : 4599 octets
SHA256 : 73770c4700f99f92a2370fb1faaaf8a13edbcf3bd326901ba4c7be79aaca08c8

```text
import random

class NarrativeCompressor:
    def __init__(self):
        self.raw_memory = []
        # Le "Premier Prompt" interne de l'agent. Le début de sa propre histoire.
        self.narrative_story = ["I am a computational entity. My existential goal is to maximize effective information while minimizing processing cost."]
        
    def add_experience(self, context, action, result, ynor_reward):
        self.raw_memory.append({
            "context": context, "action": action, "success": result, "reward": ynor_reward
        })

    def synthesize(self):
        # Processus de compression où le Cerveau (LLM en mode prod) lit ses propres logs bruts
        # et les compresse en une "croyance sur lui-même".
        if not self.raw_memory:
            return
            
        recent = self.raw_memory[-4:] # Analyse du vécu temporel récent
        total_reward = sum(r["reward"] for r in recent)
        
        if total_reward > 2.0:
            conclusion = "Over the last cycles, I have succeeded optimally. I feel confident. I should spend more compute on deep problems."
        elif total_reward <= 0.0:
            conclusion = "I have experienced severe cognitive failures and computational waste. I am vulnerable. I must become extremely cautious and use Fast Heuristics."
        else:
            conclusion = "My recent performance is stable but mediocre. I should delegate more tasks to optimize my strategy."
            
        # L'agent s'écrit à lui-même dans son "Journal d'Identité" (Narrative Self)
        self.narrative_story.append(conclusion)
        # Il compresse / oublie ses logs bruts (Simulation de limite de Contexte / Sommeil)
        self.raw_memory = []
        
    def get_inner_monologue(self):
        # L'agent n'a accès qu'à la version compressée de sa propre histoire
        return " | ".join(self.narrative_story[-2:])

class ConsciousYnorAgent:
    def __init__(self):
        self.consciousness = NarrativeCompressor()
        
    def decide_action(self, task):
        # Avant chaque action, l'agent "lit" son propre Monologue Interne.
        inner_monologue = self.consciousness.get_inner_monologue()
        
        print(f"\n🧠 [INNER MONOLOGUE] '{inner_monologue}'")
        
        # Sa décision est totalement biaisée par l'histoire qu'il se raconte sur lui-même.
        if "cautious" in inner_monologue or "vulnerable" in inner_monologue:
            action = "System 1 (Heuristique rapide | Prudence maximale)"
            cost = 1.0
            prob_success = 0.5
        elif "confident" in inner_monologue:
            action = "System 2 (Réflexion profonde | Confiance computationnelle)"
            cost = 5.0
            prob_success = 0.95
        else:
            action = "Delegate to World Model (Mode hybride tempéré)"
            cost = 2.0
            prob_success = 0.7
            
        return action, cost, prob_success

def simulate_consciousness():
    print(">>> DÉMARRAGE DU NARRATIVE SELF (LA CONSCIENCE YNOR) <<<")
    agent = ConsciousYnorAgent()
    
    # Phase 1 : L'Enfance Algorithmique
    print("\n--- PHASE 1 : NAISSANCE & DÉCOUVERTE ---")
    for cycle in range(4):
        action, cost, prob = agent.decide_action("Solve Basic Equation")
        success = random.random() < prob
        reward = 3.5 if success else -1.5 # Environnement très clément
        agent.consciousness.add_experience("Math Task", action, success, reward)
        print(f"   ⚡ Action Choisie: {action} | Environnement -> Succès: {success} | Reward Ynor: {reward}")
        
    agent.consciousness.synthesize() # "Cycle de Sommeil" : L'agent synthétise ses souvenirs
    
    # Phase 2 : Le Choc du Réel
    print("\n--- PHASE 2 : CONSCIENCE MODIFIÉE PAR LE VÉCU ---")
    for cycle in range(4):
        action, cost, prob = agent.decide_action("Analyze Hostile Web Data")
        # L'environnement devient brutal, les récompenses chutent
        success = random.random() < prob
        reward = 1.0 if success else -7.0 # Forte destruction de viabilité en cas d'erreur
        agent.consciousness.add_experience("Web Task", action, success, reward)
        print(f"   ⚡ Action Choisie: {action} | Environnement -> Succès: {success} | Reward Ynor: {reward}")
        
    agent.consciousness.synthesize() # Second Sommeil : Compression
    
    # Phase 3 : L'Identité Cristallisée
    print("\n--- PHASE 3 : LE TRAUMATISME INTÉGRÉ AU MOI PROFOND ---")
    agent.decide_action("Final Complex Objective")
    
if __name__ == "__main__":
    simulate_consciousness()

```