# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime

def monitor_system():
    print("=====================================================")
    print("   MONITEUR EN TEMPS REL : MDL YNOR ARCHITECTURE")
    print("=====================================================\n")

    # Configuration du systme (similaire  demo_ynor.py)
    dim = 2
    E = lambda S: 1.5 * S  # Forte amplification
    D = lambda S: 0.5 * S  # Faible dissipation
    S = np.array([2.0, 2.0]) # tat de dpart normal
    
    sys = YnorSystem(dim, E, D)
    
    dt = 0.5  # Intervalle de lecture
    t = 0.0
    
    print(f"{'Temps':<10} | {'Mu ()':<10} | {'Rgime':<10} | {'Statut'}")
    print("-" * 50)

    try:
        while t < 10.0:
            mu = sys.measure_dissipative_margin(S)
            regime = check_viability_regime(mu)
            
            status = "OK" if mu > 0.01 else "!!! ALARME CRITIQUE !!!"
            
            print(f"{t:<10.1f} | {mu:<10.2f} | {regime:<10} | {status}")
            
            if mu <= 0.01:
                trigger_emergency_alert(t, S, mu)
                break # On arrte pour rparation
                
            # Faire voluer le systme (Euler simple pour la dmo de monitoring)
            S_dot = sys.dynamics(t, S)
            S = S + S_dot * dt
            t += dt
            time.sleep(0.2) # Ralentir pour l'aspect "temps rel"

    except KeyboardInterrupt:
        print("\nSurveillance interrompue par l'utilisateur.")

def trigger_emergency_alert(t, S, mu):
    print("\n" + "#" * 50)
    print("         ALERTE DE RUPTURE DISSIPATIVE")
    print("#" * 50)
    
    crisis_report = {
        "event": "CRITICAL_THRESHOLD_EXCEEDED",
        "time": t,
        "mu": float(mu),
        "state": S.tolist(),
        "recommendation": "Requrir une mutation immdiate de l'oprateur D."
    }
    
    # Sauvegarde du rapport de crise
    with open("ynor_crisis_log.json", "w") as f:
        json.dump(crisis_report, f, indent=4)
        
    print(f"\n[URGENT] Le systme a franchi le seuil critique  t={t:.1f}")
    print(f"Copiez ce JSON dans ChatGPT pour une stratgie de reconstruction :")
    print(f"```json\n{json.dumps(crisis_report, indent=2)}\n```")
    print("\n" + "#" * 50)

if __name__ == "__main__":
    monitor_system()



