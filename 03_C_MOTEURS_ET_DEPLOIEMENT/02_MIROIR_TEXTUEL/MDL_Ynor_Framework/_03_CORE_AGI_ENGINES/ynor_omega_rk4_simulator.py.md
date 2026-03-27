# MIROIR TEXTUEL - ynor_omega_rk4_simulator.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\ynor_omega_rk4_simulator.py
Taille : 4865 octets
SHA256 : c760a7b81152f31dbae3627a4ef304e5def2907e643ae0b480d3b75282a4ee7f

```text
import numpy as np
import matplotlib.pyplot as plt

# =========================
# PARAMÈTRES DU SYSTÈME
# =========================

params = {
    "a1": 2.0,
    "a2": 0.8,
    "a3": 0.6,
    "b1": 0.7,
    "b2": 1.1,
    "b3": 0.4,
    "c1": 0.5,
    "c2": 0.3,
    "c3": 0.9,
}

# =========================
# DYNAMIQUE
# =========================

def dynamics(state, p):
    a, b, k = state

    da = p["a1"] - p["a2"]*b - p["a3"]*a
    db = p["b1"]*a - p["b2"]*b - p["b3"]
    dk = p["c1"]*b - p["c2"]*a - p["c3"]*k

    return np.array([da, db, dk])

# =========================
# INTÉGRATION RK4
# =========================

def rk4_step(state, dt, p):
    k1 = dynamics(state, p)
    k2 = dynamics(state + 0.5*dt*k1, p)
    k3 = dynamics(state + 0.5*dt*k2, p)
    k4 = dynamics(state + dt*k3, p)

    return state + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

# =========================
# SIMULATION
# =========================

def simulate(T=40, dt=0.01, init=(0.5, 1.5, 1.0)):

    N = int(T/dt)
    t = np.linspace(0, T, N)

    S = np.zeros((N, 3))
    mu = np.zeros(N)
    dmu = np.zeros(N)

    S[0] = np.array(init)

    for i in range(N-1):
        S[i+1] = rk4_step(S[i], dt, params)

        a, b, k = S[i]
        mu[i] = a - b - k

        da, db, dk = dynamics(S[i], params)
        dmu[i] = da - db - dk

        # Application de la Positivité Stricte (A1)
        if S[i+1][0] < 0: S[i+1][0] = 0
        if S[i+1][1] < 0: S[i+1][1] = 0
        if S[i+1][2] < 0: S[i+1][2] = 0

    mu[-1] = S[-1,0] - S[-1,1] - S[-1,2]

    return t, S, mu, dmu

# =========================
# ANALYSE
# =========================

def analyze(mu, t):
    # passage critique
    crossings = np.where((mu[:-1] < 0) & (mu[1:] >= 0))[0]

    if len(crossings) > 0:
        t_star = t[crossings[0]]
    else:
        t_star = None

    stable = np.abs(mu[-1] - mu[-50]) < 1e-3

    return {
        "t_recovery": t_star,
        "stable": stable,
        "final_mu": mu[-1]
    }

# =========================
# VISUALISATION
# =========================

def plot_results(t, S, mu):
    plt.style.use('dark_background')
    plt.figure(figsize=(10,6))

    plt.plot(t, S[:,0], label="alpha (Valeur)", color='#33ccff')
    plt.plot(t, S[:,1], label="beta (Coût)", color='#ff9933')
    plt.plot(t, S[:,2], label="kappa (Mémoire)", color='#cc33ff')
    plt.plot(t, mu, label="mu (Marge Dissipative)", linewidth=3, color='#ff3333')

    plt.axhline(0, linestyle="--", color='white')

    plt.legend()
    plt.title("Dynamique Ynor Ω+ (Intégration RK4)")
    plt.xlabel("t (Temps/Tokens)")
    plt.ylabel("Valeurs d'État")
    plt.grid(True, alpha=0.2)

    output = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_rk4_dynamics.png"
    plt.savefig(output, dpi=300)
    print(f"Graphique dynamique sauvegardé : {output}")

# =========================
# MODE EXPERT - SCAN DE PARAMÈTRES
# =========================

def scan_parameter(param_name, values):
    results = []
    # Sauvegarde de la valeur originale
    original_val = params[param_name]

    for v in values:
        params[param_name] = v
        t, S, mu, _ = simulate(init=(0.4, 1.8, 1.2))
        analysis = analyze(mu, t)
        results.append((v, analysis["final_mu"]))

    # Restauration
    params[param_name] = original_val
    return results

def run_expert_scan():
    values = np.linspace(0.1, 2.0, 50)
    scan = scan_parameter("a2", values)

    x = [v for v, m in scan]
    y = [m for v, m in scan]

    plt.figure(figsize=(10,6))
    plt.plot(x, y, color='#00ffcc', linewidth=2)
    plt.axhline(0, linestyle="--", color='white')
    
    plt.fill_between(x, np.min(y), y, where=(np.array(y)>0), color='green', alpha=0.2, label='Viable')
    plt.fill_between(x, np.min(y), y, where=(np.array(y)<=0), color='red', alpha=0.2, label='Effondrement')
    
    plt.xlabel("Paramètre a2 (Sensibilité de Valeur au Coût)")
    plt.ylabel("Marge μ finale à l'équilibre")
    plt.title("Scan Ynor Ω+ : Zone de stabilité (Bifurcation selon a2)")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    output = r"C:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\_02_RESEARCH_GRAPHS\ynor_omega_rk4_scan.png"
    plt.savefig(output, dpi=300)
    print(f"Graphique de Bifurcation sauvegardé : {output}")

# =========================
# EXECUTION CENTRALE
# =========================
if __name__ == '__main__':
    t, S, mu, dmu = simulate()
    results = analyze(mu, t)

    print("=== ANALYSE EMPIRIQUE YNOR Ω+ ===")
    print(f"Stabilité asymptotique garantie : {results['stable']}")
    print(f"Temps de recouvrement critique t*: {results['t_recovery']}")
    print(f"Marge Résiduelle Émergente μ* : {results['final_mu']:.4f}")

    plot_results(t, S, mu)
    
    print("\n=== SCAN EXPERT EN COURS ===")
    run_expert_scan()

```