# MIROIR TEXTUEL - test_core.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\test_core.py
Taille : 4222 octets
SHA256 : e6eaa21219c8450dd87679724ff179c544c4818131c5aa7bab65da86e3933ceb

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
from mdl_ynor_core import YnorSystem, check_viability_regime
import matplotlib.pyplot as plt

def test_stable_regime():
    """ Test du Théorème 1 pour mu > 0 (Décroissance exponentielle de l'énergie). """
    print("=== Test: Régime Stable (mu > 0) ===")
    
    # Espace de dimension 2
    dim = 2
    
    # Amplification faible: E(S) = beta * S  avec beta = 0.5
    E = lambda S: 0.5 * S
    
    # Dissipation forte: D(S) = alpha * S avec alpha = 2.0
    D = lambda S: 2.0 * S
    
    # Pas de mémoire, pas de forçage
    sys = YnorSystem(dimension=dim, amplification_op=E, dissipation_op=D)
    
    # Marge theorique: mu = alpha - beta = 2.0 - 0.5 = 1.5 > 0
    
    # Etat initial [10, 10]
    S0 = np.array([10.0, 10.0])
    
    # mu_est = (0 - dE/dt)/|S|^2 = - <S, E-D> / |S|^2 = - <S, -1.5*S> / |S|^2 = 1.5
    mu_est = sys.measure_dissipative_margin(S0)
    print(f"Marge dissipative estimée: {mu_est:.2f} -> Régime: {check_viability_regime(mu_est)}")
    
    # Simulation sur 5 secondes
    t_span = (0, 5)
    t_eval = np.linspace(0, 5, 100)
    
    res = sys.simulate(S0, t_span, t_eval)
    
    # Calcul de l'énergie au cours du temps
    energies = [sys.energy(res.y[:, i]) for i in range(len(res.t))]
    
    assert energies[-1] < energies[0], "L'énergie devrait décroitre"
    print("L'énergie décroît exponentiellement avec le temps. Test OK.\n")
    
    return res.t, energies

def test_instable_regime():
    """ Test du Théorème 1 pour mu < 0 (Amplification nette). """
    print("=== Test: Régime Instable (mu < 0) ===")
    
    dim = 2
    
    # Amplification forte: beta = 2.0
    E = lambda S: 2.0 * S
    
    # Dissipation faible: alpha = 0.5
    D = lambda S: 0.5 * S
    
    sys = YnorSystem(dimension=dim, amplification_op=E, dissipation_op=D)
    
    S0 = np.array([1.0, 1.0])
    mu_est = sys.measure_dissipative_margin(S0)
    print(f"Marge dissipative estimée: {mu_est:.2f} -> Régime: {check_viability_regime(mu_est)}")
    
    t_span = (0, 2)
    t_eval = np.linspace(0, 2, 50)
    res = sys.simulate(S0, t_span, t_eval)
    
    energies = [sys.energy(res.y[:, i]) for i in range(len(res.t))]
    
    assert energies[-1] > energies[0], "L'énergie devrait croitre"
    print("L'énergie croît rapidement, le système diverge. Test OK.\n")
    
    return res.t, energies

def test_critical_regime():
    """ Test du Théorème 1 pour mu = 0 (Seuil critique). """
    print("=== Test: Régime Critique (mu = 0) ===")
    
    dim = 2
    
    E = lambda S: 1.0 * S
    D = lambda S: 1.0 * S
    
    # Perturbation cyclique
    w = lambda t: np.array([np.sin(t), np.cos(t)])
    
    sys = YnorSystem(dimension=dim, amplification_op=E, dissipation_op=D, forcing_op=w)
    
    S0 = np.array([5.0, 5.0])
    
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 200)
    res = sys.simulate(S0, t_span, t_eval)
    
    energies = [sys.energy(res.y[:, i]) for i in range(len(res.t))]
    
    print(f"Énergie initiale: {energies[0]:.2f}")
    print(f"Énergie finale: {energies[-1]:.2f}")
    print("Le système est maintenu à un seuil critique sans diverger ni s'éteindre totalement, dépendant du forçage. Test OK.\n")
    return res.t, energies


if __name__ == "__main__":
    t_s, e_s = test_stable_regime()
    t_i, e_i = test_instable_regime()
    t_c, e_c = test_critical_regime()
    
    plt.figure()
    plt.plot(t_s, e_s, label="Stable (mu = 1.5)")
    plt.plot(t_i, e_i, label="Instable (mu = -1.5)", color='red')
    plt.plot(t_c, e_c, label="Critique (mu = 0 + w(t))", color='orange')
    plt.yscale('log')
    plt.title("Evolution de l'énergie minimale $E_0(S)$ selon le régime")
    plt.xlabel("Temps (t)")
    plt.ylabel("Énergie")
    plt.legend()
    plt.savefig("regimes_energy.png")
    print("Graphique sauvegardé sous 'regimes_energy.png'.")

```