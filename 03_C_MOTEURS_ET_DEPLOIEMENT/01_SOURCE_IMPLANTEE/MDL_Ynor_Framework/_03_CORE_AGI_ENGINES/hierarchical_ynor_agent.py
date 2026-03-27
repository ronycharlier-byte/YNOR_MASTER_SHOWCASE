import torch
import torch.nn as nn
import torch.optim as optim
import random

# =========================
# 🔧 CONFIG
# =========================
ALPHA = 1.0   
BETA = 0.1    

# =========================
# 📊 YNOR ESTIMATOR
# =========================
class YnorEstimator:
    def compute(self, prediction, target, step):
        d_kl = torch.mean((prediction - target) ** 2)
        i_eff = 1.0 / (d_kl + 1e-6)
        cost = torch.tensor(float(step) * 0.1) # Simulate diff costs: step 1=low, 2=high
        mu = i_eff - ALPHA * d_kl - BETA * cost
        return mu, i_eff, d_kl, cost

# =========================
# 🌍 WORLD MODEL (Mock for delegation/simulation)
# =========================
class WorldModel(nn.Module):
    def __init__(self, state_dim=4):
        super().__init__()
        self.net = nn.Linear(state_dim, state_dim)
    def forward(self, x):
        return self.net(x)

def simulate_future(agent, world_model, state, target):
    # Mocking a "Delegate" or "Simulation" output which takes longer but may be accurate
    return world_model(state)

# =========================
# 🧠 SYSTEM 1 (FAST)
# =========================
class FastSystem(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Linear(input_dim, input_dim)

    def forward(self, x):
        return self.net(x)

# =========================
# 🧠 SYSTEM 2 (DEEP)
# =========================
class DeepSystem(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# 🧠 META CONTROLLER (YNOR)
# =========================
class MetaController(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim + 3, 64),
            nn.ReLU(),
            nn.Linear(64, 3)  # fast / deep / delegate
        )

    def forward(self, state, metrics):
        x = torch.cat([state, metrics], dim=-1)
        return torch.softmax(self.net(x), dim=-1)

# =========================
# 🤖 HIERARCHICAL AGENT
# =========================
class HierarchicalYnorAgent:
    def __init__(self, input_dim=4):
        self.fast = FastSystem(input_dim)
        self.deep = DeepSystem(input_dim)
        self.meta = MetaController(input_dim)
        self.estimator = YnorEstimator()

    def step(self, state, target, world_model):
        pred_fast = self.fast(state)
        pred_deep = self.deep(state)

        # Compute respective viabilities for fast (cost 1) vs deep (cost 5)
        mu_fast, _, _, _ = self.estimator.compute(pred_fast, target, 1)
        mu_deep, _, _, _ = self.estimator.compute(pred_deep, target, 5)

        metrics = torch.tensor([
            mu_fast.item(),
            mu_deep.item(),
            1.0  # Delegate prior/cost heuristic
        ])

        probs = self.meta(state, metrics)
        choice = torch.multinomial(probs, 1).item()

        if choice == 0:
            return pred_fast, "fast"
        elif choice == 1:
            return pred_deep, "deep"
        else:
            return simulate_future(self, world_model, state, target), "delegate"

# =========================
# 🧪 SIMULATION
# =========================
def run_hierarchy():
    print("Initiating Hierarchical Ynor Agent (System 1 / System 2 / Delegate)...")
    agent = HierarchicalYnorAgent()
    world_model = WorldModel()

    routes_taken = {"fast": 0, "deep": 0, "delegate": 0}

    for episode in range(200):
        state = torch.randn(4)
        target = torch.zeros(4)

        pred, route = agent.step(state, target, world_model)
        routes_taken[route] += 1

        if episode % 40 == 0:
            print(f"Task {episode:03d} -> Routed to: {route.upper()}")

    print("\nTotal Cognitive Routing Distribution:")
    print(routes_taken)

if __name__ == "__main__":
    run_hierarchy()
