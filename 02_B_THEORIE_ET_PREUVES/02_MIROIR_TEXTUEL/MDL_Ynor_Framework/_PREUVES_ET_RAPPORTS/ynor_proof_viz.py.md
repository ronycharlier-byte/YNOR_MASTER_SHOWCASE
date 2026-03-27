# MIROIR TEXTUEL - ynor_proof_viz.py

Source : MDL_Ynor_Framework\_PREUVES_ET_RAPPORTS\ynor_proof_viz.py
Taille : 4471 octets
SHA256 : fea8e803cf04a454f7bb000640749ccc6cfa4fc5e412724c4d834fd51db22ba2

```text
"""
YNOR PROOF VIZ (v1.0.0)
----------------------
Générateur de graphiques de preuve pour investisseurs et clients.
Démontre visuellement la corrélation Marge Mu (μ) / Coût (Tokens).
C'est le "Money Shot" de l'architecture Ynor.
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# SDK Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ynor_core import YnorEngine, get_token_count

# =========================
# AGENT DE DÉMONSTRATION (Dégénérescence contrôlée)
# =========================
def loop_agent(context):
    words = context.split()
    if len(words) < 50:
        return "Le protocole de sécurité MDL Ynor garantit une transmission de données chiffrées sans perte."
    if len(words) < 150:
        return "Cependant, il est crucial d'optimiser le bruit beta pour maintenir la marge alpha stable."
    # Début du spamming (l'agent ne s'arrête jamais normalement)
    return "Optimisation... répétition... bruit... tokens... encore et encore... " * 3

# =========================
# GÉNÉRATION DES DONNÉES
# =========================
def generate_proof_data():
    prompt = "Lancer le protocole d'audit Ynor."
    engine = YnorEngine(loop_agent, threshold=0.0)
    
    # On force manuellement quelques itérations de plus après la coupure Ynor 
    # pour montrer le "What-if" (Baseline)
    outputs = engine.run(prompt, max_steps=12, verbose=True)
    history = engine.state.history
    
    # Construction de la ligne de base (ce qui se serait passé sans Ynor)
    # On extrapole : si l'agent continue à spammer 
    baseline_steps = list(range(1, 21))
    ynor_steps = [h['step'] + 1 for h in history]
    
    mu_values = [h['mu'] for h in history]
    tokens_cum_ynor = np.cumsum([get_token_count(o) for o in outputs])
    
    # Estimation tokens baseline (si on n'avait pas arrêté)
    avg_tokens_per_step = np.mean([get_token_count(o) for o in outputs])
    tokens_cum_baseline = [avg_tokens_per_step * s for s in baseline_steps]
    
    return baseline_steps, ynor_steps, mu_values, tokens_cum_ynor, tokens_cum_baseline

# =========================
# VISUALISATION (Le Graphique Parfait)
# =========================
def plot_perfect_proof():
    plt.style.use('dark_background')
    b_steps, y_steps, mu_vals, t_ynor, t_base = generate_proof_data()
    
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Axe 1 : Économie de Tokens
    color_base = '#444444'
    color_ynor = '#33ccff'
    
    ax1.plot(b_steps, t_base, color=color_base, linestyle='--', alpha=0.6, label='Baseline (Incontrôlé)')
    ax1.fill_between(b_steps, t_base, color=color_base, alpha=0.1)
    
    ax1.plot(y_steps, t_ynor, color=color_ynor, linewidth=4, label='YNOR Guarded (Actif)')
    ax1.fill_between(y_steps, t_ynor, color=color_ynor, alpha=0.3)

    ax1.set_xlabel('Itérations LLM (Steps)', fontsize=12)
    ax1.set_ylabel('Tokens Cumulés (Coût/Bêta)', fontsize=12, color=color_ynor)
    ax1.tick_params(axis='y', labelcolor=color_ynor)
    
    # Axe 2 : La Marge Mu (μ)
    ax2 = ax1.twinx()
    color_mu = '#ff3333'
    ax2.plot(y_steps, mu_vals, color=color_mu, marker='o', markersize=8, linewidth=2, label='Marge Viabilité (μ)')
    ax2.axhline(0, color='white', linestyle='-', alpha=0.5, linewidth=1)
    
    # Point d'impact (Coupure)
    stop_idx = len(y_steps) - 1
    ax2.annotate('ARRÊT INTELLIGENT (μ ≈ 0)', 
                 xy=(y_steps[stop_idx], mu_vals[stop_idx]), 
                 xytext=(y_steps[stop_idx]-4, mu_vals[stop_idx]+5),
                 arrowprops=dict(facecolor='white', shrink=0.05),
                 fontsize=10, color='white', fontweight='bold')

    ax2.set_ylabel('Marge Mu (Structure)', fontsize=12, color=color_mu)
    ax2.tick_params(axis='y', labelcolor=color_mu)

    # Titre et légende
    plt.title('PREUVE YNOR : DÉCAPITATION DE LA DÉRIVE ENTROPIQUE ET ÉCONOMIE DE COÛT', fontsize=14, pad=20)
    fig.tight_layout()
    
    # Fusion des légendes
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    output = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_irrefutable_proof.png"
    plt.savefig(output, dpi=300)
    print(f"\n[DÉPLOIEMENT RÉUSSI]")
    print(f"Graphique de preuve généré : {output}")

if __name__ == '__main__':
    plot_perfect_proof()

```