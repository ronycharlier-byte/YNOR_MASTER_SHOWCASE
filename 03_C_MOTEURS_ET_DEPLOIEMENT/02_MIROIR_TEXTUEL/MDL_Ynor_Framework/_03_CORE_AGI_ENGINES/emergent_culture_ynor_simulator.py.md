# MIROIR TEXTUEL - emergent_culture_ynor_simulator.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\emergent_culture_ynor_simulator.py
Taille : 5128 octets
SHA256 : 49dcad8e8e7e37f1f778714fa9caa25471937e2ec402efb5d81d5f9d240e6ca6

```text
import random

# =========================
#  CULTURE EMERGENTE YNOR (VRAIE CULTURE CONTEXTUELLE)
# =========================
GAMMA_COOP = 2.0
DELTA_CONFLICT = 1.5

class CollectiveMemory:
    def __init__(self):
        self.protocols = {}
        
    def update_norm(self, context, best_agent_name):
        self.protocols[context] = f"Use {best_agent_name} for {context}"

class CulturalAgent:
    def __init__(self, name, role, base_cost, error_rate):
        self.name = name
        self.role = role
        self.base_cost = base_cost
        self.base_error = error_rate
        # Matrice de Reputation CONTEXTUELLE
        self.reputation_matrix = {
            "simple_task": {},
            "critical_task": {}
        }

    def init_reputation(self, peer_names):
        for peer in peer_names:
            self.reputation_matrix["simple_task"][peer] = 5.0
            self.reputation_matrix["critical_task"][peer] = 5.0
            
    def perform_task(self, task_difficulty):
        fatigue = random.uniform(0.8, 1.2)
        real_cost = self.base_cost * fatigue
        
        # Multiplicateur d'erreur si la tache est critique
        difficulty_multiplier = 1.0 if task_difficulty == "simple_task" else 5.0
        real_error = self.base_error * fatigue * difficulty_multiplier
        
        i_eff = 1.0 / (real_error + 0.1)
        # Penalite de Cout stricte sur les petites taches, indulgente sur les lourdes
        beta = 1.0 if task_difficulty == "simple_task" else 0.1
        mu_self = i_eff - real_error - (beta * real_cost)
        
        return mu_self, real_error, real_cost

class CultureSimulator:
    def __init__(self):
        self.agents = [
            CulturalAgent("Architect", "planner", base_cost=5.0, error_rate=0.5),
            CulturalAgent("Dev-Alpha", "coder", base_cost=1.0, error_rate=0.4),  # Tres rentable mais brouillon
            CulturalAgent("Dev-Beta", "coder", base_cost=10.0, error_rate=0.05), # Parfait mais hors de prix
            CulturalAgent("Critic", "reviewer", base_cost=1.0, error_rate=0.1)
        ]
        
        agent_names = [a.name for a in self.agents]
        for a in self.agents:
            a.init_reputation(agent_names)
            
        self.collective_memory = CollectiveMemory()

    def run_society(self, cycles=40):
        print(">>> DEMARRAGE DU SIMULATEUR DE VRAIE CULTURE YNOR <<<")
        architect = self.agents[0]
        coders = [a for a in self.agents if a.role == "coder"]
        
        for cycle in range(1, cycles + 1):
            # L'environnement alterne les contextes
            task_context = "simple_task" if cycle % 2 != 0 else "critical_task"
            print(f"\n--- CYCLE {cycle} | Contexte : {task_context.upper()} ---")
            
            # 1. Selection par l'Architecte (selon le contexte)
            chosen_coder = max(coders, key=lambda c: architect.reputation_matrix[task_context][c.name])
            print(f" Architect Delegue a [{chosen_coder.name}] (Trust: {architect.reputation_matrix[task_context][chosen_coder.name]:.2f})")
            
            # 2. Execution du Dev
            mu_coder, err_coder, cost_coder = chosen_coder.perform_task(task_context)
            
            # 3. Ynor Evaluation Culturelle (Critic)
            mu_collectif = mu_coder
            
            if task_context == "simple_task":
                if cost_coder > 5.0:
                    print(f" Critic sanctionne {chosen_coder.name} (Gaspillage Ynor : Cost={cost_coder:.2f})")
                    mu_collectif -= DELTA_CONFLICT
                    architect.reputation_matrix[task_context][chosen_coder.name] -= 1.5
                else:
                    print(f" Critic valide {chosen_coder.name} (Tache economique reussie)")
                    mu_collectif += GAMMA_COOP
                    architect.reputation_matrix[task_context][chosen_coder.name] += 1.0
                    
            elif task_context == "critical_task":
                if err_coder > 1.5:
                    print(f" Critic sanctionne {chosen_coder.name} (Divergence fatale : Error={err_coder:.2f})")
                    mu_collectif -= DELTA_CONFLICT
                    architect.reputation_matrix[task_context][chosen_coder.name] -= 2.0
                else:
                    print(f" Critic valide {chosen_coder.name} (Precision critique assuree)")
                    mu_collectif += GAMMA_COOP
                    architect.reputation_matrix[task_context][chosen_coder.name] += 1.0

            # 4. Encrage dans la Memoire Collective
            current_best = max(coders, key=lambda c: architect.reputation_matrix[task_context][c.name])
            self.collective_memory.update_norm(task_context, current_best.name)

        print("\n=== ETAT FINAL DE LA CULTURE EMERGENTE ===")
        print(" MEMOIRE COLLECTIVE COMPORTEMENTALE (Tradition) :")
        for context, rule in self.collective_memory.protocols.items():
            print(f" - {rule}")

if __name__ == "__main__":
    sim = CultureSimulator()
    sim.run_society(cycles=40)

```