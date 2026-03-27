import numpy as np
import matplotlib.pyplot as plt
import os

# =========================
# PARAMÈTRES DE BASE
# =========================

BASE_PARAMS = {
    "a1": 2.0, "a2": 0.8, "a3": 0.6,
    "b1": 0.7, "b2": 1.1, "b3": 0.4,
    "c1": 0.5, "c2": 0.3, "c3": 0.9,
}

# =========================
# DYNAMIQUE
# =========================

def dynamics(state: np.ndarray, p: dict) -> np.ndarray:
    a, b, k = state
    da = p["a1"] - p["a2"] * b - p["a3"] * a
    db = p["b1"] * a - p["b2"] * b - p["b3"]
    dk = p["c1"] * b - p["c2"] * a - p["c3"] * k
    return np.array([da, db, dk], dtype=float)

def rk4_step(state: np.ndarray, dt: float, p: dict) -> np.ndarray:
    k1 = dynamics(state, p)
    k2 = dynamics(state + 0.5 * dt * k1, p)
    k3 = dynamics(state + 0.5 * dt * k2, p)
    k4 = dynamics(state + dt * k3, p)
    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)

# =========================
# SIMULATION
# =========================

def simulate(
    params: dict,
    T: float = 40.0,
    dt: float = 0.01,
    init: tuple[float, float, float] = (0.5, 1.5, 1.0),
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    n_steps = int(T / dt)
    t = np.linspace(0.0, T, n_steps)
    states = np.zeros((n_steps, 3), dtype=float)
    mu = np.zeros(n_steps, dtype=float)

    states[0] = np.array(init, dtype=float)

    for i in range(n_steps - 1):
        states[i + 1] = rk4_step(states[i], dt, params)
        # Positivité stricte (Axiome A1)
        if states[i + 1][0] < 0: states[i + 1][0] = 0
        if states[i + 1][1] < 0: states[i + 1][1] = 0
        if states[i + 1][2] < 0: states[i + 1][2] = 0
        a, b, k = states[i]
        mu[i] = a - b - k

    a, b, k = states[-1]
    mu[-1] = a - b - k
    return t, states, mu

# =========================
# CLASSIFICATION DES RÉGIMES
# =========================

def classify_mu(mu_final: float, eps: float = 0.05) -> int:
    if mu_final > eps:
        return 1
    if mu_final < -eps:
        return -1
    return 0

# =========================
# HEATMAP 2D
# =========================

def build_heatmap(
    a2_values: np.ndarray,
    b1_values: np.ndarray,
    base_params: dict = BASE_PARAMS,
    T: float = 40.0,
    dt: float = 0.05,
    init: tuple[float, float, float] = (0.5, 1.5, 1.0),
    eps: float = 0.05,
) -> tuple[np.ndarray, np.ndarray]:
    
    mu_grid = np.zeros((len(b1_values), len(a2_values)), dtype=float)
    regime_grid = np.zeros((len(b1_values), len(a2_values)), dtype=int)

    for i, b1 in enumerate(b1_values):
        for j, a2 in enumerate(a2_values):
            params = dict(base_params)
            params["a2"] = float(a2)
            params["b1"] = float(b1)

            _, _, mu = simulate(params=params, T=T, dt=dt, init=init)
            mu_final = float(mu[-1])

            mu_grid[i, j] = mu_final
            regime_grid[i, j] = classify_mu(mu_final, eps=eps)

    return mu_grid, regime_grid

# =========================
# VISUALISATION
# =========================

def plot_mu_heatmap(a2_values, b1_values, mu_grid):
    plt.style.use('dark_background')
    plt.figure(figsize=(9, 6))
    im = plt.imshow(
        mu_grid, origin="lower", aspect="auto", cmap="RdYlGn",
        extent=[a2_values[0], a2_values[-1], b1_values[0], b1_values[-1]]
    )
    plt.colorbar(im, label="Marge Asymptotique (μ final)")
    
    contours = plt.contour(
        a2_values, b1_values, mu_grid, levels=[0.0],
        colors='white', linewidths=2, linestyles='--'
    )
    plt.clabel(contours, inline=True, fontsize=10, fmt="Surface Critique Σ (μ=0)")
    
    plt.xlabel("Paramètre a2 (Inhibition de Valeur par le Bruit)")
    plt.ylabel("Paramètre b1 (Création de Bruit par la Valeur)")
    plt.title("Heatmap Ynor : Espace Paramétrique de Marge Dissipative")
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_regimes_mu_heatmap.png"
    plt.savefig(output, dpi=300)
    print(f"[OK] Heatmap MU sauvegardée : {output}")

def plot_regime_map(a2_values, b1_values, regime_grid):
    plt.style.use('dark_background')
    plt.figure(figsize=(9, 6))
    im = plt.imshow(
        regime_grid, origin="lower", aspect="auto", cmap="RdYlGn",
        extent=[a2_values[0], a2_values[-1], b1_values[0], b1_values[-1]],
        vmin=-1, vmax=1
    )
    plt.colorbar(im, ticks=[-1, 0, 1], format=plt.FuncFormatter(lambda val, loc: ['Non Viable (-1)', 'Critique (0)', 'Viable (+1)'][int(val)+1]))
    
    plt.xlabel("Paramètre a2")
    plt.ylabel("Paramètre b1")
    plt.title("Classification Topologique des Régimes (Stables vs Crash)")
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_regimes_classification.png"
    plt.savefig(output, dpi=300)
    print(f"[OK] Heatmap de Classification sauvegardée : {output}")

# =========================
# EXÉCUTION
# =========================

if __name__ == "__main__":
    print("Construction de la Cartographie 2D des Régimes...")
    a2_values = np.linspace(0.1, 2.0, 80)
    b1_values = np.linspace(0.1, 2.0, 80)

    # Réduire 'dt' légèrement pour la rapidité du calcul sur la grille de 80x80 (6400 points)
    mu_grid, regime_grid = build_heatmap(
        a2_values=a2_values, b1_values=b1_values, T=40.0, dt=0.05, init=(0.5, 1.5, 1.0), eps=0.05
    )

    plot_mu_heatmap(a2_values, b1_values, mu_grid)
    plot_regime_map(a2_values, b1_values, regime_grid)
