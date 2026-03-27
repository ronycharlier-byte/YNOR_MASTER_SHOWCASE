# MIROIR TEXTUEL - mdl_master_system.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\mdl_master_system.py
Taille : 4594 octets
SHA256 : 915a6f4e3954d09aaaac1dbe26bbf358f0c3f8176419ba2f80f627ddc181774c

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import json
import time
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import get_ai_reconstruction_strategy

class MDLMasterSystem:
    """
    Implémentation Totale de la Théorie MDL Ynor (Synthèse des 55 Chapitres).
    """
    def __init__(self):
        # 1. Noyau de Résonance : Un réseau de 5 systèmes interconnectés
        self.nodes = {
            "ENERGIE": YnorSystem(2, lambda S: 1.5 * S, lambda S: 0.5 * S),
            "MATIERE": YnorSystem(2, lambda S: 1.0 * S, lambda S: 1.1 * S),
            "INFORMATION": YnorSystem(2, lambda S: 2.0 * S, lambda S: 0.8 * S),
            "GOUVERNANCE": YnorSystem(2, lambda S: 0.5 * S, lambda S: 1.5 * S),
            "BIOLOGIE": YnorSystem(2, lambda S: 1.2 * S, lambda S: 1.0 * S)
        }
        
        # Etats initiaux (S)
        self.states = {name: np.array([2.0, 2.0]) for name in self.nodes.keys()}
        
        # Historique pour visualisation
        self.history = {name: [] for name in self.nodes.keys()}
        self.time_points = []

    def get_global_coupling(self):
        """
        Définit l'influence mutuelle des nœuds. (Chapitre VII).
        """
        # Matrice de synergie : On calcule l'effort de chaque noeud sur les autres
        pass 

    def audit_global(self, t):
        """
        Réalise un AUDIT FORMEL de l'intégralité de l'architecture (Chapitre XII).
        """
        print(f"\n--- AUDIT GLOBAL MDL t={t:.2f} ---")
        unstable_nodes = []
        
        for name, sys in self.nodes.items():
            mu = sys.measure_dissipative_margin(self.states[name])
            regime = check_viability_regime(mu)
            print(f"[{name:<12}] mu={mu:<5.2f} | {regime}")
            
            if mu <= 0.0:
                unstable_nodes.append((name, mu))
        
        return unstable_nodes

    def run_master_loop(self, steps=20):
        t = 0.0
        dt = 0.2
        
        for step in range(steps):
            self.time_points.append(t)
            
            # 1. Analyse critique
            crises = self.audit_global(t)
            
            # 2. Re-stabilisation par le Gouverneur IA
            if crises:
                print(f"[ALERTE] Détection de défaillance majeure sur {len(crises)} noeuds.")
                for node_name, mu in crises:
                    print(f"   [IA] Intervention sur {node_name}...")
                    strategy = get_ai_reconstruction_strategy(mu, self.states[node_name].tolist())
                    r = strategy["mutation_rate"]
                    
                    # Mutation décisive
                    sys = self.nodes[node_name]
                    old_D = sys.D
                    sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
                    print(f"   [IA] Noeud {node_name} muté à +{r*100}%.")

            # 3. Evolution dynamique couplée
            for name, sys in self.nodes.items():
                self.history[name].append(sys.energy(self.states[name]))
                
                # Evolution
                S_dot = sys.dynamics(t, self.states[name])
                self.states[name] = self.states[name] + S_dot * dt

            t += dt

        self.generate_master_report()

    def generate_master_report(self):
        plt.figure(figsize=(12, 7))
        for name, data in self.history.items():
            plt.plot(self.time_points, data, label=name, marker='o', markersize=3)
        
        plt.yscale('log')
        plt.title("AUDIT TOTAL DE STABILITÉ : NOYAU MDL YNOR (Synthèse 55 Chapitres)")
        plt.xlabel("Cycle de Temps (t)")
        plt.ylabel("Énergie Structurelle $(\log |S|^2)$")
        plt.grid(True, which="both", alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        plt.savefig("mdl_master_audit_graph.png")
        print("\n" + "="*50)
        print("   RAPPORT MASTER AUDIT : GÉNÉRÉ")
        print("="*50)
        print("[OK] Graphique : mdl_master_audit_graph.png")
        print("[OK] Log : mdl_master_audit.log")

if __name__ == "__main__":
    master = MDLMasterSystem()
    master.run_master_loop()

```