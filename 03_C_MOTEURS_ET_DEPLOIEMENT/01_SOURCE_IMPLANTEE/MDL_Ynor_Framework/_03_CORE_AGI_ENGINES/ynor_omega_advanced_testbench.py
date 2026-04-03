"""
BANC D'ESSAI NUMÉRIQUE RÉEL YNOR Ω+
-----------------------------------
Expérimentation paramétrique avancée et Heatmap Topologique.
Test de robustesse des attracteurs Ynor.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def ynor_dynamics(a, b, k, a1, a2, a3, b1, b2, b3, c1, c2, c3):
    da = a1 - a2*b - a3*a
    db = b1*a - b2*b - b3
    dk = c1*b - c2*a - c3*k
    return da, db, dk

def run_testbench():
    print("==================================================")
    print(" Lancement du Banc d'Essai Paramétrique YNOR Ω+   ")
    print("==================================================")
    
    # SCAN DE PARAMÈTRES : On analyse l'impact de 'b1' (taux auquel la Valeur génère du Coût/Bruit)
    # et de 'c1' (taux auquel le Bruit sature la Mémoire).
    b1_vals = np.linspace(0.1, 2.0, 100)
    c1_vals = np.linspace(0.1, 2.0, 100)
    
    mu_final = np.zeros((len(c1_vals), len(b1_vals)))
    
    T = 30.0
    dt = 0.05
    N = int(T/dt)
    
    # Paramètres de base de l'Équilibre
    a1, a2, a3 = 2.0, 0.8, 0.6
    b2, b3 = 1.1, 0.4
    c2, c3 = 0.3, 0.9
    
    for i, c1 in enumerate(c1_vals):
        for j, b1 in enumerate(b1_vals):
            # Conditions initiales perturbées
            a, b, k = 0.4, 1.8, 1.2
            for _ in range(N):
                da, db, dk = ynor_dynamics(a, b, k, a1, a2, a3, b1, b2, b3, c1, c2, c3)
                a += dt*da
                b += dt*db
                k += dt*dk
                
                # Physique stricte (valeurs >= 0)
                if a < 0: a = 0
                if b < 0: b = 0
                if k < 0: k = 0
                
            mu_final[i, j] = a - b - k

    # Création de la Heatmap Structurée
    plt.style.use('dark_background')
    plt.figure(figsize=(10, 8))
    
    # Colormap: Rouge (Instable) -> Jaune (Critique) -> Vert (Stable)
    img = plt.imshow(mu_final, extent=[b1_vals.min(), b1_vals.max(), c1_vals.min(), c1_vals.max()],
               origin='lower', aspect='auto', cmap='RdYlGn')
    plt.colorbar(img, label='Marge asymptotique (μ*) à l\'équilibre')
    
    # Ligne des zéros (Surface Critique)
    contours = plt.contour(b1_vals, c1_vals, mu_final, levels=[0], colors='white', linewidths=3, linestyles='--')
    plt.clabel(contours, inline=True, fontsize=12, fmt="Surface Critique Σ (μ=0)")
    
    plt.title('BANC D\'ESSAI YNOR : Diagramme de Phase & Zones de Stabilité', fontsize=14, color='white')
    plt.xlabel('Paramètre $b_1$ (Taux d\'Expansion du Coût Textuel)', fontsize=12)
    plt.ylabel('Paramètre $c_1$ (Taux de Surcharge Mémorielle)', fontsize=12)
    
    # Annotations
    plt.text(np.percentile(b1_vals, 10), np.percentile(c1_vals, 80), 'RÉGIME VIABLE\n(Auto-Stabilisation de l\'IA)', 
             color='black', fontsize=12, fontweight='bold', bbox=dict(facecolor='#33cc33', alpha=0.8, edgecolor='none'))
    plt.text(np.percentile(b1_vals, 60), np.percentile(c1_vals, 15), 'RÉGIME NON-VIABLE\n(Dérive Thermodynamique LLM)', 
             color='white', fontsize=12, fontweight='bold', bbox=dict(facecolor='#ff3333', alpha=0.8, edgecolor='none'))

    output_path = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_heatmap_stability.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"\n[OK] Heatmap de Stabilité Globalisée générée : {output_path}")

if __name__ == '__main__':
    run_testbench()
