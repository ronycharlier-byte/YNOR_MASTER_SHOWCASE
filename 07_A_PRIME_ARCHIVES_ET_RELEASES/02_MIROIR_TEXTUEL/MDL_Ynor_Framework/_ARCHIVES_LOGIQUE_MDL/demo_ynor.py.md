# MIROIR TEXTUEL - demo_ynor.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\demo_ynor.py
Taille : 4233 octets
SHA256 : 5b88589eb85352fb8690803e69745bee70575c65941faeb85e61119225dc368b

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
from mdl_ynor_core import YnorSystem, check_viability_regime
from mdl_ynor_regimes import PostCriticalReconstructor

def run_demo():
    print("=====================================================")
    print("   DEMONSTRATION : THEORIE MDL YNOR ARCHITECTURE")
    print("=====================================================")
    print("Ce script démontre le comportement d'un système dissipatif")
    print("faisant face à une crise (mu < 0) et se reconstruisant.\n")

    # 1. Définition du système initialement instable (Chapitre I & II)
    dim = 2
    # Amplification forte
    E = lambda S: 1.5 * S
    # Dissipation faible (Système initialement voué à l'échec)
    D = lambda S: 0.5 * S
    
    sys = YnorSystem(dim, E, D)
    S0 = np.array([2.0, 2.0])
    
    mu_initial = sys.measure_dissipative_margin(S0)
    print(f"-> État Initial du Système : Marge estimée mu = {mu_initial:.2f}")
    print(f"-> Régime détecté : {check_viability_regime(mu_initial)}")
    print("-> ANOMALIE : Le système va diverger vers la destruction.\n")
    
    # Simulation de la phase 1 (chute)
    t_span_1 = (0, 3)
    t_eval_1 = np.linspace(0, 3, 50)
    res_1 = sys.simulate(S0, t_span_1, t_eval_1)
    
    energies_1 = [sys.energy(res_1.y[:, i]) for i in range(len(res_1.t))]
    
    # 2. Intervention du mécanisme de gouvernance post-critique (Chapitre VI)
    # L'état final de la phase 1 déclenche une crise.
    S_crisis = res_1.y[:, -1]
    print(f"-> TEMPS t=3 : Le système atteint l'état critique S={S_crisis}")
    
    reconstructor = PostCriticalReconstructor(sys, mutation_rate=2.5) # Booste la dissipation de +250%
    print("-> DÉCLENCHEMENT DE LA RECONSTRUCTION STRUCTURELLE...")
    
    if reconstructor.evaluate_and_reconstruct(S_crisis):
        print("-> MUTATION EFFECTUÉE : Capacité dissipative modifiée.")
    
    mu_post = sys.measure_dissipative_margin(S_crisis)
    print(f"-> Nouvel État du Système : Marge estimée mu = {mu_post:.2f}")
    print(f"-> Nouveau Régime : {check_viability_regime(mu_post)}\n")
    
    # Simulation de la phase 2 (reconstruction et stabilisation)
    t_span_2 = (3, 8)
    t_eval_2 = np.linspace(3, 8, 80)
    res_2 = sys.simulate(S_crisis, t_span_2, t_eval_2)
    
    energies_2 = [sys.energy(res_2.y[:, i]) for i in range(len(res_2.t))]
    
    # Concaténation des résultats pour l'affichage
    t_total = np.concatenate([res_1.t, res_2.t])
    e_total = np.concatenate([energies_1, energies_2])
    
    # 3. Épreuve de Validation (Chapitres XII et XIII)
    print("=====================================================")
    print("   VALIDATION FORMELLE (AUDIT DU CADRE)")
    print("=====================================================")
    if e_total[-1] < e_total[len(energies_1)-1]:
         print("-> RÉSULTAT DE L'AUDIT : [ACCEPT]")
         print("   Le système a réussi sa reconstruction post-critique.")
    else:
         print("-> RÉSULTAT DE L'AUDIT : [REJECT]")
         
    # 4. Tracé Graphique
    plt.figure(figsize=(10, 6))
    plt.plot(res_1.t, energies_1, 'r-', linewidth=2, label='Phase 1 : Instabilité (Amplification > Dissipation)')
    plt.plot(res_2.t, energies_2, 'g-', linewidth=2, label='Phase 2 : Reconstruction (Dissipation mutée)')
    
    plt.axvline(x=3, color='k', linestyle='--', label='Transition Critique (Mutation)')
    
    plt.yscale('log')
    plt.title("Dynamique de l'énergie systémique dans le cadre MDL Ynor")
    plt.xlabel("Temps (t)")
    plt.ylabel("Énergie Minimale $E_0(S)$ (log scale)")
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    
    output_filename = "demo_ynor_plot.png"
    plt.savefig(output_filename)
    print(f"\n-> Graphique de simulation enregistré sous : {output_filename}")


if __name__ == "__main__":
    run_demo()

```