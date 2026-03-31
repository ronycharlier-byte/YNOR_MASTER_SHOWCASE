# MIROIR TEXTUEL - run_and_log_experiments.py

Source : MDL_Ynor_Framework\_08_EXPERIMENTS_AND_DEMOS\experiments\run_and_log_experiments.py
Taille : 1332 octets
SHA256 : f457a600d279a1071b9117d4dfb3bcb9d759412b2576e2e72d2a9bec245fcc36

```text
import json
import time
import os
import random

def run_experiment(seed=42):
    random.seed(seed)
    
    # Simulate a run
    config = {
        "alpha_weight": 0.2,
        "beta_weight": 0.05,
        "kappa_base": 0.01,
        "seed": seed
    }
    
    metrics = []
    mu_total = 1.0
    for step in range(1, 11):
        alpha = random.uniform(0.1, 0.5) * (1/step)
        beta = 0.05 + (0.01 * step)
        kappa = 0.01 * (step**1.1)
        mu = alpha - (beta + kappa)
        mu_total += mu
        
        metrics.append({
            "step": step,
            "alpha": round(alpha, 4),
            "beta": round(beta, 4),
            "kappa": round(kappa, 4),
            "mu": round(mu, 4)
        })
        
        if mu <= 0:
            break
            
    result = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": config,
        "metrics": metrics,
        "final_status": "SUCCESS" if mu_total > 0 else "COLLAPSE"
    }
    
    os.makedirs("experiments", exist_ok=True)
    filename = f"experiments/run_{seed}_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(f"Experiment finished. Results saved to {filename}")

if __name__ == "__main__":
    for s in [42, 101, 2026]:
        run_experiment(s)

```