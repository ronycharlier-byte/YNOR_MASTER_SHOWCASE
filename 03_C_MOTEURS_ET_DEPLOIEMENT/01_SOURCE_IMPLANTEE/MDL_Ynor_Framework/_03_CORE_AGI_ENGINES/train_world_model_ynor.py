import torch
import torch.nn as nn
import torch.optim as optim
import random

# =========================
# 🔧 CONFIG
# =========================
ALPHA = 1.0
BETA = 0.1
GAMMA = 0.2
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
# 🌍 WORLD MODEL
# =========================
class WorldModel(nn.Module):
    def __init__(self, state_dim, action_dim=3, hidden_dim=64):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(state_dim + action_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, state_dim)
        )
    def forward(self, states, actions):
        x = torch.cat([states, actions], dim=-1)
        return self.model(x)

def encode_action(action_id, action_dim=3):
    vec = torch.zeros(action_dim)
    vec[action_id] = 1.0
    return vec

# =========================
# 💾 REPLAY BUFFER
# =========================
class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buffer = []
        self.capacity = capacity

    def add(self, state, action, next_state):
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append((state, action, next_state))

    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, next_states = zip(*batch)
        return torch.stack(states), torch.stack(actions), torch.stack(next_states)

# =========================
# 🤖 DUMB AGENT (Data collection)
# =========================
class YnorAgentDumb:
    def __init__(self, input_dim=4, hidden_dim=32):
        self.model = InternalModel(input_dim, hidden_dim)
    def step(self, x):
        return self.model(x)

class MultiAgentSystem:
    def __init__(self, num_agents=3):
        self.agents = [YnorAgentDumb() for _ in range(num_agents)]

# =========================
# 🔄 TRAINING & COLLECTION
# =========================
def collect_data(system, buffer):
    x = torch.randn(4)
    current_agent = random.choice(system.agents)
    state = x.clone()

    for step in range(5):
        pred = current_agent.step(state)
        action_id = random.choice([0, 1, 2])  # 0=continue, 1=stop, 2=delegate
        action_vec = encode_action(action_id)
        
        next_state = pred.detach()
        buffer.add(state, action_vec, next_state)
        state = next_state

def train_world_model(world_model, buffer, optimizer, epochs=5):
    if len(buffer.buffer) < 32:
        return

    for epoch in range(epochs):
        states, actions, next_states = buffer.sample(32)
        preds = world_model(states, actions)
        
        loss = torch.mean((preds - next_states) ** 2)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    return loss.item()

# =========================
# 🧪 SIMULATION
# =========================
def run_world_model_training():
    print("Initiating World Model Training (Environment Dynamics Learning)...")
    system = MultiAgentSystem(num_agents=3)
    world_model = WorldModel(state_dim=4, action_dim=3)
    optimizer = torch.optim.Adam(world_model.parameters(), lr=1e-3)
    buffer = ReplayBuffer()

    for episode in range(1, 201):
        collect_data(system, buffer)
        
        loss = train_world_model(world_model, buffer, optimizer, epochs=5)
        
        if episode % 20 == 0 and loss is not None:
            print(f"Episode {episode:03d} | World Model MSE Loss: {loss:.4f}")

if __name__ == "__main__":
    run_world_model_training()
