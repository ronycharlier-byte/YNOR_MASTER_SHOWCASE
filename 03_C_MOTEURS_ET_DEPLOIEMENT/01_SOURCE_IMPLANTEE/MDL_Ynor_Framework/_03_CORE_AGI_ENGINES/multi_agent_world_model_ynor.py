import torch
import torch.nn as nn
import torch.optim as optim
import random

# =========================
# 🔧 CONFIG
# =========================
ALPHA = 1.0   # divergence penalty
BETA = 0.1    # cost penalty
GAMMA = 0.2   # collaboration bonus
MAX_STEPS = 10
SIMULATION_DEPTH = 3

# =========================
# 🧠 INTERNAL MODEL
# =========================
class InternalModel(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# 📊 YNOR ESTIMATOR
# =========================
class YnorEstimator:
    def compute(self, prediction, target, step):
        # divergence (MSE proxy)
        d_kl = torch.mean((prediction - target) ** 2)

        # information (inverse error proxy)
        i_eff = 1.0 / (d_kl + 1e-6)

        # cost = steps used
        cost = torch.tensor(float(step))

        # Ynor objective
        mu = i_eff - ALPHA * d_kl - BETA * cost

        return mu, i_eff, d_kl, cost

# =========================
# 🌍 WORLD MODEL (NEW)
# =========================
class WorldModel(nn.Module):
    def __init__(self, state_dim, action_dim=3, hidden_dim=64):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )

    def forward(self, state, action):
        x = torch.cat([state, action], dim=-1)
        next_state = self.model(x)
        return next_state

def encode_action(action_id, action_dim=3):
    vec = torch.zeros(action_dim)
    vec[action_id] = 1.0
    return vec

def simulate_future(agent, world_model, state, target, depth=SIMULATION_DEPTH):
    best_score = -1e9
    best_action = 0

    for action in [0, 1, 2]:  # 0=continue, 1=stop, 2=delegate
        sim_state = state.clone()
        total_mu = 0

        for d in range(depth):
            action_vec = encode_action(action)
            sim_state = world_model(sim_state, action_vec)

            pred = agent.model(sim_state)
            mu, i_eff, d_kl, cost = agent.compute_ynor(pred, target, d+1)

            total_mu += mu.item()

        if total_mu > best_score:
            best_score = total_mu
            best_action = action

    return best_action

# =========================
# 🤖 AGENT (PROSPECTIVE)
# =========================
class YnorAgent:
    def __init__(self, id, input_dim=4, hidden_dim=32):
        self.id = id
        self.model = InternalModel(input_dim, hidden_dim)
        self.estimator = YnorEstimator()
        
        # World Model intégré à l'agent
        self.world_model = WorldModel(state_dim=input_dim, action_dim=3)

        self.optimizer = optim.Adam(
            list(self.model.parameters()) + list(self.world_model.parameters()),
            lr=1e-3
        )

    def step(self, x):
        return self.model(x)

    def decide_with_world_model(self, state, target):
        action = simulate_future(self, self.world_model, state, target)
        return action

    def compute_ynor(self, pred, target, step):
        return self.estimator.compute(pred, target, step)


# =========================
# 🌐 MULTI-AGENT SYSTEM (WM ENHANCED)
# =========================
class MultiAgentYnor:
    def __init__(self, num_agents=3):
        self.agents = [YnorAgent(i) for i in range(num_agents)]

    def delegate(self, from_agent, state):
        candidates = [a for a in self.agents if a.id != from_agent.id]
        target_agent = random.choice(candidates)
        return target_agent

    def run_episode(self, x, target):
        total_mu = 0
        current_agent = random.choice(self.agents)
        state = x.clone()

        for step in range(1, MAX_STEPS + 1):
            pred = current_agent.step(state)
            mu, i_eff, d_kl, cost = current_agent.compute_ynor(pred, target, step)
            
            # 🧠 ANTICIPATION (IMAGINATION)
            action = current_agent.decide_with_world_model(state, target)

            if action == 1:  # STOP
                total_mu += mu.item()
                break

            elif action == 2:  # DELEGATE
                next_agent = self.delegate(current_agent, state)
                total_mu += GAMMA
                current_agent = next_agent
                state = pred.detach()

            else:  # CONTINUE
                state = pred.detach()

            total_mu += mu.item()

        return total_mu

# =========================
# 🧪 SIMULATION
# =========================
def simulate():
    print("Initiating Ynor World Model Simulation (Prospective Intelligence)...")
    system = MultiAgentYnor(num_agents=3)

    for episode in range(20):
        x = torch.randn(4)
        target = torch.zeros(4)

        mu = system.run_episode(x, target)

        print(f"Episode {episode} | Total Viability μ (with Planning): {mu:.4f}")

if __name__ == "__main__":
    simulate()
