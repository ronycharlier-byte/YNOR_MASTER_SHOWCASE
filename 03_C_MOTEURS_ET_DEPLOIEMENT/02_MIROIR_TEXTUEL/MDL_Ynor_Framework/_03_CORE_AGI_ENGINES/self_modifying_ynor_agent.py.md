# MIROIR TEXTUEL - self_modifying_ynor_agent.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\self_modifying_ynor_agent.py
Taille : 3916 octets
SHA256 : fba57ac704cadffd8aa22a94baa948cfa872d2c9a5b1069b76f32a543aa3221a

```text
import torch
import torch.nn as nn
import torch.optim as optim

# =========================
# 🔴 LEVEL 2: SELF-MODIFICATION
# =========================
class MetaEvaluator:
    def __init__(self):
        self.history = []

    def record(self, mu, cost, dkl):
        self.history.append((mu, cost, dkl))

    def analyze(self):
        if len(self.history) < 10:
            return "stable"

        # Analyze the last 10 steps to determine if system is failing
        recent = self.history[-10:]
        avg_mu = sum([h[0] for h in recent]) / 10.0
        avg_cost = sum([h[1] for h in recent]) / 10.0

        if avg_mu < 0:
            return "collapse"
        elif avg_cost > 3.0: # Threshold for excessive compute cost
            return "overcompute"
        else:
            return "optimal"

class SelfModifier:
    def __init__(self, agent):
        self.agent = agent

    def adapt(self, signal):
        old_beta = self.agent.beta
        if signal == "collapse":
            self.agent.beta *= 1.2  # penalize cost more to force early stopping if collapsing
        elif signal == "overcompute":
            self.agent.beta *= 1.1  # reduce cost tolerance
        elif signal == "optimal":
            self.agent.beta *= 0.99 # relax constraint to allow deeper thinking
            
        # 🔒 Safety clamp to prevent divergence
        self.agent.beta = max(0.01, min(1.0, self.agent.beta))
        return old_beta != self.agent.beta

# =========================
# 🧠 LEVEL 1 & 0: AGENT & ESTIMATOR
# =========================
class InternalModel(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )
    def forward(self, x):
        return self.net(x)

class YnorEstimator:
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def compute(self, prediction, target, step, beta):
        d_kl = torch.mean((prediction - target) ** 2)
        i_eff = 1.0 / (d_kl + 1e-6)
        cost = torch.tensor(float(step))
        mu = i_eff - self.alpha * d_kl - beta * cost
        return mu, i_eff, d_kl, cost

class SelfAwareYnorAgent:
    def __init__(self, input_dim=4):
        self.model = InternalModel(input_dim)
        self.estimator = YnorEstimator(alpha=1.0)
        self.beta = 0.1 # Starting hyperparameter
        
        self.meta_eval = MetaEvaluator()
        self.self_modifier = SelfModifier(self)

    def step(self, state, target, step_idx):
        pred = self.model(state)
        mu, i_eff, d_kl, cost = self.estimator.compute(pred, target, step_idx, self.beta)
        
        # Meta recording
        self.meta_eval.record(mu.item(), cost.item(), d_kl.item())
        signal = self.meta_eval.analyze()
        
        # Action! (Self-Modification)
        changed = self.self_modifier.adapt(signal)
        return mu, signal, changed

# =========================
# 🧪 SIMULATION
# =========================
def run_self_modification():
    print("Initiating Level 3 AGI Cognitive Engine (Self-Modifying Architecture)...")
    agent = SelfAwareYnorAgent()
    
    # Introduce adversarial environment target drift
    target = torch.zeros(4)

    for episode in range(1, 101):
        # Environment gets harder every 25 episodes
        if episode % 25 == 0:
            target += 0.5 
            
        state = torch.randn(4)
        
        # Simulate an agent deciding to compute for 4 steps initially, then 2.
        steps_taken = 4 if episode < 50 else 2 
        
        mu, signal, changed = agent.step(state, target, steps_taken)

        if episode % 10 == 0 or changed:
            print(f"Ep {episode:03d} | Signal: {signal.upper():<11} | Beta: {agent.beta:.4f} | Mu: {mu.item():.2f}")

if __name__ == "__main__":
    run_self_modification()

```