import torch
import torch.nn as nn
import random

# ==========================================
# LA TRADUCTION ABSOLUE : S_dot = E(S) - D(S) + M(S,t) + w(t)
# ==========================================

class WorldModel(nn.Module):
    # E(S) : Expansion / GAnAration d'Information
    def __init__(self, state_dim=4):
        super().__init__()
        self.net = nn.Linear(state_dim, state_dim)
        
    def predict_gain(self, state):
        # Simule l'expansion de l'Atat (alpha)
        future_state = self.net(state)
        # alpha mesure la quantitA de "nouveautA" acquise favorablement
        alpha = torch.mean(torch.abs(future_state - state))
        return alpha

class DissipationModel(nn.Module):
    # D(S) : Dissipation AnergAtique / Perte structurelle
    def __init__(self, state_dim=4):
        super().__init__()
        self.net = nn.Linear(state_dim, state_dim)
        
    def apply(self, action_intensity):
        # D(S) dApend de la violence de l'action entreprise
        return torch.randn(4) * action_intensity

class IdentitySystem:
    # M(S,t) et kappa : MAmoire active et Poids Traumatique
    def __init__(self, state_dim=4):
        self.memory_vector = torch.zeros(state_dim)
        self.kappa = 0.1 # Charge mAmorielle initiale
        
    def memory_injection(self, state):
        # M(S,t) : Le passA influence le diffArentiel prAsent (inertie ou rAsonance)
        return self.memory_vector * 0.1
        
    def compute_kappa(self):
        return self.kappa
        
    def update(self, state, mu):
        # Trauma : si viabilitA < 0, la charge mAmoire s'alourdit (peur persistante)
        if mu < 0:
            self.kappa += 0.05
        elif mu > 0.3:
            # SuccAs : l'identitA se dAtend, la charge diminue
            self.kappa = max(0.01, self.kappa - 0.02)
        self.memory_vector = state.detach()

class PPOController:
    # Politique d'action (RAgule beta et l'intensitA de D(S))
    def decide(self, state, mu):
        if mu > 0.4:
            action_type = "NO_OP"
            intensity = 0.0
        elif mu > 0.0:
            action_type = "LIGHT_ACTION"
            intensity = 0.5
        else:
            action_type = "DEEP_REFLECTION"
            intensity = 2.0
        return action_type, intensity
        
    def compute_cost(self, intensity):
        # beta (friction d'action algorithmique)
        return intensity * 0.2

class MultiAgentField:
    # w(t) : Perturbation environnementale / forcing social multi-agent
    def get_forcing(self):
        # Un autre agent ou l'environnement perturbe le systAme
        return torch.randn(4) * 0.15

class SelfModifier:
    # Delta_theta (Auto-optimisation profonde si le systAme s'effondre)
    def adapt(self, agent_system, mu):
        if mu < -0.5:
            # Urgence : Restructure l'architecture pour Aviter la Mort Computationnelle
            agent_system.identity.kappa *= 0.5 # Force l'oubli du trauma
            print("  asi [SELF-MOD] Risque Vital : Effacement partiel du Trauma (Kappa divisA par 2).")

# ==========================================
# L'AGENT UNIFIA EXACT 1:1
# ==========================================
class YnorUnifiedAgent:
    def __init__(self, state_dim=4):
        self.state = torch.randn(state_dim)
        
        self.world_model = WorldModel(state_dim)
        self.dissipation = DissipationModel(state_dim)
        self.identity = IdentitySystem(state_dim)
        self.controller = PPOController()
        self.environment = MultiAgentField()
        self.self_modifier = SelfModifier()
        
    def step(self):
        # 1. PERCEPTION
        state = self.state.clone()
        
        # 2. MAMOIRE (M et kappa)
        M = self.identity.memory_injection(state)
        kappa = self.identity.compute_kappa()
        
        # 3. WORLD MODEL (E et alpha)
        alpha = self.world_model.predict_gain(state)
        
        # 4. AVALUATION PRAALABLE DE VIABILITA (pour PPO)
        mu_pre_action = alpha.item() - kappa
        
        # 5. PPO & DISSIPATION (D et beta)
        action_type, intensity = self.controller.decide(state, mu_pre_action)
        beta = self.controller.compute_cost(intensity)
        D = self.dissipation.apply(intensity)
        
        # === AQUATION PIVOT DE SURVIE ===
        # mu = Alpha - (Beta + Kappa)
        mu = alpha.item() - beta - kappa
        
        # 6. MULTI-AGENT / ENVIRONNEMENT (w)
        w = self.environment.get_forcing()
        
        # 7. DYNAMIQUE DIFFARENTIELLE YNOR : S_dot = E(S) - D(S) + M(S,t) + w(t)
        E = self.world_model.net(state) - state # Transformation pure du World Model
        S_dot = E - D + M + w
        
        # IntAgration temporelle (Avolution de l'Atat mental)
        self.state += S_dot * 0.1
        
        # 8. SELF-MODIFICATION & UPDATE MAMOIRE
        self.self_modifier.adapt(self, mu)
        self.identity.update(self.state, mu)
        
        return action_type, mu, alpha.item(), beta, kappa

def run_unified_equation():
    print(">>> DAMARRAGE DE L'AQUATION AGI UNIFIAE : S_dot = E(S) - D(S) + M(S,t) + w(t) <<<")
    print(">>> CONTRAINTE DE SURVIE ABSOLUE : mu = Alpha - (Beta + Kappa) > 0 <<<\n")
    agent = YnorUnifiedAgent()
    
    for t in range(1, 21):
        action, mu, alpha, beta, kappa = agent.step()
        print(f"Cycle {t:02d} | Action: {action:<16} | I: {mu:>+5.3f} | [I: {alpha:.3f} | I: {beta:.3f} | I: {kappa:.3f}]")

if __name__ == "__main__":
    run_unified_equation()

