# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import time
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import get_ai_reconstruction_strategy

class YnorResilienceExploitation:
    """
    Test de rsilience face  des chocs externes et de l'inertie structurelle.
    """
    def __init__(self):
        # On dfinit un choc externe  t=2.0
        def w_forcing(t):
            if 2.0 <= t <= 2.5:
                # Injection massive d'anomalie sur le premier canal
                return np.array([20.0, 0.0])
            return np.zeros(2)

        # On dfinit une mmoire structurelle (Inertie kappa)
        # La mmoire tend  conserver l'tat prcdent (rsistance au changement)
        def memory_inertia(S, t):
            # Le systme "pousse" contre la drive pour rester sur place
            return -0.2 * S 

        # Systme Principal avec Forage et Mmoire
        self.sys = YnorSystem(2, 
            amplification_op=lambda S: 1.2 * S, 
            dissipation_op=lambda S: 1.0 * S,
            memory_op=memory_inertia,
            forcing_op=w_forcing
        )
        
        self.S = np.array([1.0, 1.0])

    def run(self):
        print("=====================================================")
        print("   TEST DE RSILIENCE : CHOC EXTERNE ET INERTIE (KAPPA)")
        print("=====================================================\n")

        t = 0.0
        dt = 0.1
        history_energy = []
        timestamps = []
        
        print(f"Lancement du test. Choc prvu  t=2.0...")
        print("-" * 60)

        for step in range(80):
            energy = self.sys.energy(self.S)
            history_energy.append(energy)
            timestamps.append(t)
            
            mu = self.sys.measure_dissipative_margin(self.S)
            regime = check_viability_regime(mu)
            
            # Affichage priodique
            if step % 5 == 0 or mu <= 0.0:
                 print(f"t={t:<4.1f} | mu={mu:<6.2f} | Energy={energy:<8.2f} | Status={regime}")
            
            # GOUVERNANCE IA : Raction d'urgence
            if mu <= 0.0:
                print(f"\n[ALERTE CHOC] Rupture dtecte ! Intervention IA immdiate...")
                # L'IA doit donner une mutation qui domine  la fois l'amplification ET le choc externe
                strategy = get_ai_reconstruction_strategy(mu, self.S.tolist())
                r = strategy["mutation_rate"]
                
                # Mutation dcisive
                old_D = self.sys.D
                self.sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
                print(f"[IA] Mutation d'absorption applique (+{r*100}% de dissipation).\n")

            # Simulation pas  pas
            S_dot = self.sys.dynamics(t, self.S)
            self.S = self.S + S_dot * dt
            t += dt

        self.plot_results(timestamps, history_energy)

    def plot_results(self, t, e):
        plt.figure(figsize=(10, 6))
        plt.plot(t, e, 'r-', linewidth=2, label="Densit d'nergie (S)")
        plt.axvspan(2.0, 2.5, color='orange', alpha=0.3, label="Zone de Choc Externe (w)")
        plt.yscale('log')
        plt.title("Rsilience MDL Ynor : Survie face  une Injection d'Anomalie")
        plt.xlabel("Temps (t)")
        plt.ylabel("nergie $(\log)$")
        plt.grid(True, which="both", ls="--", alpha=0.5)
        plt.legend()
        
        file_name = "ynor_resilience_audit.png"
        plt.savefig(file_name)
        print(f"\n[OK] Audit de rsilience gnr : {file_name}")

if __name__ == "__main__":
    app = YnorResilienceExploitation()
    app.run()



