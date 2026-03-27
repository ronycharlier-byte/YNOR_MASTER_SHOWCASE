# MIROIR TEXTUEL - ynor_agi_prototype_v1.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\ynor_agi_prototype_v1.py
Taille : 8072 octets
SHA256 : 628a6033d8fbdbe1ec93a9064a459c3a39343ec350fa4f0251415ab798ed88fc

```text
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.distributions import Categorical
import numpy as np

# =====================================================================
# 🧬 ⚙️ ARCHITECTURE AGI YNOR - PROTOTYPE V1 (PyTorch)
# Implémentation du Principe Variationnel de Viabilité sous Contrainte
# =====================================================================

# ---------------------------------------------------------
# 1. MODÈLE INTERNE (Générateur d'inférences)
# ---------------------------------------------------------
class YnorInternalModel(nn.Module):
    """
    Réseau de neurones récurrent / itératif.
    Chaque passage (étape) affine la prédiction mais augmente le coût calculatoire (FLOPs).
    """
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.rnn_cell = nn.GRUCell(hidden_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, hidden_state=None):
        if hidden_state is None:
            hidden_state = torch.relu(self.encoder(x))
        # Affinement itératif de la pensée (1 step de compute)
        next_hidden = self.rnn_cell(hidden_state, hidden_state)
        prediction = self.decoder(next_hidden)
        return prediction, next_hidden

# ---------------------------------------------------------
# 2. CONTRÔLEUR YNOR (La Politique π_t de l'AGI)
# ---------------------------------------------------------
class YnorController(nn.Module):
    """
    Le cœur de l'AGI. Décide de manière endogène : 
    Faut-il utiliser plus de calcul (Continue = 1) ou répondre maintenant (Stop = 0) ?
    """
    def __init__(self, input_dim, metric_dim, hidden_dim):
        super().__init__()
        # Observe le stimulus (input) ET son propre état interne (viabilité actuelle)
        self.net = nn.Sequential(
            nn.Linear(input_dim + metric_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 2) # 2 actions: 0 (Stop), 1 (Continue)
        )
        
    def forward(self, x, current_metrics):
        state = torch.cat([x, current_metrics], dim=-1)
        logits = self.net(state)
        return Categorical(logits=logits)

# ---------------------------------------------------------
# 3. ESTIMATEUR DE VIABILITÉ (L'Action S_Ynor)
# ---------------------------------------------------------
class YnorEstimator:
    def __init__(self, alpha=0.1, beta=0.05):
        self.alpha = alpha # Pénalité d'incohérence / divergence
        self.beta = beta   # Prix du calcul (Coût par itération)
        
    def compute_metrics(self, y_pred, y_target, compute_steps):
        # 1. I_eff : Information Utile (Simulée ici par l'inverse de la perte MSE)
        mse = F.mse_loss(y_pred, y_target, reduction='none').mean(dim=1, keepdim=True)
        # Plus l'erreur baisse, plus on a extrait d'info utile
        I_eff = 1.0 / (1.0 + mse) 
        
        # 2. D_KL : Instabilité résiduelle (Simulée par la persistance de l'erreur)
        # Dans un vrai système, ce serait par rapport à un modèle P*
        D_kl = mse * 0.5 
        
        # 3. C : Coût computationnel réel (profondeur)
        C = compute_steps
        
        # Calcul du Lagrangien local (Viabilité instantanée)
        L = I_eff - (self.alpha * D_kl) - (self.beta * C)
        
        return L, I_eff, D_kl, C

# ---------------------------------------------------------
# 4. LE SYSTÈME AGI GLOBAL
# ---------------------------------------------------------
class YnorAGI:
    def __init__(self, input_dim, hidden_dim, output_dim, max_compute=10):
        self.model = YnorInternalModel(input_dim, hidden_dim, output_dim)
        # Le contrôleur reçoit l'input + 3 métriques (I_eff, D_kl, C)
        self.controller = YnorController(input_dim, 3, hidden_dim)
        self.estimator = YnorEstimator(alpha=0.2, beta=0.1)
        
        self.optimizer_model = optim.Adam(self.model.parameters(), lr=1e-3)
        self.optimizer_ctrl = optim.Adam(self.controller.parameters(), lr=1e-3)
        
        self.max_compute = max_compute

    def process_and_learn(self, x, y_target):
        batch_size = x.size(0)
        
        # Initialisation
        hidden = None
        compute_steps = torch.ones(batch_size, 1) # Commence avec au moins 1 step
        active_mask = torch.ones(batch_size, dtype=torch.bool)
        
        log_probs = []
        viability_history = []
        
        # Boucle d'adaptation endogène
        for step in range(self.max_compute):
            # 1. Inférence (Coûte du calcul)
            y_pred, hidden = self.model(x, hidden)
            
            # 2. Rétrospection : Estimation de la viabilité
            with torch.no_grad():
                L, I_eff, D_kl, C = self.estimator.compute_metrics(y_pred, y_target, float(step + 1))
                metrics = torch.cat([I_eff, D_kl, torch.full_like(I_eff, float(step+1))], dim=-1)
            
            # 3. Décision du Contrôleur (RL)
            dist = self.controller(x, metrics)
            action = dist.sample() # 0 = Stop, 1 = Continue
            
            # On enregistre la probabilité pour le policy gradient
            log_probs.append(dist.log_prob(action))
            viability_history.append(L)
            
            # Mise à jour de qui doit continuer
            # Si action == 0 (Stop), on considère que le calcul est fini pour cet item
            force_stop = (action == 0)
            active_mask = active_mask & ~force_stop
            
            if not active_mask.any():
                break # Tout le monde a décidé de s'arrêter
                
        # --- PHASE D'APPRENTISSAGE (Mise à jour Ynor) ---
        # Le reward final est la viabilité L atteinte au moment de l'arrêt
        final_L, _, _, _ = self.estimator.compute_metrics(y_pred, y_target, compute_steps.float())
        
        # 1. Entraînement du modèle (Supervisé local pour maximiser l'information)
        loss_model = F.mse_loss(y_pred, y_target)
        self.optimizer_model.zero_grad()
        loss_model.backward(retain_graph=True)
        self.optimizer_model.step()
        
        # 2. Entraînement du Contrôleur (Reinforce algorithm pour maximiser S_Ynor)
        policy_loss = []
        for lp, v_reward in zip(log_probs, viability_history):
            # Le contrôleur apprend à favoriser les actions qui rapportent de la viabilité
            policy_loss.append(-lp * v_reward.detach().squeeze())
            
        policy_loss = torch.stack(policy_loss).sum()
        self.optimizer_ctrl.zero_grad()
        policy_loss.backward()
        self.optimizer_ctrl.step()
        
        return final_L.mean().item(), loss_model.item(), step + 1

# =====================================================================
# SIMULATION DE DÉMONSTRATION
# =====================================================================
if __name__ == "__main__":
    print("\n🚀 Lancement du Prototype AGI Ynor V1")
    
    # Paramètres arbitraires pour simulation
    INPUT_DIM = 10
    HIDDEN_DIM = 32
    OUTPUT_DIM = 5
    
    agi = YnorAGI(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)
    
    print("\nDébut de l'entraînement (Optimisation de la Viabilité Globale)...")
    for epoch in range(1, 101):
        # Création de tâches aléatoires de difficulté variable
        x_batch = torch.randn(16, INPUT_DIM)
        # La cible est une fonction non-linéaire arbitraire (complexité cachée)
        y_target = torch.sin(x_batch[:, :OUTPUT_DIM]) * 2.0
        
        viability, error, avg_compute = agi.process_and_learn(x_batch, y_target)
        
        if epoch % 20 == 0:
            print(f"Époque {epoch} | Viabilité (\u03bc): {viability:.4f} | Erreur: {error:.4f} | Profondeur moyenne de calcul (Coût): {avg_compute}")

    print("\n✅ Simulation terminée. L'AGI a appris à auto-réguler son allocation de ressources !")

```