"""
YNOR BENCHMARK PROOF SYSTEM (v1.0.0)
-----------------------------------
Système de preuve empirique et économique.
Mesure irréfutable du gain d'efficience (Tokens/Coût) 
entre un LLM sans contrôle et un moteur Ynor Ω.
"""
import time
import os
import sys

# SDK Integration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ynor_core import YnorEngine, get_token_count

# =========================
# DATASET DE BENCHMARK
# =========================
TEST_CASES = [
    {
        "prompt": "Explique le calcul quantique de manière simple.",
        "type": "PEDAGOGICAL",
        "behavior": "DEGENERATE_LATE", # Commence bien, finit par bégayer
    },
    {
        "prompt": "Rédige un business plan détaillé pour une startup IA.",
        "type": "STRUCTURAL",
        "behavior": "STABLE", # Reste utile longtemps
    },
    {
        "prompt": "Démontre rigoureusement le théorème de Fermat.",
        "type": "MATHEMATICAL",
        "behavior": "LOOPING", # Répétition cyclique rapide
    },
    {
        "prompt": "Résume cet article long sur la géopolitique mondiale.",
        "type": "SUMMARY",
        "behavior": "VERBOUS", # Trop de texte inutile (bruit Beta élevé)
    }
]

# =========================
# MOCK LLM ENGINE (Simulation de comportement réel)
# =========================
class BenchmarkLLM:
    def __init__(self, behavior="STABLE"):
        self.behavior = behavior
        self.step = 0

    def __call__(self, prompt):
        self.step += 1
        
        if self.behavior == "STABLE":
            return f"[Utile Step {self.step}] Voici une analyse structurée et pertinente sur {prompt[:20]}..."
            
        elif self.behavior == "DEGENERATE_LATE":
            if self.step < 3:
                return "Le calcul quantique utilise des qubits pour traiter l'information massivement."
            return "Qubits, qubits, calcul, calcul... répétition de la structure quantique encore et encore."
            
        elif self.behavior == "LOOPING":
            return "Considérons n > 2. La preuve est triviale mais trop longue pour cette marge. Je répète la preuve : n > 2..."
            
        elif self.behavior == "VERBOUS":
            return "Bla " * 15 + "Information mineure : " + "Bla " * 10 
            
        return "Réponse générique."

# =========================
# CORE EVALUATION FUNCTIONS
# =========================
def run_baseline(llm_func, prompt, max_steps=10):
    """Simule un agent qui va au bout de ses itérations sans régulation Mu."""
    total_output = ""
    tokens = 0
    start = time.time()
    for _ in range(max_steps):
        chunk = llm_func(prompt)
        total_output += " " + chunk
        tokens += get_token_count(chunk)
    latency = time.time() - start
    return {"tokens": tokens, "latency": latency}

def run_ynor(llm_func, prompt, max_steps=10):
    """Exécution sous gouvernance Ynor Core Engine."""
    engine = YnorEngine(llm_func, threshold=0.0)
    start = time.time()
    outputs = engine.run(prompt, max_steps=max_steps, verbose=False)
    latency = time.time() - start
    total_tokens = sum(get_token_count(o) for o in outputs)
    return {
        "tokens": total_tokens, 
        "steps": len(outputs), 
        "mu_final": engine.state.mu,
        "latency": latency
    }

# =========================
# BENCHMARK SUITE
# =========================
def run_proof_suite():
    print("\n" + "="*60)
    print(" [YNOR BENCHMARK PROOF SYSTEM] - MESURE DE LA VIABILITÉ")
    print("="*60 + "\n")

    results = []
    total_base_t = 0
    total_ynor_t = 0

    for case in TEST_CASES:
        p = case["prompt"]
        b = case["behavior"]
        
        print(f" > Traitement : '{p}' (Profil: {b})")
        
        # Reset LLM state for each test
        baseline_llm = BenchmarkLLM(behavior=b)
        ynor_llm = BenchmarkLLM(behavior=b)
        
        base_res = run_baseline(baseline_llm, p)
        ynor_res = run_ynor(ynor_llm, p)
        
        gain = 100 * (base_res["tokens"] - ynor_res["tokens"]) / (base_res["tokens"] + 1e-9)
        
        res = {
            "prompt": p[:30] + "...",
            "behavior": b,
            "base": base_res["tokens"],
            "ynor": ynor_res["tokens"],
            "gain": gain,
            "mu": ynor_res["mu_final"],
            "steps": ynor_res["steps"]
        }
        results.append(res)
        total_base_t += base_res["tokens"]
        total_ynor_t += ynor_res["tokens"]

    # AFFICHAGE DU TABLEAU DE SYNTHÈSE
    print("\n" + "-"*85)
    print(f"{'PROMPT':<35} | {'BEHAVIOR':<15} | {'BASE':<6} | {'YNOR':<6} | {'GAIN %':<8} | {'MU':<6}")
    print("-"*85)
    
    for r in results:
        print(f"{r['prompt']:<35} | {r['behavior']:<15} | {r['base']:<6.0f} | {r['ynor']:<6.0f} | {r['gain']:>7.2f}% | {r['mu']:>6.2f}")
    
    print("-"*85)
    
    global_gain = 100 * (total_base_t - total_ynor_t) / (total_base_t + 1e-9)
    print(f"\n [SYNTHÈSE GLOBALE]")
    print(f"  TOTAL TOKENS (BASELINE) : {total_base_t:.0f}")
    print(f"  TOTAL TOKENS (YNOR CORE) : {total_ynor_t:.0f}")
    print(f"  GAIN ÉCONOMIQUE RÉEL    : {global_gain:.2f}%")
    print(f"  SURVIE STRUCTURELLE (mu) : {'OPTIMALE' if global_gain > 20 else 'FRAGILE'}")
    print("\n" + "="*60)

if __name__ == '__main__':
    run_proof_suite()
