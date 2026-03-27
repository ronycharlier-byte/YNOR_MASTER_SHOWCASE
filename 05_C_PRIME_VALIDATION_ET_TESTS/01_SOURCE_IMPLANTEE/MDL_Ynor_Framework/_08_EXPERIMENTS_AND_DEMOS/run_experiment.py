# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# MDL YNOR - RUN EXPERIMENT (REPRODUCIBLE RESEARCH)
# Fixed seeds & numerical outputs for the final benchmark.
# =============================================================================
import numpy as np
import time
from _04_DEPLOYMENT_AND_API.ynor_core.engine import YnorSystem

def run_experiment_01(seed=101):
    \"\"\"Simule une mutation AGI en réponse à une chute de mu.\"\"\"
    np.random.seed(seed)
    print(f"🔬 [EXPÉRIENCE] Lancement de l'expérience #01 (Seed: {seed})")
    
    # 1. Système initialement instable (D < E)
    E = lambda S: 1.5 * S
    D = lambda S: 0.5 * S
    sys = YnorSystem(dim=2, amplification_op=E, dissipation_op=D)
    
    S0 = np.array([1.0, 1.0])
    mu_initial = sys.measure_dissipative_margin(S0)
    print(f"   ETAT INITIAL  | mu = {mu_initial:.2f} (CRITICAL: µ <= 0)")

    # 2. Simulation de la mutation structurelle (AGI INNOVATION)
    # L'IA augmente le facteur de dissipation pour stabiliser.
    D_mutated = lambda S: 3.0 * S
    sys.D = D_mutated
    
    mu_mutated = sys.measure_dissipative_margin(S0)
    print(f"   ETAT MUTÉ     | mu = {mu_mutated:.2f} (STABLE: µ > 0)")
    
    success = mu_mutated > 2.0
    print("-" * 50)
    print(f"RÉUSSITE EXP. | {'SUCCESS' if success else 'FAILURE'}")
    print("-" * 50)

if __name__ == "__main__":
    run_experiment_01()
