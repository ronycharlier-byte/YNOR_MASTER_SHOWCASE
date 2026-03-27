import random

# =========================
# 🧬 MOTEUR D'EVOLUTION CULTURELLE YNOR
# =========================
GAMMA_COOP = 2.0
DELTA_CONFLICT = 1.5

class Norm:
    def __init__(self, action, condition, origin="Genesis"):
        self.action = action          # e.g., "Dev-Alpha"
        self.condition = condition    # e.g., "simple_task"
        self.score = 5.0              # Survival fitness
        self.origin = origin          # Track lineage
        self.usage_count = 0
        
    def __repr__(self):
        return f"[Norm | {self.origin}] If {self.condition} -> Use {self.action} (Score: {self.score:.2f})"

class CulturalMemory:
    def __init__(self):
        self.norms = [
            Norm("Dev-Alpha", "simple_task"),
            Norm("Dev-Beta", "critical_task"),
            Norm("Dev-Beta", "simple_task"), # Competing norm
            Norm("Dev-Alpha", "critical_task") # Competing norm
        ]
        
    def get_best_norm(self, context):
        # Le "marché des idées" : sélectionne la norme la plus forte pour le contexte
        applicable_norms = [n for n in self.norms if n.condition == context]
        if not applicable_norms:
            return None
        return max(applicable_norms, key=lambda x: x.score)

    def mutate(self):
        # Mutation culturelle stochastique
        if random.random() < 0.15 and self.norms:
            parent = random.choice(self.norms)
            new_action = "Dev-Alpha" if parent.action == "Dev-Beta" else "Dev-Beta"
            new_norm = Norm(new_action, parent.condition, origin=f"Mutated from {parent.action}")
            new_norm.score = parent.score * 0.8 # Inheritance penalty
            self.norms.append(new_norm)
            print(f"  🧬 [CULTURAL MUTATION] Nouvelle norme apparue -> {new_norm.action} for {new_norm.condition}")

    def cull_dead_norms(self):
        # Mort par sélection naturelle culturelle
        dead = [n for n in self.norms if n.score <= 0.0]
        for d in dead:
            print(f"  💀 [CULTURAL DEATH] La norme '{d.action} for {d.condition}' a été éliminée par la matrice de survie (Score <= 0).")
        self.norms = [n for n in self.norms if n.score > 0.0]

class EvolutionaryAgent:
    def __init__(self, name, base_cost, error_rate):
        self.name = name
        self.base_cost = base_cost
        self.base_error = error_rate

    def perform_task(self, task_difficulty):
        fatigue = random.uniform(0.8, 1.2)
        real_cost = self.base_cost * fatigue
        difficulty_multiplier = 1.0 if task_difficulty == "simple_task" else 5.0
        real_error = self.base_error * fatigue * difficulty_multiplier
        return real_error, real_cost

class EvolutionaryCultureSimulator:
    def __init__(self):
        self.coders = {
            "Dev-Alpha": EvolutionaryAgent("Dev-Alpha", base_cost=1.0, error_rate=0.4),
            "Dev-Beta": EvolutionaryAgent("Dev-Beta", base_cost=10.0, error_rate=0.05)
        }
        self.memory = CulturalMemory()

    def run_epoch(self, cycles=50):
        print(">>> DEMARRAGE DU MOTEUR D'ÉVOLUTION CULTURELLE YNOR <<<")
        
        for cycle in range(1, cycles + 1):
            task_context = "simple_task" if cycle % 2 != 0 else "critical_task"
            
            # 1. Sélection culturelle (Darwinisme)
            applied_norm = self.memory.get_best_norm(task_context)
            if not applied_norm:
                continue # Culture effondrée sur ce contexte
                
            applied_norm.usage_count += 1
            chosen_coder = self.coders[applied_norm.action]
            
            # 2. Exécution du Dev
            err_coder, cost_coder = chosen_coder.perform_task(task_context)
            
            # 3. Ynor Evaluation & Norm Score Update
            if task_context == "simple_task":
                if cost_coder > 5.0:
                    applied_norm.score -= DELTA_CONFLICT
                else:
                    applied_norm.score += GAMMA_COOP
            elif task_context == "critical_task":
                if err_coder > 1.5:
                    applied_norm.score -= DELTA_CONFLICT
                else:
                    applied_norm.score += GAMMA_COOP

            # 4. Mutations & Culling
            self.memory.mutate()
            self.memory.cull_dead_norms()

        print("\n=== ÉTAT FINAL DE LA CULTURE ÉMERGENTE (SURVIVANTS) ===")
        for norm in sorted(self.memory.norms, key=lambda n: n.score, reverse=True):
            print(norm)

if __name__ == "__main__":
    sim = EvolutionaryCultureSimulator()
    sim.run_epoch(cycles=50)
