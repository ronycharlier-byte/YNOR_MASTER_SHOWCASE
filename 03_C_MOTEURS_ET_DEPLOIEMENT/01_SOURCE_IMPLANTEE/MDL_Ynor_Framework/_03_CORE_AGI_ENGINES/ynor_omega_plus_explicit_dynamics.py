"""
YNOR Ω+ : FORMALISATION DYNAMIQUE EXPLICITE
Simulateur Numérique du Système Dynamique Génératif.

Système d'Équations Différentielles (Couplage α, β, κ) :
dα/dt = a1 - a2*β
dβ/dt = b1*α - b2
dκ/dt = c1*β - c2*α
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import odeint
import os

# Paramètres du système Ynor Ω+
# Pour un système possédant un attracteur viable, on choisit les constantes:
a1, a2 = 0.5, 0.1   # La verbosité (β) freine la création de valeur (α)
b1, b2 = 0.2, 0.4   # La valeur (α) exige un coût mathématique/structurel pour croître
c1, c2 = 0.3, 0.1   # La verbosité s'accumule en mémoire, l'information pure la nettoie

def ynor_vector_field(S, t):
    alpha, beta, kappa = S
    
    # Dynamique Réelle
    d_alpha = a1 - a2 * beta
    d_beta  = b1 * alpha - b2
    d_kappa = c1 * beta - c2 * alpha
    
    # Contrainte de positivité de l'Espace de Phase X = R^3_>=0
    if alpha <= 0 and d_alpha < 0: d_alpha = 0
    if beta <= 0 and d_beta < 0: d_beta = 0
    if kappa <= 0 and d_kappa < 0: d_kappa = 0
        
    return [d_alpha, d_beta, d_kappa]

def run_omega_plus_simulation():
    print("=====================================================")
    print(" YNOR Ω+ : Lancement du Simulateur Dynamique Continu")
    print("=====================================================")
    
    # Point d'équilibre théorique (Point Critique):
    alpha_star = b2 / b1
    beta_star = a1 / a2
    print(f"\n[ÉQUILIBRE ANALYTIQUE]")
    print(f"α* = {alpha_star:.2f}, β* = {beta_star:.2f}")
    
    # Temps continu
    t = np.linspace(0, 50, 1000)
    
    # Conditions initiales (Prompt LLM initial)
    S0 = [0.1, 0.1, 0.0]
    
    # Intégration du Flot de Gradient / Champ de Vecteur
    solution = odeint(ynor_vector_field, S0, t)
    
    alphas = solution[:, 0]
    betas  = solution[:, 1]
    kappas = solution[:, 2]
    mus    = alphas - betas - kappas
    
    # Trouver le moment de la bifurcation (mu passe < 0)
    stop_idx = len(t)
    for i, mu in enumerate(mus):
        if mu <= 0:
            stop_idx = i
            print(f"\n[!] BIFURCATION DISSIPATIVE ATTEINTE.")
            print(f"La trajectoire traverse la surface critique Σ (μ=0) à t={t[i]:.2f}.")
            print(f"État critique : α={alphas[i]:.2f}, β={betas[i]:.2f}, κ={kappas[i]:.2f}")
            break
    
    # --- VISUALISATION TOPOLOGIQUE 2D ---
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(12, 8))
    
    ax1 = fig.add_subplot(211)
    ax1.plot(t[:stop_idx], mus[:stop_idx], color='#ff3333', linewidth=3, label='Marge viabilité μ(t)')
    ax1.plot(t[:stop_idx], alphas[:stop_idx], color='#33ccff', linestyle='--', label='α(t) Valeur')
    ax1.plot(t[:stop_idx], betas[:stop_idx], color='#ff9933', linestyle='--', label='β(t) Coût')
    ax1.plot(t[:stop_idx], kappas[:stop_idx], color='#cc33ff', linestyle='--', label='κ(t) Mémoire')
    ax1.axhline(0, color='white', linestyle=':')
    ax1.set_title("Évolution Temporelle des Paramètres d'État Ynor Ω+")
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.2)
    
    # --- VISUALISATION PHASE SPACE 3D ---
    ax2 = fig.add_subplot(212, projection='3d')
    # Trajectoire viable
    ax2.plot(alphas[:stop_idx], betas[:stop_idx], kappas[:stop_idx], color='#00ff00', linewidth=2, label='Trajectoire Viable (μ > 0)')
    # Trajectoire non viable (fantomatique)
    if stop_idx < len(t):
        ax2.plot(alphas[stop_idx:], betas[stop_idx:], kappas[stop_idx:], color='#ff0000', linewidth=2, alpha=0.3, label='Dérive Non Viable (μ < 0)')
    
    # Surface Critique Mu = 0 (alpha = beta + kappa)
    A_grid, B_grid = np.meshgrid(np.linspace(0, max(alphas), 10), np.linspace(0, max(betas), 10))
    K_grid = A_grid - B_grid
    K_grid[K_grid < 0] = np.nan # On ne plotte que kappa >= 0
    ax2.plot_surface(A_grid, B_grid, K_grid, color='cyan', alpha=0.1)
    
    ax2.set_xlabel('α (Valeur)')
    ax2.set_ylabel('β (Coût)')
    ax2.set_zlabel('κ (Mémoire)')
    ax2.set_title("Espace de Phase 3D & Surface Critique Σ")
    ax2.legend()
    
    plt.tight_layout()
    output_path = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_plus_phase_space.png"
    plt.savefig(output_path, dpi=300)
    print(f"\n[OK] Topologie 3D sauvegardée sous: {output_path}")

if __name__ == '__main__':
    run_omega_plus_simulation()
