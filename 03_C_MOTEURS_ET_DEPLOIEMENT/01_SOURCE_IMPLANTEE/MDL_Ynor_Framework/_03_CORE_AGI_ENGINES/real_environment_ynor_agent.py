import torch
import torch.nn as nn
import random

# =========================
# ⚙️ MOCK TOOLS & PERCEPTION
# =========================
def perceive_text(input_text):
    # Mock LLM embedding: text -> tensor of size 4
    torch.manual_seed(hash(input_text) % 1000000)
    return torch.randn(4)

def act_in_world(action_type, data_tensor):
    print(f"  [ACTION EXECUTED] Type: {action_type.upper()}")
    # Simulate environment response
    if action_type == "search":
        return "Search results found: optimal logic involves A then B."
    elif action_type == "compute":
        return "Code execution successful: 0 errors."
    elif action_type == "respond":
        return "User, I have synthesized the answer for you."
    else:
        return "Tool failed."

def compute_reward(result_text):
    if "successful" in result_text or "optimal" in result_text:
        return 10.0
    return 1.0

# =========================
# 🧠 HIERARCHICAL YNOR BRAIN
# =========================
class DeepYnorBrain(nn.Module):
    def __init__(self, state_dim=4):
        super().__init__()
        # Decides which tool to use based on embedding (state)
        self.router = nn.Sequential(
            nn.Linear(state_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 3) # 0=search, 1=compute, 2=respond
        )
        
    def step(self, state):
        probs = torch.softmax(self.router(state), dim=-1)
        choice = torch.multinomial(probs, 1).item()
        
        tools = ["search", "compute", "respond"]
        return tools[choice]

# =========================
# 🔄 MEMORY UPDATE
# =========================
class SimpleMemory:
    def __init__(self):
        self.buffer = []
    def add(self, state, action, reward, next_state):
        self.buffer.append((state, action, reward, next_state))

# =========================
# 🚀 BOUCLE AGENT AUTONOME
# =========================
class FullStackYnorAgent:
    def __init__(self):
        self.brain = DeepYnorBrain()
        self.memory = SimpleMemory()

    def run_task(self, user_prompt, max_steps=5):
        print(f"\n[USER COMMAND]: '{user_prompt}'")
        state = perceive_text(user_prompt)

        for step in range(1, max_steps + 1):
            print(f"Step {step}...")
            
            # 1. Ynor Brain decides tool
            action_mode = self.brain.step(state)
            
            # 2. Act in the Real World
            result_text = act_in_world(action_mode, state)
            
            # 3. Perceive new world state
            next_state = perceive_text(result_text)
            
            # 4. Feedback (Reward)
            reward = compute_reward(result_text)
            print(f"  -> Reward Gained: {reward}")
            
            # 5. Memory Update
            self.memory.add(state, action_mode, reward, next_state)
            
            state = next_state

            if action_mode == "respond":
                print(f"✅ FINAL AGENT OUTPUT: {result_text}")
                break

        return "Task Completed."

def deploy_agent():
    print("Initiating Full Stack Ynor Autonomous Agent...")
    agent = FullStackYnorAgent()
    
    tasks = [
        "Analyze the market and write a summary.",
        "Code a python script to sort arrays.",
        "Hello, how are you?"
    ]
    
    for t in tasks:
        agent.run_task(t)

if __name__ == "__main__":
    deploy_agent()
