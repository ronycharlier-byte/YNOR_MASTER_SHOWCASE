# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import get_ai_reconstruction_strategy

class UltimateStressTest:
    """
    Test de rupture globale et Benchmark de l'IA Gouverneur.
    """
    def __init__(self):
        # Initialisation Master (5 Noeuds)
        self.nodes = {
            "ENERGIE": YnorSystem(2, lambda S: 1.5 * S, lambda S: 0.5 * S),
            "MATIERE": YnorSystem(2, lambda S: 1.0 * S, lambda S: 1.2 * S),
            "INFORMATION": YnorSystem(2, lambda S: 2.0 * S, lambda S: 0.8 * S),
            "GOUVERNANCE": YnorSystem(2, lambda S: 0.5 * S, lambda S: 1.5 * S),
            "BIOLOGIE": YnorSystem(2, lambda S: 1.2 * S, lambda S: 1.0 * S)
        }
        self.states = {name: np.array([1.0, 1.0]) for name in self.nodes.keys()}
        self.benchmark_results = []

    def inject_global_shock(self):
        print("\n[!!!] CHOC GLOBAL DTECT : Injection d'Incohrence Structurelle...")
        for name in self.states.keys():
            self.states[name] = self.states[name] * 50.0 # Multiplicateur de choc x50

    def run(self):
        print("=====================================================")
        print("   STRESS TEST ULTIME & BENCHMARK OPENIA")
        print("=====================================================\n")

        t = 0.0
        dt = 0.2
        steps = 15
        
        for step in range(steps):
            print(f"-- Cycle t={t:.1f} --")
            
            # Injection du choc  t=1.0
            if step == 5:
                self.inject_global_shock()

            # Audit de survie
            for name, sys in self.nodes.items():
                mu = sys.measure_dissipative_margin(self.states[name])
                
                if mu <= 0.0:
                    print(f"   [CRISE] Noeud {name} (mu={mu:.2f})")
                    
                    # MESURE DU BENCHMARK (TEMPS DE RPONSE)
                    start_time = time.time()
                    strategy = get_ai_reconstruction_strategy(mu, self.states[name].tolist())
                    latency = (time.time() - start_time) * 1000 # en ms
                    
                    r = strategy["mutation_rate"]
                    
                    # Mise  jour du nud
                    old_D = sys.D
                    sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
                    
                    # Log du Benchmark
                    self.benchmark_results.append({
                        "node": name,
                        "t": t,
                        "mu_before": float(mu),
                        "mutation_suggested": float(r),
                        "latency_ms": latency,
                        "ai_explanation": strategy.get("explanation", "No explanation")
                    })
                    print(f"   [IA] Noeud {name} stabilis. Latence IA : {latency:.0f}ms")

            # Dynamique simple
            for name, sys in self.nodes.items():
                self.states[name] = self.states[name] + sys.dynamics(t, self.states[name]) * dt
            
            t += dt

        self.save_benchmark()

    def save_benchmark(self):
        avg_latency = np.mean([res["latency_ms"] for res in self.benchmark_results])
        total_mutations = len(self.benchmark_results)
        
        final_report = {
            "test_type": "GLOBAL_CRASH_RESILIENCE",
            "date": time.ctime(),
            "average_ai_latency_ms": float(avg_latency),
            "total_intervention_count": total_mutations,
            "details": self.benchmark_results
        }
        
        with open("mdl_openai_stress_benchmark.json", "w") as f:
            json.dump(final_report, f, indent=4)
            
        print("\n" + "="*50)
        print("   BENCHMARK OPENIA TERMIN")
        print("="*50)
        print(f"Latence moyenne de l'IA Gouverneur : {avg_latency:.0f} ms")
        print(f"Nombre total d'interventions russies : {total_mutations}")
        print("[OK] Rapport complet sauvegard : mdl_openai_stress_benchmark.json")

if __name__ == "__main__":
    stress = UltimateStressTest()
    stress.run()



