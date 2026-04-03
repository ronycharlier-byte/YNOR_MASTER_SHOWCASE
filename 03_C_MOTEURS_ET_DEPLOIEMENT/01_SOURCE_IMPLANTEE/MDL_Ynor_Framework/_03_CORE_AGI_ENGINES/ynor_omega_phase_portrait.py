import numpy as np
import matplotlib.pyplot as plt

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
        a, b, k = states[i]
        mu[i] = a - b - k

    a, b, k = states[-1]
    mu[-1] = a - b - k

    return t, states, mu

# =========================
# ÉQUILIBRE
# =========================

def equilibrium(p: dict) -> np.ndarray:
    # a3*a + a2*b = a1
    # -b1*a + b2*b = -b3
    # c2*a - c1*b + c3*k = 0

    M = np.array([
        [p["a3"],  p["a2"]],
        [-p["b1"], p["b2"]],
    ], dtype=float)

    rhs = np.array([p["a1"], -p["b3"]], dtype=float)

    a_star, b_star = np.linalg.solve(M, rhs)
    k_star = (p["c1"] * b_star - p["c2"] * a_star) / p["c3"]

    return np.array([a_star, b_star, k_star], dtype=float)

# =========================
# VISUALISATIONS (Portraits de phase structurés)
# =========================

def plot_phase_portrait_alpha_beta(
    params: dict,
    init_conditions: list,
    T: float = 40.0,
    dt: float = 0.01,
    a_range: tuple = (0.0, 4.0),
    b_range: tuple = (0.0, 4.0),
    grid_size: int = 20,
) -> None:
    plt.style.use('dark_background')
    a_vals = np.linspace(a_range[0], a_range[1], grid_size)
    b_vals = np.linspace(b_range[0], b_range[1], grid_size)
    A, B = np.meshgrid(a_vals, b_vals)

    eq = equilibrium(params)
    k_eq = eq[2]

    U = np.zeros_like(A)
    V = np.zeros_like(B)

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            da, db, _ = dynamics(np.array([A[i, j], B[i, j], k_eq]), params)
            U[i, j] = da
            V[i, j] = db

    plt.figure(figsize=(9, 7))
    plt.streamplot(A, B, U, V, density=1.2, color='#1f77b4', linewidth=0.8)

    colors = ['#ff3333', '#33cc33', '#ff9933', '#cc33ff', '#ffffff']

    for idx_c, init in enumerate(init_conditions):
        _, states, mu = simulate(params=params, T=T, dt=dt, init=init)
        color = colors[idx_c % len(colors)]
        plt.plot(states[:, 0], states[:, 1], linewidth=2.0, color=color, alpha=0.9)
        plt.plot(states[0, 0], states[0, 1], marker="o", color=color, markersize=6)

        idx = np.where(mu >= 0)[0]
        if len(idx) > 0:
            j = idx[0]
            plt.plot(states[j, 0], states[j, 1], marker="x", color='w', markersize=10, markeredgewidth=2)

    plt.plot(eq[0], eq[1], marker="*", color='#ffff00', markersize=18, label="Attracteur (*) Équilibre", zorder=10)

    plt.xlabel("α (Gain Informationnel)")
    plt.ylabel("β (Bruit et Coût d'expansion)")
    plt.title("Ynor Ω+ : Espace Vectoriel & Trajectoires de Viabilité (Plan α-β)")
    plt.legend()
    plt.grid(True, alpha=0.15)
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_phase_portrait_alpha_beta.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"[OK] Portrait de Phase (α vs β) généré : {output}")

def plot_phase_portrait_alpha_kappa(
    params: dict,
    init_conditions: list,
    T: float = 40.0,
    dt: float = 0.01,
    a_range: tuple = (0.0, 4.0),
    k_range: tuple = (0.0, 4.0),
    grid_size: int = 20,
) -> None:
    plt.style.use('dark_background')
    a_vals = np.linspace(a_range[0], a_range[1], grid_size)
    k_vals = np.linspace(k_range[0], k_range[1], grid_size)
    A, K = np.meshgrid(a_vals, k_vals)

    eq = equilibrium(params)
    b_eq = eq[1]

    U = np.zeros_like(A)
    V = np.zeros_like(K)

    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            da, _, dk = dynamics(np.array([A[i, j], b_eq, K[i, j]]), params)
            U[i, j] = da
            V[i, j] = dk

    plt.figure(figsize=(9, 7))
    plt.streamplot(A, K, U, V, density=1.2, color='#1f77b4', linewidth=0.8)

    colors = ['#ff3333', '#33cc33', '#ff9933', '#cc33ff', '#ffffff']

    for idx_c, init in enumerate(init_conditions):
        _, states, mu = simulate(params=params, T=T, dt=dt, init=init)
        color = colors[idx_c % len(colors)]
        plt.plot(states[:, 0], states[:, 2], linewidth=2.0, color=color, alpha=0.9)
        plt.plot(states[0, 0], states[0, 2], marker="o", color=color, markersize=6)

        idx = np.where(mu >= 0)[0]
        if len(idx) > 0:
            j = idx[0]
            plt.plot(states[j, 0], states[j, 2], marker="x", color='w', markersize=10, markeredgewidth=2)

    plt.plot(eq[0], eq[2], marker="*", color='#ffff00', markersize=18, label="Attracteur (*) Équilibre", zorder=10)

    plt.xlabel("α (Gain Informationnel)")
    plt.ylabel("κ (Charge Mnésique et Contexte)")
    plt.title("Ynor Ω+ : Espace Vectoriel & Trajectoires de Viabilité (Plan α-κ)")
    plt.legend()
    plt.grid(True, alpha=0.15)
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_phase_portrait_alpha_kappa.png"
    plt.savefig(output, dpi=300, bbox_inches='tight')
    print(f"[OK] Portrait de Phase (α vs κ) généré : {output}")

# =========================
# EXÉCUTION
# =========================

if __name__ == "__main__":
    
    print("\nCalcul de l'Équilibre Global pour le Portrait de Phase Ynor...")
    
    initial_conditions = [
        (0.3, 2.2, 1.7),  # Haut Coût, Haute Mémoire
        (0.5, 1.5, 1.0),  # Stress Modéré
        (1.2, 0.9, 0.8),  # Information Stable
        (2.0, 0.5, 0.3),  # Idéal : Haute Info, Bas Bruit
        (0.8, 2.5, 2.0),  # Surcharge Critique
    ]

    plot_phase_portrait_alpha_beta(
        params=BASE_PARAMS,
        init_conditions=initial_conditions,
        T=60.0,
        dt=0.01,
        a_range=(0.0, 3.5),
        b_range=(0.0, 3.5),
        grid_size=25,
    )

    plot_phase_portrait_alpha_kappa(
        params=BASE_PARAMS,
        init_conditions=initial_conditions,
        T=60.0,
        dt=0.01,
        a_range=(0.0, 3.5),
        k_range=(0.0, 3.5),
        grid_size=25,
    )
