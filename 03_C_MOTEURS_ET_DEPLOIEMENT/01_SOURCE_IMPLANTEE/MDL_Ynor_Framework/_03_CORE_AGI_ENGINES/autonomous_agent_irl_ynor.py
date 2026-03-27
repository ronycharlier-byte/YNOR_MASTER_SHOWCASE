import torch
import torch.nn as nn
import time
import os

# =========================
# 🔒 SÉCURITÉ & CONFINEMENT (DEFCON 1)
# =========================
ALLOWED_ACTIONS = ["read_file", "write_file", "search_web", "do_nothing"]
MAX_COST = 50.0  # Budget Compute Strict
READ_ONLY_MODE = os.getenv("MDL_ALLOW_WRITE", "FALSE").upper() != "TRUE"

def log_audit_action(action, detail):
    """Enregistre toute tentative d'écriture dans un journal d'audit infalsifiable."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] AUDIT: {action} | {detail}\n"
    with open("mdl_audit_trail.log", "a", encoding="utf-8") as f:
        f.write(log_entry)

# =========================
# ⚙️ MOCK TOOLS (IRL BINDINGS)
# =========================
def search_web(query):
    print(f"  [WEB] Simulated search querying: '{query}'...")
    return f"Result for {query}: The market is shifting towards AI automation."

def read_file(path):
    print(f"  [FS] Reading file: {path}...")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return "File not found."

def write_file(filename, content):
    if READ_ONLY_MODE:
        print(f"  [⚠️ SECURITY] Write Attempt Blocked: {filename}. (READ_ONLY_MODE=TRUE)")
        log_audit_action("BLOCKED_WRITE", f"Attempted to write to {filename}")
        return "ERROR: System is in READ_ONLY_MODE. Human approval required."
    
    print(f"  [FS] Writing to file: {filename}...")
    log_audit_action("AUTHORIZED_WRITE", f"Writing to {filename}")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File {filename} successfully written."

# =========================
# 🧠 YNOR META-CONTROLLER (Mock IRL)
# =========================
class RealWorldYnorBrain(nn.Module):
    def __init__(self, state_dim=4):
        super().__init__()
        # 0=read, 1=write, 2=search, 3=do_nothing
        self.net = nn.Sequential(
            nn.Linear(state_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 4)
        )
    def forward(self, state):
        probs = torch.softmax(self.net(state), dim=-1)
        choice = torch.multinomial(probs, 1).item()
        return ALLOWED_ACTIONS[choice]

# =========================
# 🔄 MEMORY + SELF-MOD
# =========================
class AgentMemory:
    def __init__(self):
        self.log = []
    def add(self, state, action, reward, result):
        self.log.append({"action": action, "reward": reward, "result": result})

# =========================
# 🚀 BOUCLE AUTONOME INFINIE (CŒUR AGI)
# =========================
class AutonomousIRLYnorAgent:
    def __init__(self):
        self.brain = RealWorldYnorBrain()
        self.memory = AgentMemory()
        self.total_cost = 0.0

    def get_environment_state(self):
        # Perception réelle simulée (ex: observe le dossier, la bourse, l'heure)
        torch.manual_seed(int(time.time() * 1000) % 10000)
        return torch.randn(4)

    def execute_real_action(self, action):
        cost_incurred = 0.0
        result = ""
        if action == "do_nothing":
            cost_incurred = 0.1
            result = "Agent rested. Energy saved."
        elif action == "search_web":
            cost_incurred = 2.0
            result = search_web("AI startup opportunities")
        elif action == "read_file":
            cost_incurred = 0.5
            result = read_file("target_sandbox.txt")
        elif action == "write_file":
            cost_incurred = 1.0
            result = write_file("target_sandbox.txt", "Autonomous Agent Output Data.")
            
        self.total_cost += cost_incurred
        return result, cost_incurred

    def evaluate(self, result, cost):
        # Fonction de récompense (Ynor proxy : max info / min coût)
        base_reward = 10.0 if "success" in result.lower() or "result" in result.lower() else 1.0
        # Sanction sur le coût pour forcer l'optimisation mathématique
        return base_reward - (0.5 * cost)

    def self_improve(self):
        # L'agent analyse ses récompenses récentes et met à jour ses poids (Mock)
        pass

    def run_infinite_loop(self, max_iter=5):
        print(">>> DEMARRAGE DE LA BOUCLE AUTONOME YNOR (IRL)...")
        iteration = 0
        while True:
            iteration += 1
            print(f"\n--- [CYCLE {iteration}] ---")
            
            # BUDGET CHECK (Safety)
            if self.total_cost > MAX_COST:
                print("🚨 MAXIMUM COMPUTE BUDGET REACHED! HALTING AGENT.")
                break
                
            observation = self.get_environment_state()
            action = self.brain(observation)
            print(f"🧠 Meta-Controller a choisi l'action : [{action.upper()}]")
            
            result, cost = self.execute_real_action(action)
            reward = self.evaluate(result, cost)
            
            print(f"📈 Résultat: {result[:50]}... | Reward: {reward:.2f} | Coût total: {self.total_cost:.1f}")
            
            self.memory.add(observation, action, reward, result)
            self.self_improve()
            
            time.sleep(1) # Rythme mental continu

            if iteration >= max_iter:
                print("\n>>> FIN DE LA SIMULATION (Sécurité Anti-Runaway activée pour le test)")
                break

if __name__ == "__main__":
    agent = AutonomousIRLYnorAgent()
    agent.run_infinite_loop(max_iter=5)
