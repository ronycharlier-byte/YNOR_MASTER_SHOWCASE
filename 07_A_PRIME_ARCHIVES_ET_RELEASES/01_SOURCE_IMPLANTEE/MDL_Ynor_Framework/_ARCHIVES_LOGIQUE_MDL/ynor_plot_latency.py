# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import json
import matplotlib.pyplot as plt
import numpy as np

def plot_latency_benchmark():
    file_path = "mdl_openai_stress_benchmark.json"
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Erreur : Fichier de benchmark introuvable. Lancez d'abord le stress test.")
        return

    details = data.get("details", [])
    if not details:
        print("Aucune intervention enregistre dans le benchmark.")
        return

    nodes = [d["node"] for d in details]
    latencies = [d["latency_ms"] for d in details]
    mutations = [d["mutation_suggested"] for d in details]

    # Cration du Graphique
    plt.figure(figsize=(10, 6))
    bars = plt.bar(nodes, latencies, color='skyblue', edgecolor='navy', alpha=0.8)
    
    # Ajout des tiquettes (Latence et Taux de mutation)
    for bar, mut in zip(bars, mutations):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 50, 
                 f"{yval:.0f}ms\n(Mut: +{mut*100:.0f}%)", 
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("BENCHMARK IA : INDICE DE DIFFICULT PAR NUD MDL YNOR")
    plt.ylabel("Temps de Rflexion OpenAI (ms)")
    plt.xlabel("Nuds de l'Principal Investigatorure")
    plt.ylim(0, max(latencies) * 1.3)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    
    output_file = "mdl_latency_benchmark_chart.png"
    plt.savefig(output_file)
    print(f"\n[OK] Graphique de benchmarking gnr : {output_file}")
    
    # Rapport textuel
    hardest_node = nodes[np.argmax(latencies)]
    print(f"\n[ANALYSE] Le nud le plus complexe  stabiliser pour l'IA est : {hardest_node}")

if __name__ == "__main__":
    plot_latency_benchmark()



