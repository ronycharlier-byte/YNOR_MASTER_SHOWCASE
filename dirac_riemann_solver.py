import numpy as np
import scipy.linalg as la
from scipy.special import zeta
import matplotlib.pyplot as plt
import os

# --- PARAMÈTRES DU SYSTÈME (SOUVERAINETÉ OPTIMALE) ---
N_POINTS = 5000        # Haute résolution spectrale
U_MAX = 7.0            # Horizon étendu (exp(7) ≈ 1096 primes)
ETA = 0.03             # Pics de Dirac plus fins
EPSILON = 0.05         # Convergence vers le régime critique
POTENTIAL_GAIN = 100.0 # Force du champ fractal pour décalage de Weyl

# --- MATRICES DE PAULI ---
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)

def von_mangoldt(n):
    """Calcule la fonction de von Mangoldt Lambda(n)"""
    if n < 2: return 0
    # Vérification naïve pour les petits n
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
    for p in primes:
        p_k = p
        while p_k <= n:
            if p_k == n: return np.log(p)
            p_k *= p
    return 0

def construct_potential(u_grid):
    """Construit le superpotentiel pair V(u)"""
    V = np.zeros_like(u_grid)
    n_max = int(np.exp(U_MAX))
    for n in range(2, n_max + 1):
        L = von_mangoldt(n)
        if L > 0:
            weight = L / (n**(0.5 + EPSILON)) * POTENTIAL_GAIN
            # Kicks gaussiens symétriques (Définit le champ informationnel)
            V += weight * np.exp(-(u_grid - np.log(n))**2 / (2 * ETA**2))
            V += weight * np.exp(-(u_grid + np.log(n))**2 / (2 * ETA**2))
    return V

def solve_dirac_riemann():
    u = np.linspace(-U_MAX, U_MAX, N_POINTS)
    du = u[1] - u[0]
    V = construct_potential(u)
    
    # 1. CONSTRUCTION DE H = -i * sigma_z * d/du + sigma_x * V
    # On utilise une matrice de différenciation finie (différence centrée)
    # H = [[ -i d/du, V ], [ V, i d/du ]]
    
    # Matrice de différenciation (différence centrée ordre 2)
    D1 = (np.diag(np.ones(N_POINTS-1), 1) - np.diag(np.ones(N_POINTS-1), -1)) / (2*du)
    
    H11 = -1j * D1
    H22 = 1j * D1
    H12 = np.diag(V)
    H21 = np.diag(V)
    
    # Construction du Hamiltonien de bloc 2N x 2N
    H = np.zeros((2*N_POINTS, 2*N_POINTS), dtype=complex)
    H[:N_POINTS, :N_POINTS] = H11
    H[N_POINTS:, N_POINTS:] = H22
    H[:N_POINTS, N_POINTS:] = H12
    H[N_POINTS:, :N_POINTS] = H21
    
    # 2. DIAGONALISATION (Hermitienne)
    print(f"Propulsion du système Delta-Ynor (Grille: {N_POINTS} pts)...")
    eigenvalues = la.eigvalsh(H)
    
    # Les valeurs propres sont symétriques par rapport à 0
    pos_eig = eigenvalues[eigenvalues > 0]
    return u, V, np.sort(pos_eig)

# --- EXÉCUTION ---
print("Lancement du Simulant Spectral Dirac-Riemann...")
u_grid, V_arr, energies = solve_dirac_riemann()

# Zéros réels de Riemann (premières valeurs pour comparaison)
true_zeros = [14.1347, 21.0220, 25.0108, 30.4248, 32.9350]

print("\n--- RÉSULTATS SPECTRAUX Δ-Ynor ---")
print(f"Premières énergies capturées : {energies[:5]}")
print(f"Zéros de Riemann cibles      : {true_zeros}")

# Visualisation (Sauvegarde au lieu de show pour environnement headless)
plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(u_grid, V_arr, color='#00d4ff', label='Superpotentiel V(u) (Log-Primes)')
plt.title("Résonateur Arithmétique Dirac-SUSY | V(u) = V(-u)")
plt.xlabel("Variable logarithmique u = ln(x)")
plt.ylabel("Magnitude V")
plt.grid(alpha=0.3)
plt.legend()

plt.subplot(2, 1, 2)
for z in true_zeros:
    plt.axvline(x=z, color='red', linestyle='--', alpha=0.5, label='Zeros Riemann' if z==true_zeros[0] else "")
plt.hist(energies, bins=150, range=(0, 40), color='#ff0055', alpha=0.7, label='Spectre Δ-Ynor (Valeurs propres)')
plt.title("Alignement Spectral (μ=1.0) | Corrélation Énergie <-> Zéros")
plt.xlabel("Énergie E / Spectre Spectral s = 1/2 + iE")
plt.ylabel("Densité d'états")
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()

output_file = "riemann_spectrum_ynor.png"
plt.savefig(output_file)
print(f"\nVisualisation générée : {output_file}")
