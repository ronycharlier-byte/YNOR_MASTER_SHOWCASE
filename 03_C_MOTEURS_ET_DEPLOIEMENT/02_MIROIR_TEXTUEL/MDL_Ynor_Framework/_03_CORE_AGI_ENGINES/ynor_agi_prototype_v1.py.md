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
#   ARCHITECTURE AGI YNOR - PROTOTYPE V1 (PyTorch)
# Implementation du Principe Variationnel de Viabilite sous Contrainte
# =====================================================================

# ---------------------------------------------------------
# 1. MODELE INTERNE (Generateur d'inferences)
# ---------------------------------------------------------
class YnorInternalModel(nn.Module):
    """
    Reseau de neurones recurrent / iteratif.
    Chaque passage (etape) affine la prediction mais augmente le cout calculatoire (FLOPs).
    """
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.rnn_cell = nn.GRUCell(hidden_dim, hidden_dim)
        self.decoder = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, hidden_state=None):
        if hidden_state is None:
            hidden_state = torch.relu(self.encoder(x))
        # Affinement iteratif de la pensee (1 step de compute)
        next_hidden = self.rnn_cell(hidden_state, hidden_state)
        prediction = self.decoder(next_hidden)
        return prediction, next_hidden

# ---------------------------------------------------------
# 2. CONTROLEUR YNOR (La Politique _t de l'AGI)
# ---------------------------------------------------------
class YnorController(nn.Module):
    """
    Le cur de l'AGI. Decide de maniere endogene : 
    Faut-il utiliser plus de calcul (Continue = 1) ou repondre maintenant (Stop = 0) ?
    """
    def __init__(self, input_dim, metric_dim, hidden_dim):
        super().__init__()
        # Observe le stimulus (input) ET son propre etat interne (viabilite actuelle)
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
# 3. ESTIMATEUR DE VIABILITE (L'Action S_Ynor)
# ---------------------------------------------------------
class YnorEstimator:
    def __init__(self, alpha=0.1, beta=0.05):
        self.alpha = alpha # Penalite d'incoherence / divergence
        self.beta = beta   # Prix du calcul (Cout par iteration)
        
    def compute_metrics(self, y_pred, y_target, compute_steps):
        # 1. I_eff : Information Utile (Simulee ici par l'inverse de la perte MSE)
        mse = F.mse_loss(y_pred, y_target, reduction='none').mean(dim=1, keepdim=True)
        # Plus l'erreur baisse, plus on a extrait d'info utile
        I_eff = 1.0 / (1.0 + mse) 
        
        # 2. D_KL : Instabilite residuelle (Simulee par la persistance de l'erreur)
        # Dans un vrai systeme, ce serait par rapport a un modele P*
        D_kl = mse * 0.5 
        
        # 3. C : Cout computationnel reel (profondeur)
        C = compute_steps
        
        # Calcul du Lagrangien local (Viabilite instantanee)
        L = I_eff - (self.alpha * D_kl) - (self.beta * C)
        
        return L, I_eff, D_kl, C

# ---------------------------------------------------------
# 4. LE SYSTEME AGI GLOBAL
# ---------------------------------------------------------
class YnorAGI:
    def __init__(self, input_dim, hidden_dim, output_dim, max_compute=10):
        self.model = YnorInternalModel(input_dim, hidden_dim, output_dim)
        # Le controleur recoit l'input + 3 metriques (I_eff, D_kl, C)
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
        
        # Boucle d'adaptation endogene
        for step in range(self.max_compute):
            # 1. Inference (Coute du calcul)
            y_pred, hidden = self.model(x, hidden)
            
            # 2. Retrospection : Estimation de la viabilite
            with torch.no_grad():
                L, I_eff, D_kl, C = self.estimator.compute_metrics(y_pred, y_target, float(step + 1))
                metrics = torch.cat([I_eff, D_kl, torch.full_like(I_eff, float(step+1))], dim=-1)
            
            # 3. Decision du Controleur (RL)
            dist = self.controller(x, metrics)
            action = dist.sample() # 0 = Stop, 1 = Continue
            
            # On enregistre la probabilite pour le policy gradient
            log_probs.append(dist.log_prob(action))
            viability_history.append(L)
            
            # Mise a jour de qui doit continuer
            # Si action == 0 (Stop), on considere que le calcul est fini pour cet item
            force_stop = (action == 0)
            active_mask = active_mask & ~force_stop
            
            if not active_mask.any():
                break # Tout le monde a decide de s'arreter
                
        # --- PHASE D'APPRENTISSAGE (Mise a jour Ynor) ---
        # Le reward final est la viabilite L atteinte au moment de l'arret
        final_L, _, _, _ = self.estimator.compute_metrics(y_pred, y_target, compute_steps.float())
        
        # 1. Entrainement du modele (Supervise local pour maximiser l'information)
        loss_model = F.mse_loss(y_pred, y_target)
        self.optimizer_model.zero_grad()
        loss_model.backward(retain_graph=True)
        self.optimizer_model.step()
        
        # 2. Entrainement du Controleur (Reinforce algorithm pour maximiser S_Ynor)
        policy_loss = []
        for lp, v_reward in zip(log_probs, viability_history):
            # Le controleur apprend a favoriser les actions qui rapportent de la viabilite
            policy_loss.append(-lp * v_reward.detach().squeeze())
            
        policy_loss = torch.stack(policy_loss).sum()
        self.optimizer_ctrl.zero_grad()
        policy_loss.backward()
        self.optimizer_ctrl.step()
        
        return final_L.mean().item(), loss_model.item(), step + 1

# =====================================================================
# SIMULATION DE DEMONSTRATION
# =====================================================================
if __name__ == "__main__":
    print("\n Lancement du Prototype AGI Ynor V1")
    
    # Parametres arbitraires pour simulation
    INPUT_DIM = 10
    HIDDEN_DIM = 32
    OUTPUT_DIM = 5
    
    agi = YnorAGI(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM)
    
    print("\nDebut de l'entrainement (Optimisation de la Viabilite Globale)...")
    for epoch in range(1, 101):
        # Creation de taches aleatoires de difficulte variable
        x_batch = torch.randn(16, INPUT_DIM)
        # La cible est une fonction non-lineaire arbitraire (complexite cachee)
        y_target = torch.sin(x_batch[:, :OUTPUT_DIM]) * 2.0
        
        viability, error, avg_compute = agi.process_and_learn(x_batch, y_target)
        
        if epoch % 20 == 0:
            print(f"Epoque {epoch} | Viabilite (\u03bc): {viability:.4f} | Erreur: {error:.4f} | Profondeur moyenne de calcul (Cout): {avg_compute}")

    print("\n Simulation terminee. L'AGI a appris a auto-reguler son allocation de ressources !")

```