# MIROIR TEXTUEL - hardcore_validation.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\hardcore_validation.py
Taille : 3497 octets
SHA256 : cd2d3e3ad6f26cd29bc80b4ad4367d2bfffb4b34861f792ff98b28f0de7f395a

```text
import math
import random

def inference_error(diff_factor, step, noise_level):
    # La divergence baisse avec l'itération mais avec un plancher stochastique
    base_error = math.exp(-step / diff_factor)
    return base_error + random.uniform(0, noise_level)

def compute_viability(error, step, alpha=0.2, beta=0.05):
    I_eff = 1.0 - error
    D_kl = error * 1.5
    C = float(step)
    return I_eff - (alpha * D_kl) - (beta * C)

def run_trial(diff_factor, noise_level, max_steps, mode="ynor", alpha=0.2, beta=0.05):
    best_L = -999.0
    best_step = 1
    
    # 1. Génération de la trajectoire (même environnement pour tous les modes)
    traj = []
    for s in range(1, max_steps + 1):
        err = inference_error(diff_factor, s, noise_level)
        # La vraie viabilité du système évaluée de l'extérieur:
        L_true = compute_viability(err, s, alpha, beta)
        traj.append((s, L_true, err))
        
    # 2. Comportement selon le contrôleur
    if mode == "ynor":
        for s, L, err in traj:
            if L > best_L:
                best_L = L
                best_step = s
        return best_step, best_L
        
    elif mode == "fixed": # LLM standard
        s, L, err = traj[-1]
        return s, L
        
    elif mode == "random": # Contrôleur aléatoire (Monkey)
        s, L, err = random.choice(traj)
        return s, L
        
    elif mode == "ablation_no_C": # Optimise sans prendre en compte le coût (\beta = 0)
        best_L_internal = -999.0
        b_s = 1
        for s in range(1, max_steps + 1):
            err = traj[s-1][2]
            L_int = compute_viability(err, s, alpha=alpha, beta=0.0) 
            if L_int > best_L_internal:
                best_L_internal = L_int
                b_s = s
        # On retourne la viabilité RÉELLE évaluée par la nature
        _, real_L, _ = traj[b_s-1]
        return b_s, real_L

    elif mode == "ablation_no_D": # Optimise sans peur de l'incohérence (\alpha = 0)
        best_L_internal = -999.0
        b_s = 1
        for s in range(1, max_steps + 1):
            err = traj[s-1][2]
            L_int = compute_viability(err, s, alpha=0.0, beta=beta) 
            if L_int > best_L_internal:
                best_L_internal = L_int
                b_s = s
        _, real_L, _ = traj[b_s-1]
        return b_s, real_L

def run_experiment_suite():
    seeds = 100 # Loi des grands nombres
    diff_factor = 2.5
    noise_level = 0.08
    max_steps = 15
    
    results = {"ynor": [], "fixed": [], "random": [], "ablation_no_C": [], "ablation_no_D": []}
    
    for s in range(seeds):
        # Mêmé gen stochastique par architecture pour comparaison iso
        for mode in results.keys():
            random.seed(s) 
            step, L = run_trial(diff_factor, noise_level, max_steps, mode)
            results[mode].append((step, L))
            
    print("==================================================")
    print("🧪 VALIDATION HARDCORE YNOR : MONTE CARLO N=100")
    print("==================================================")
    for mode, data in results.items():
        avg_step = sum(x[0] for x in data) / seeds
        avg_L = sum(x[1] for x in data) / seeds
        var_L = sum((x[1] - avg_L)**2 for x in data) / seeds
        
        # Formatage clean
        nom = mode.upper().ljust(15)
        print(f"[{nom}] -> Compute Moyen: {avg_step:4.1f} steps | Viabilité Finale (\u03bc): {avg_L:6.3f} | Variance: {var_L:5.4f}")

run_experiment_suite()

```