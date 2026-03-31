import torch
import torch.nn as nn
import random

# =========================
#  SECURITE MINIMALE
# =========================
GLOBAL_COST_LIMIT = 1000.0  # Budget total de la civilisation

# =========================
#  DUMMY YNOR COMPONENT
# =========================
class YnorEstimator:
    def __init__(self, alpha=1.0, beta=0.1):
        self.alpha = alpha
        self.beta = beta
    def compute(self, error, cost):
        # proxy function
        i_eff = 1.0 / (error + 1e-6)
        mu = i_eff - self.alpha * error - self.beta * cost
        return mu

# =========================
#  AGENT WRAPPER (SPECIALIZED)
# =========================
class SpecializedYnorAgent:
    def __init__(self, agent_id, role, cost_multiplier, error_profile):
        self.id = agent_id
        self.role = role
        self.cost_multiplier = cost_multiplier
        self.error_profile = error_profile  # Expected error for specific task types
        self.estimator = YnorEstimator()

    def estimate_viability(self, task_type):
        # L'agent estime sa propre viabilite pour une tache precise
        # Si la tache n'est pas dans son profil, l'erreur attendue est enorme (5.0)
        expected_error = self.error_profile.get(task_type, 5.0) 
        expected_cost = 10.0 * self.cost_multiplier
        
        mu = self.estimator.compute(expected_error, expected_cost)
        return mu, expected_cost

    def process_task(self, task_type):
        print(f"    -> [AGENT {self.id} | {self.role.upper()}] executing '{task_type}'...")
        # Simulation d'un travail effectif
        _, cost = self.estimate_viability(task_type)
        return f"Result of {task_type} by {self.role}", cost

# =========================
#  MARKET SYSTEM (ECOSYSTEM)
# =========================
class AgentMarket:
    def __init__(self):
        # Creation de la startup AGI
        self.agents = [
            SpecializedYnorAgent("A1", "planner", cost_multiplier=1.5, error_profile={"planning": 0.1, "coding": 10.0, "research": 2.0}),
            SpecializedYnorAgent("A2", "coder", cost_multiplier=2.0, error_profile={"planning": 5.0, "coding": 0.1, "research": 4.0}),
            SpecializedYnorAgent("A3", "researcher", cost_multiplier=1.0, error_profile={"planning": 3.0, "coding": 8.0, "research": 0.2}),
        ]
        self.global_cost = 0.0

    def get_best_agent(self, task_type):
        best_mu = -float("inf")
        best_agent = None

        for agent in self.agents:
            # Calcul Ynor Variationnel: Maximisation de Mu pour remporter l'enchere
            mu, _ = agent.estimate_viability(task_type)
            if mu > best_mu:
                best_mu = mu
                best_agent = agent
                
        return best_agent, best_mu

    def assign_task(self, task_type):
        print(f"\n[MARKET] Broadcasting Task: '{task_type}'")
        
        # Le marche trouve l'agent avec le plus grand Mu (Viabilite maximale)
        assigned_agent, expected_mu = self.get_best_agent(task_type)
        
        print(f"  -> Bidding won by {assigned_agent.id} ({assigned_agent.role}) | Expected : {expected_mu:.2f}")
        
        result, cost = assigned_agent.process_task(task_type)
        self.global_cost += cost
        
        if self.global_cost > GLOBAL_COST_LIMIT:
            print(" GLOBAL COMPUTE LIMIT REACHED. HALTING CIVILIZATION.")
            return None
            
        print(f"  -> Task finished. Current Global Compute Cost: {self.global_cost:.1f}")
        return result

# =========================
#  SIMULATION
# =========================
def run_economy():
    print("Initiating Multi-Agent Ynor Economy (Distributed AGI Society)...")
    market = AgentMarket()
    
    # Simulation d'un brief de projet complexe brise en micro-taches
    tasks = ["planning", "research", "research", "coding", "coding", "planning"]
    
    for task in tasks:
        market.assign_task(task)

if __name__ == "__main__":
    run_economy()
