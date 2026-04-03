# MIROIR TEXTUEL - ynor_omega_phase_space_simulator.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\ynor_omega_phase_space_simulator.py
Taille : 4443 octets
SHA256 : 6881665074084ead2d9fcc40eee92bc02948d7c40e17afe6994dbc2c7a5ab8d7

```text
"""
YNOR OMEGA (Ω) - SIMULATEUR DYNAMIQUE CANONIQUE
Espace d'état : S = (alpha, beta, kappa) ∈ R³_≥0
Marge dissipative : mu = alpha - (beta + kappa)
Régime de gouvernance fermé.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# Paramètres de dynamique
class YnorOmegaSystem:
    def __init__(self, alpha_0=0.1, beta_0=0.01, kappa_0=0.0):
        self.alpha = alpha_0
        self.beta = beta_0
        self.kappa = kappa_0
        self.history = []
        self._record_state()

    def _record_state(self):
        mu = self.alpha - self.beta - self.kappa
        self.history.append((self.alpha, self.beta, self.kappa, mu))

    def step(self, F_alpha, F_beta, F_kappa):
        # Dynamique discrète (S_n+1 = T(S_n, e_n))
        self.alpha += F_alpha
        self.beta += F_beta
        self.kappa += F_kappa
        self._record_state()
        return self.mu()

    def mu(self):
        return self.alpha - self.beta - self.kappa

def simulate_llm_generation():
    sys = YnorOmegaSystem()
    print("=========================================================")
    print("DÉMARRAGE SIMULATION YNOR Ω (Fermeture Structurelle)")
    print("Espace d'état : X = R^3_>=0")
    print("Surface Critique : Σ = {(α,β,κ) ∈ X : α - β - κ = 0}")
    print("=========================================================\n")
    
    n_steps = 50
    
    for n in range(n_steps):
        # FORME EXPLICITE DU CHAMP VECTORIEL F(S, e_n)
        # Simulation d'une génération textuelle (LLM):
        # 1. Le gain d'information (alpha) ralentit avec la longueur (rendement décroissant)
        F_alpha = 0.6 * np.exp(-0.15 * n)
        
        # 2. Le coût de structure / verbosité (beta) augmente progressivement
        F_beta = 0.05 + 0.01 * n
        
        # 3. La surcharge mnésique (kappa) s'accumule proportionnellement à alpha
        F_kappa = 0.03 * sys.alpha
        
        mu_current = sys.mu()
        mu_next = sys.step(F_alpha, F_beta, F_kappa)
        
        print(f"Étape {n:02d} | α={sys.alpha:.2f}, β={sys.beta:.2f}, κ={sys.kappa:.2f} | μ={mu_next:.3f}")
        
        # LOI DE GOUVERNANCE CANONIQUE D'ARRÊT
        if mu_next <= 0:
            print(f"\n[!] ARRÊT FORMEL (μ <= 0).")
            print(f"Le système a franchi la surface critique Σ.")
            print(f"Bifurcation dissipative atteinte. Arrêt à l'étape {n}.")
            break
        
        # Règle d'arrêt préventif (Dérive de la marge)
        if (mu_next - mu_current) < -0.15 and mu_next < 0.2:
            print(f"\n[!] ARRÊT DE PRÉCAUTION (Dérive dissipative).")
            print(f"dμ/dt s'effondre de manière persistante.")
            break

    # Construction du graphe de l'Espace de Phase
    alphas = [s[0] for s in sys.history]
    betas = [s[1] for s in sys.history]
    kappas = [s[2] for s in sys.history]
    mus = [s[3] for s in sys.history]

    plt.figure(figsize=(10,6), facecolor="#0e1117")
    ax = plt.axes()
    ax.set_facecolor("#0e1117")
    
    plt.plot(mus, label='Marge μ (Viabilité)', color='#ff3333', linewidth=3)
    plt.plot(alphas, label='α (Valeur logic)', color='#33ccff', linestyle='--', linewidth=2)
    plt.plot(betas, label='β (Coût / Bruit)', color='#ff9933', linestyle='--', linewidth=2)
    plt.plot(kappas, label='κ (Mémoire)', color='#cc33ff', linestyle='--', linewidth=2)
    
    plt.axhline(0, color='white', linewidth=1.5, linestyle=":")
    plt.fill_between(range(len(mus)), 0, mus, where=(np.array(mus)>0), color='#33cc33', alpha=0.1, label='Zone Viable')
    plt.fill_between(range(len(mus)), 0, mus, where=(np.array(mus)<0), color='#ff3333', alpha=0.1, label='Zone Non Viable')
    
    plt.title("Dynamique Ynor Ω - Trajectoire vers la Surface Critique", color="white")
    plt.xlabel("Étapes (Tokens / Générations)", color="white")
    plt.ylabel("Amplitudes (α, β, κ)", color="white")
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.legend(facecolor="#1a1c24", edgecolor="none", labelcolor="white")
    plt.grid(True, alpha=0.2, color="white")
    
    output_path = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_phase_space.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"\nGraphique topologique sauvegardé: {output_path}")

if __name__ == '__main__':
    simulate_llm_generation()

```