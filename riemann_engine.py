import numpy as np
import scipy.linalg as la
from pydantic import BaseModel
from typing import List, Dict

# --- PARAMÈTRES PAR DÉFAUT ---
DEFAULT_N_POINTS = 500
DEFAULT_U_MAX = 5.0
DEFAULT_ETA = 0.05
DEFAULT_EPSILON = 0.1
DEFAULT_POTENTIAL_GAIN = 10.0

class RiemannResult(BaseModel):
    mu: float
    energies: List[float]
    true_zeros: List[float]
    status: str

def von_mangoldt(n):
    if n < 2: return 0
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    for p in primes:
        p_k = p
        while p_k <= n:
            if p_k == n: return np.log(p)
            p_k *= p
    return 0

def run_riemann_engine(n_points=DEFAULT_N_POINTS, u_max=DEFAULT_U_MAX, gain=DEFAULT_POTENTIAL_GAIN):
    """Exécute le moteur spectral Dirac-SUSY Ynor"""
    u = np.linspace(-u_max, u_max, n_points)
    du = u[1] - u[0]
    
    # Construction du potentiel
    V = np.zeros_like(u)
    n_max = int(np.exp(u_max))
    for n in range(2, n_max + 1):
        lam = von_mangoldt(n)
        if lam > 0:
            weight = lam / (n**0.6) * gain
            V += weight * np.exp(-(u - np.log(n))**2 / (2 * 0.05**2))
            V += weight * np.exp(-(u + np.log(n))**2 / (2 * 0.05**2))
            
    # Hamiltonien de Dirac
    D1 = (np.diag(np.ones(n_points-1), 1) - np.diag(np.ones(n_points-1), -1)) / (2*du)
    H = np.zeros((2*n_points, 2*n_points), dtype=complex)
    H[:n_points, :n_points] = -1j * D1
    H[n_points:, n_points:] = 1j * D1
    V_mat = np.diag(V)
    H[:n_points, n_points:] = V_mat
    H[n_points:, :n_points] = V_mat
    
    # Diagonalisation
    eigenvalues = la.eigvalsh(H)
    pos_eig = np.sort(eigenvalues[eigenvalues > 0])
    
    return {
        "mu": 1.0,
        "energies": pos_eig[:10].tolist(),
        "true_zeros": [14.134, 21.022, 25.011, 30.425, 32.935],
        "status": "SATURATED"
    }

if __name__ == "__main__":
    # Test local
    print(run_riemann_engine())
