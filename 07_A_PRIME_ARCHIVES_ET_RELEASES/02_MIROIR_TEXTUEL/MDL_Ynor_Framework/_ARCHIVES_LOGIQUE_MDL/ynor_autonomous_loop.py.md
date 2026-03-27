# MIROIR TEXTUEL - ynor_autonomous_loop.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\ynor_autonomous_loop.py
Taille : 2330 octets
SHA256 : 1e884dae734446a4d93c0319664ae443f6d92cc8d7b8df0825eade9ded828d44

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import get_ai_reconstruction_strategy

def autonomous_system_loop():
    print("=====================================================")
    print("   GOUVERNANCE AUTONOME MDL YNOR (COCKPIT IA)")
    print("=====================================================\n")

    # Système initial (Instable : E > D)
    dim = 2
    E = lambda S: 1.5 * S  # beta ≈ 1.5
    D = lambda S: 0.5 * S  # alpha ≈ 0.5
    S = np.array([2.0, 2.0])
    
    sys = YnorSystem(dim, E, D)
    
    t = 0.0
    dt = 0.5
    
    print(f"Lancement de la surveillance autonome sur 20 cycles...")
    print("-" * 60)

    for _ in range(20):
        mu = sys.measure_dissipative_margin(S)
        regime = check_viability_regime(mu)
        
        print(f"t={t:<4.1f} | mu={mu:<5.2f} | {regime:<10} | Etat={S}")
        
        # SI LE SYSTÈME ENTRE EN CRISE (mu <= 0)
        if mu <= 0.0:
            print("\n[CRISE DÉTECTÉE] ALARME ROUGE : µ = " + str(mu))
            
            # APPEL À L'AGENCE DE GOUVERNANCE IA (OpenAI)
            strategy = get_ai_reconstruction_strategy(mu, S.tolist())
            
            r = strategy["mutation_rate"]
            desc = strategy["explanation"]
            
            print(f"[MUTATION IA] Taux appliqué : +{r*100}%")
            print(f"[EXPLICATION] : {desc}")
            
            # APPLICATION DE LA MUTATION STRUCTURELLE
            old_D = sys.D
            # Nouveau D boosté par l'IA
            sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
            
            print("[SYSTÈME RECONSTRUIT] Continuité de la simulation...\n")
            
        # Evolution
        S_dot = sys.dynamics(t, S)
        S = S + S_dot * dt
        t += dt
        time.sleep(0.3)

    print("\nSimulation Autonome terminée.")

if __name__ == "__main__":
    autonomous_system_loop()

```