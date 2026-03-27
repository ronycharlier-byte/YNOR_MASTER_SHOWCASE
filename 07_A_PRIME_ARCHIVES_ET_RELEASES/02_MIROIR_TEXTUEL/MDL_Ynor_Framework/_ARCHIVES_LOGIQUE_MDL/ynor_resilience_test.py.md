# MIROIR TEXTUEL - ynor_resilience_test.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\ynor_resilience_test.py
Taille : 4053 octets
SHA256 : 721653dbe1c53f2a68752dc36d8368183d71e8f2c4b4c5fd2b0c3ad2af45734d

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import time
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import get_ai_reconstruction_strategy

class YnorResilienceExploitation:
    """
    Test de résilience face à des chocs externes et de l'inertie structurelle.
    """
    def __init__(self):
        # On définit un choc externe à t=2.0
        def w_forcing(t):
            if 2.0 <= t <= 2.5:
                # Injection massive d'anomalie sur le premier canal
                return np.array([20.0, 0.0])
            return np.zeros(2)

        # On définit une mémoire structurelle (Inertie kappa)
        # La mémoire tend à conserver l'état précédent (résistance au changement)
        def memory_inertia(S, t):
            # Le système "pousse" contre la dérivée pour rester sur place
            return -0.2 * S 

        # Système Principal avec Forçage et Mémoire
        self.sys = YnorSystem(2, 
            amplification_op=lambda S: 1.2 * S, 
            dissipation_op=lambda S: 1.0 * S,
            memory_op=memory_inertia,
            forcing_op=w_forcing
        )
        
        self.S = np.array([1.0, 1.0])

    def run(self):
        print("=====================================================")
        print("   TEST DE RÉSILIENCE : CHOC EXTERNE ET INERTIE (KAPPA)")
        print("=====================================================\n")

        t = 0.0
        dt = 0.1
        history_energy = []
        timestamps = []
        
        print(f"Lancement du test. Choc prévu à t=2.0...")
        print("-" * 60)

        for step in range(80):
            energy = self.sys.energy(self.S)
            history_energy.append(energy)
            timestamps.append(t)
            
            mu = self.sys.measure_dissipative_margin(self.S)
            regime = check_viability_regime(mu)
            
            # Affichage périodique
            if step % 5 == 0 or mu <= 0.0:
                 print(f"t={t:<4.1f} | mu={mu:<6.2f} | Energy={energy:<8.2f} | Status={regime}")
            
            # GOUVERNANCE IA : Réaction d'urgence
            if mu <= 0.0:
                print(f"\n[ALERTE CHOC] Rupture détectée ! Intervention IA immédiate...")
                # L'IA doit donner une mutation qui domine à la fois l'amplification ET le choc externe
                strategy = get_ai_reconstruction_strategy(mu, self.S.tolist())
                r = strategy["mutation_rate"]
                
                # Mutation décisive
                old_D = self.sys.D
                self.sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
                print(f"[IA] Mutation d'absorption appliquée (+{r*100}% de dissipation).\n")

            # Simulation pas à pas
            S_dot = self.sys.dynamics(t, self.S)
            self.S = self.S + S_dot * dt
            t += dt

        self.plot_results(timestamps, history_energy)

    def plot_results(self, t, e):
        plt.figure(figsize=(10, 6))
        plt.plot(t, e, 'r-', linewidth=2, label="Densité d'énergie (S)")
        plt.axvspan(2.0, 2.5, color='orange', alpha=0.3, label="Zone de Choc Externe (w)")
        plt.yscale('log')
        plt.title("Résilience MDL Ynor : Survie face à une Injection d'Anomalie")
        plt.xlabel("Temps (t)")
        plt.ylabel("Énergie $(\log)$")
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.legend()
        
        file_name = "ynor_resilience_audit.png"
        plt.savefig(file_name)
        print(f"\n[OK] Audit de résilience généré : {file_name}")

if __name__ == "__main__":
    app = YnorResilienceExploitation()
    app.run()

```