# MIROIR TEXTUEL - multi_agent_ynor_simulation.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\multi_agent_ynor_simulation.py
Taille : 4236 octets
SHA256 : ddb6b4e124c9923467cf802f6b1a04f799b1f1082ea48f58f70205048bdbd110

```text
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
# 🎮 CONTROLLER (DECISION)
# =========================
class Controller(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim + 3, 32),
            nn.ReLU(),
            nn.Linear(32, 3)  # actions: [continue, stop, delegate]
        )

    def forward(self, state, metrics):
        x = torch.cat([state, metrics], dim=-1)
        logits = self.net(x)
        return torch.softmax(logits, dim=-1)


# =========================
# 🤖 AGENT
# =========================
class YnorAgent:
    def __init__(self, id, input_dim=4, hidden_dim=32):
        self.id = id
        self.model = InternalModel(input_dim, hidden_dim)
        self.controller = Controller(input_dim)
        self.estimator = YnorEstimator()

        self.optimizer = optim.Adam(
            list(self.model.parameters()) + list(self.controller.parameters()),
            lr=1e-3
        )

    def step(self, x):
        return self.model(x)

    def decide(self, state, metrics):
        probs = self.controller(state, metrics)
        action = torch.multinomial(probs, 1).item()
        return action  # 0=continue, 1=stop, 2=delegate

    def compute_ynor(self, pred, target, step):
        return self.estimator.compute(pred, target, step)


# =========================
# 🌐 MULTI-AGENT SYSTEM
# =========================
class MultiAgentYnor:
    def __init__(self, num_agents=3):
        self.agents = [YnorAgent(i) for i in range(num_agents)]

    def delegate(self, from_agent, state):
        # choose another agent randomly
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

            metrics = torch.tensor([i_eff.item(), d_kl.item(), cost.item()])

            action = current_agent.decide(state, metrics)

            if action == 1:  # STOP
                total_mu += mu
                break

            elif action == 2:  # DELEGATE
                next_agent = self.delegate(current_agent, state)

                # collaboration bonus
                total_mu += GAMMA

                current_agent = next_agent
                state = pred.detach()

            else:  # CONTINUE
                state = pred

            total_mu += mu

        return total_mu


# =========================
# 🧪 SIMULATION
# =========================
def simulate():
    system = MultiAgentYnor(num_agents=3)

    for episode in range(20):
        x = torch.randn(4)
        target = torch.zeros(4)

        mu = system.run_episode(x, target)

        print(f"Episode {episode} | Total Viability μ: {mu.item():.4f}")


if __name__ == "__main__":
    simulate()

```