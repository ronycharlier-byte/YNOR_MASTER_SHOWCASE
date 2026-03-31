"""
YNOR OMEGA (I) - SIMULATEUR DYNAMIQUE CANONIQUE
Espace d'Atat : S = (alpha, beta, kappa) a RA_a0
Marge dissipative : mu = Alpha - (Beta + Kappa)
RAgime de gouvernance fermA.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ParamAtres de dynamique
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
        # Dynamique discrAte (S_n+1 = T(S_n, e_n))
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
    print("DAMARRAGE SIMULATION YNOR I (Fermeture Structurelle)")
    print("Espace d'Atat : X = R^3_>=0")
    print("Surface Critique : I = {(I,I,I) a X : I - I - I = 0}")
    print("=========================================================\n")
    
    n_steps = 50
    
    for n in range(n_steps):
        # FORME EXPLICITE DU CHAMP VECTORIEL F(S, e_n)
        # Simulation d'une gAnAration textuelle (LLM):
        # 1. Le gain d'information (alpha) ralentit avec la longueur (rendement dAcroissant)
        F_alpha = 0.6 * np.exp(-0.15 * n)
        
        # 2. Le coAt de structure / verbositA (beta) augmente progressivement
        F_beta = 0.05 + 0.01 * n
        
        # 3. La surcharge mnAsique (kappa) s'accumule proportionnellement A alpha
        F_kappa = 0.03 * sys.alpha
        
        mu_current = sys.mu()
        mu_next = sys.step(F_alpha, F_beta, F_kappa)
        
        print(f"Atape {n:02d} | I={sys.alpha:.2f}, I={sys.beta:.2f}, I={sys.kappa:.2f} | I={mu_next:.3f}")
        
        # LOI DE GOUVERNANCE CANONIQUE D'ARRAST
        if mu_next <= 0:
            print(f"\n[!] ARRAST FORMEL (I <= 0).")
            print(f"Le systAme a franchi la surface critique I.")
            print(f"Bifurcation dissipative atteinte. ArrAt A l'Atape {n}.")
            break
        
        # RAgle d'arrAt prAventif (DArive de la marge)
        if (mu_next - mu_current) < -0.15 and mu_next < 0.2:
            print(f"\n[!] ARRAST DE PRACAUTION (DArive dissipative).")
            print(f"dI/dt s'effondre de maniAre persistante.")
            break

    # Construction du graphe de l'Espace de Phase
    alphas = [s[0] for s in sys.history]
    betas = [s[1] for s in sys.history]
    kappas = [s[2] for s in sys.history]
    mus = [s[3] for s in sys.history]

    plt.figure(figsize=(10,6), facecolor="#0e1117")
    ax = plt.axes()
    ax.set_facecolor("#0e1117")
    
    plt.plot(mus, label='Marge I (ViabilitA)', color='#ff3333', linewidth=3)
    plt.plot(alphas, label='I (Valeur logic)', color='#33ccff', linestyle='--', linewidth=2)
    plt.plot(betas, label='I (CoAt / Bruit)', color='#ff9933', linestyle='--', linewidth=2)
    plt.plot(kappas, label='I (MAmoire)', color='#cc33ff', linestyle='--', linewidth=2)
    
    plt.axhline(0, color='white', linewidth=1.5, linestyle=":")
    plt.fill_between(range(len(mus)), 0, mus, where=(np.array(mus)>0), color='#33cc33', alpha=0.1, label='Zone Viable')
    plt.fill_between(range(len(mus)), 0, mus, where=(np.array(mus)<0), color='#ff3333', alpha=0.1, label='Zone Non Viable')
    
    plt.title("Dynamique Ynor I - Trajectoire vers la Surface Critique", color="white")
    plt.xlabel("Atapes (Tokens / GAnArations)", color="white")
    plt.ylabel("Amplitudes (I, I, I)", color="white")
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.legend(facecolor="#1a1c24", edgecolor="none", labelcolor="white")
    plt.grid(True, alpha=0.2, color="white")
    
    output_path = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_phase_space.png"
    plt.savefig(output_path, bbox_inches='tight')
    print(f"\nGraphique topologique sauvegardA: {output_path}")

if __name__ == '__main__':
    simulate_llm_generation()

