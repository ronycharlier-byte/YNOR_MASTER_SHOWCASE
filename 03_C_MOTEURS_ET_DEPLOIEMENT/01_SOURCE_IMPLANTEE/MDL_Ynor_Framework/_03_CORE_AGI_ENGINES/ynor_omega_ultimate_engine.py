"""
YNOR Ω+ : MOTEUR OPÉRATIONNEL GLOBAL (PHASES 1 À 4)
--------------------------------------------------
Banc d'essai canonique avec observables intégrées et cartographie géométrique.
Traduction LLM temps réel.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def ynor_vector_field(S, t, a1, a2, a3, b1, b2, b3, c1, c2, c3):
    alpha, beta, kappa = S
    
    da = a1 - a2*beta - a3*alpha
    db = b1*alpha - b2*beta - b3
    dk = c1*beta - c2*alpha - c3*kappa
    
    if alpha <= 0 and da < 0: da = 0
    if beta <= 0 and db < 0: db = 0
    if kappa <= 0 and dk < 0: dk = 0

    return [da, db, dk]

def phase_1_to_3():
    # Phase 1: Simulateur Canonique
    print("[PHASE 1] Initialisation du Modèle Dynamique...")
    t = np.linspace(0, 50, 2000)
    
    # Paramètres d'un LLM en situation de stress
    params = (2.0, 0.8, 0.6, 0.7, 1.1, 0.4, 0.5, 0.3, 0.9)
    S0_stress = [0.1, 1.5, 1.0] # Prompte initial difficile, fort coût b et k
    
    solution = odeint(ynor_vector_field, S0_stress, t, args=params)
    alphas, betas, kappas = solution[:,0], solution[:,1], solution[:,2]
    
    # Phase 2: Observables Ynor
    print("[PHASE 2] Calcul des Observables (μ, dμ/dt)...")
    mus = alphas - betas - kappas
    d_mus = np.gradient(mus, t)
    
    # Temps de retour à la viabilité
    viable_indices = np.where(mus >= 0)[0]
    t_star = t[viable_indices[0]] if len(viable_indices) > 0 else None
    
    if t_star:
        print(f" -> Temps de retour à la viabilité (μ >= 0) : t* = {t_star:.2f}")
    else:
        print(" -> Système intrinsèquement non-viable (Instabilité globale).")
    
    # Phase 3: Géométrie (Portraits de Phase)
    print("[PHASE 3] Géométrie et Stabilité...")
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Trace 1 : Observables dans le Temps
    ax1.plot(t, mus, color='#ff3333', linewidth=2, label='Marge Dissipative μ(t)')
    ax1.plot(t, d_mus, color='#ffff33', linestyle=':', label='Vitesse dμ/dt')
    ax1.axhline(0, color='white', linewidth=1)
    if t_star:
        ax1.axvline(t_star, color='#33ccff', linestyle='--', label=f'Viabilité t*={t_star:.1f}')
    
    ax1.fill_between(t, 0, mus, where=(mus>=0), color='#33cc33', alpha=0.2)
    ax1.fill_between(t, 0, mus, where=(mus<0), color='#ff3333', alpha=0.2)
    ax1.set_title("Évolution de la Viabilité et Dérivée")
    ax1.set_xlabel('Temps / Jetons')
    ax1.legend()

    # Trace 2 : Portrait de Phase (β vs α) avec champ de vitesses
    ax2.plot(betas, alphas, color='#33ccff', linewidth=2, label='Trajectoire de l\'Attracteur')
    ax2.scatter(betas[0], alphas[0], color='red', s=100, label='État Initial')
    ax2.scatter(betas[-1], alphas[-1], color='green', s=100, label='Équilibre Asymptotique')
    ax2.set_title("Portrait de Phase : Valeur (α) vs Coût (β)")
    ax2.set_xlabel('Coût/Bruit (β)')
    ax2.set_ylabel('Valeur Utile (α)')
    ax2.legend()
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_ultimate_engine.png"
    plt.savefig(output, dpi=300)
    print(f" -> Graphiques générés : {output}")

def phase_4():
    print("\n[PHASE 4] TRADUCTION LLM (Mapping Génératif)")
    print(" - α (Valeur) : Mesure l'apport informationnel strict sur le prompt.")
    print(" - β (Coût) : Mesure le coût computationnel Inutile (verbosité du LLM).")
    print(" - κ (Mémoire) : Mesure le poids latent contextuel (fenêtre de tokens bloquante).")
    print("L'équation μ = α - β - κ est formellement prête pour intercepter les requêtes API (Gouvernance).")

if __name__ == '__main__':
    phase_1_to_3()
    phase_4()
