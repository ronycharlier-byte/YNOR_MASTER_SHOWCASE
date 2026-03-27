# MIROIR TEXTUEL - ppo_world_model_ynor.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\ppo_world_model_ynor.py
Taille : 6973 octets
SHA256 : 0df8e00f246af3f13b073bf2306752565bc66fb7666ffef27c5641704b58f0ab

```text
import torch
import torch.nn as nn
import torch.optim as optim
import random

# =========================
# 🔧 CONFIG
# =========================
ALPHA = 1.0   
BETA = 0.1    
GAMMA_RL = 0.99  # Standard PPO discount factor
MAX_STEPS = 10
SIMULATION_DEPTH = 3

# =========================
# 🧠 INTERNAL MODEL & ESTIMATOR
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
    def compute(self, prediction, target, step):
        d_kl = torch.mean((prediction - target) ** 2)
        i_eff = 1.0 / (d_kl + 1e-6)
        cost = torch.tensor(float(step))
        mu = i_eff - ALPHA * d_kl - BETA * cost
        return mu, i_eff, d_kl, cost

# =========================
# 🌍 WORLD MODEL
# =========================
class WorldModel(nn.Module):
    def __init__(self, state_dim=4, action_dim=3, hidden_dim=64):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )
    def forward(self, state, action):
        x = torch.cat([state, action], dim=-1)
        return self.model(x)

def encode_action(action_id, action_dim=3):
    vec = torch.zeros(action_dim)
    vec[action_id] = 1.0
    return vec

def simulate_future(agent_model, estimator, world_model, state, target, depth: int):
    best_score = -1e9
    best_action = 0

    for action in [0, 1, 2]:
        sim_state = state.clone()
        total_mu = 0
        for d in range(depth):
            action_vec = encode_action(action)
            sim_state = world_model(sim_state, action_vec)
            pred = agent_model(sim_state)
            mu, _, _, _ = estimator.compute(pred, target, d+1)
            total_mu += mu.item()

        if total_mu > best_score:
            best_score = total_mu
            best_action = action
    return best_action

# =========================
# 🤖 DUMB AGENT WRAPPER (for functions)
# =========================
class MockAgent:
    def __init__(self):
        self.model = InternalModel(4, 32)
        self.estimator = YnorEstimator()
    def compute_ynor(self, pred, target, step):
        return self.estimator.compute(pred, target, step)

# =========================
# 🎯 PPO POLICY
# =========================
class PPOPolicy(nn.Module):
    def __init__(self, state_dim=4):
        super().__init__()
        self.actor = nn.Sequential(
            nn.Linear(state_dim + 3, 64),
            nn.ReLU(),
            nn.Linear(64, 3)
        )
        self.critic = nn.Sequential(
            nn.Linear(state_dim + 3, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, state, metrics):
        x = torch.cat([state, metrics], dim=-1)
        logits = self.actor(x)
        value = self.critic(x)
        return logits, value

def select_action(policy, state, metrics):
    logits, value = policy(state, metrics)
    probs = torch.softmax(logits, dim=-1)
    dist = torch.distributions.Categorical(probs)
    action = dist.sample()
    return action.item(), dist.log_prob(action), value

# =========================
# 🔄 PPO ROLLOUT + UPDATE
# =========================
def rollout(agent, world_model, policy, target):
    memory = []
    state = torch.randn(4)

    for step in range(1, MAX_STEPS + 1):
        # 🧠 1. IMAGINATION
        sim_action = simulate_future(agent.model, agent.estimator, world_model, state, target, depth=SIMULATION_DEPTH)
        
        # Current Inference
        pred = agent.model(state)
        mu, i_eff, d_kl, cost = agent.compute_ynor(pred, target, step)
        metrics = torch.tensor([i_eff.item(), d_kl.item(), cost.item()])
        
        # 🎯 2. DECISION (PPO Policy)
        action, log_prob, value = select_action(policy, state, metrics)
        
        # 💥 BLEND IMAGINATION & REALITY
        final_action = sim_action if random.random() < 0.5 else action
        action_vec = encode_action(final_action)
        
        # NEXT STATE FROM WORLD MODEL (approximating environment)
        next_state = world_model(state, action_vec)
        reward = mu.item()
        
        memory.append((state, metrics, final_action, log_prob, value, reward))
        state = next_state.detach()
        
        if final_action == 1:  # STOP
            break
            
    return memory

def ppo_update(policy, optimizer, memory, gamma=GAMMA_RL, eps_clip=0.2):
    if len(memory) == 0: return

    states, metrics, actions, log_probs, values, rewards = zip(*memory)

    returns = []
    G = 0
    for r in reversed(rewards):
        G = r + gamma * G
        returns.insert(0, G)

    returns = torch.tensor(returns, dtype=torch.float32)
    values = torch.cat(values).squeeze()
    
    if values.dim() == 0:
        values = values.unsqueeze(0)

    advantages = returns - values.detach()

    if len(advantages) > 1:
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

    for _ in range(4):  # PPO epochs
        for i in range(len(states)):
            state_i = states[i].unsqueeze(0) if states[i].dim() == 1 else states[i]
            metrics_i = metrics[i].unsqueeze(0) if metrics[i].dim() == 1 else metrics[i]
            
            logits, value = policy(state_i, metrics_i)
            probs = torch.softmax(logits, dim=-1)
            dist = torch.distributions.Categorical(probs)
            
            new_log_prob = dist.log_prob(torch.tensor([actions[i]]))
            
            ratio = torch.exp(new_log_prob - log_probs[i].detach())
            surr1 = ratio * advantages[i]
            surr2 = torch.clamp(ratio, 1 - eps_clip, 1 + eps_clip) * advantages[i]

            actor_loss = -torch.min(surr1, surr2)
            critic_loss = (returns[i] - value.squeeze())**2

            loss = actor_loss + 0.5 * critic_loss

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

# =========================
# 🚀 MAIN GLOBALE
# =========================
def train_ppo_ynor():
    print("Initiating Final PPO + World Model Ynor Engine...")
    
    agent = MockAgent()
    world_model = WorldModel(4, 3)
    
    policy = PPOPolicy(state_dim=4)
    optimizer = torch.optim.Adam(policy.parameters(), lr=1e-3)

    target = torch.zeros(4)

    for episode in range(1, 201):
        memory = rollout(agent, world_model, policy, target)
        ppo_update(policy, optimizer, memory)

        if episode % 10 == 0:
            total_reward = sum([m[-1] for m in memory])
            print(f"[Episode {episode:03d}] Ynor Reward: {total_reward:.4f} | Steps taken: {len(memory)}")

if __name__ == "__main__":
    train_ppo_ynor()

```