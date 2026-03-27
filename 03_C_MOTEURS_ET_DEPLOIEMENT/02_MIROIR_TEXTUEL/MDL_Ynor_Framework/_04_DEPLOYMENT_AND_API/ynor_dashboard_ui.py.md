# MIROIR TEXTUEL - ynor_dashboard_ui.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\ynor_dashboard_ui.py
Taille : 10952 octets
SHA256 : 6440b5c07fd05a015a39fc2314c1deee23436f348b98b40ae699437d6506f789

```text
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YNOR AGI - Enterprise Governance</title>
    <style>
        :root {
            --bg-color: #09090b;
            --surface: #18181b;
            --border: #27272a;
            --text-main: #f8fafc;
            --text-muted: #a1a1aa;
            --primary: #22c55e;
            --danger: #ef4444;
            --warning: #eab308;
            --accent: #8b5cf6;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            line-height: 1.5;
            padding: 2rem;
            min-height: 100vh;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }

        .logo { font-size: 1.5rem; font-weight: 800; letter-spacing: -0.05em; color: var(--primary); }
        .badge { background: rgba(34, 197, 94, 0.1); color: var(--primary); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.875rem; font-weight: 600; border: 1px solid rgba(34, 197, 94, 0.2); animation: pulse 2s infinite;}
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }

        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }

        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2); border-color: rgba(255,255,255,0.1); }

        .metric-title { color: var(--text-muted); font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        .metric-value { font-size: 2.5rem; font-weight: 700; font-variant-numeric: tabular-nums; display: flex; align-items: baseline; gap: 0.5rem; transition: color 0.3s; }
        .metric-value.green { color: var(--primary); }
        .metric-value.red { color: var(--danger); text-shadow: 0 0 20px rgba(239, 68, 68, 0.4); }
        .metric-sub { font-size: 0.875rem; color: var(--text-muted); margin-top: 0.25rem; transition: color 0.3s; }

        .mu-equation {
            display: flex; gap: 1rem; align-items: center; justify-content: center;
            background: rgba(0,0,0,0.5); padding: 1rem; border-radius: 8px; font-family: monospace; font-size: 1.25rem;
            margin-top: 1rem; border: 1px solid var(--border); transition: border-color 0.3s;
        }
        .var-alpha { color: var(--primary); }
        .var-beta { color: var(--danger); }
        .var-kappa { color: var(--warning); }

        .controls { display: flex; gap: 1rem; margin-top: 2rem; }
        button {
            background: var(--text-main); color: var(--bg-color); border: none; padding: 0.75rem 1.5rem;
            border-radius: 6px; font-weight: 600; cursor: pointer; transition: opacity 0.2s;
        }
        button:hover { opacity: 0.9; }
        button.btn-danger { background: var(--danger); color: white; }

        .log-container {
            background: #000; border: 1px solid var(--border); border-radius: 8px;
            padding: 1rem; height: 300px; overflow-y: auto; font-family: monospace; font-size: 0.875rem;
            color: var(--text-muted); margin-top: 2rem; scroll-behavior: smooth;
        }
        .log-entry { margin-bottom: 0.5rem; border-bottom: 1px dashed #333; padding-bottom: 0.5rem; animation: fadein 0.3s; }
        .log-time { color: #555; margin-right: 8px;}
        .log-info { color: #3b82f6; }
        .log-warn { color: var(--warning); }
        .log-crit { color: var(--danger); font-weight: bold; }
        .log-success { color: var(--primary); }
        
        @keyframes fadein {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }

    </style>
</head>
<body>

    <div class="header">
        <div class="logo">YNOR.AI</div>
        <div class="badge">● LIVE TELEMETRY</div>
    </div>

    <div class="grid">
        <!-- GLOBAL MU SCORE -->
        <div class="card" id="mu-card">
            <div class="metric-title">Marge Dissipative Actuelle (μ)</div>
            <div class="metric-value green" id="mu-display">0.8500</div>
            <div class="metric-sub" id="mu-status">L'agent génère des tokens valides.</div>
            
            <div class="mu-equation" id="mu-eq-box">
                <span>μ =</span>
                <span class="var-alpha" id="val-a">α(1.0)</span> - 
                <span class="var-beta" id="val-b">β(0.1)</span> - 
                <span class="var-kappa" id="val-k">κ(0.05)</span>
            </div>
        </div>

        <!-- FINANCIALS -->
        <div class="card">
            <div class="metric-title">Savings PNL Ynor</div>
            <div class="metric-value green">$<span id="saved-money">0.00</span></div>
            <div class="metric-sub">Économisé contre les hallucinations</div>
        </div>

        <!-- ENGINE METRICS -->
        <div class="card">
            <div class="metric-title">Orchestrateur AGI</div>
            <div style="display:flex; justify-content: space-between; margin-top: 1rem;">
                <div>
                    <div style="font-size:0.75rem; color:var(--text-muted)">Système 1 (Heuristique)</div>
                    <div style="font-size:1.5rem; font-weight:700" id="sys1-count">42</div>
                </div>
                <div>
                    <div style="font-size:0.75rem; color:var(--text-muted)">Système 2 (Correction)</div>
                    <div style="font-size:1.5rem; font-weight:700; color:var(--accent)" id="sys2-count">3</div>
                </div>
            </div>
        </div>
    </div>

    <div class="log-container" id="terminal-logs">
        <div class="log-entry"><span class="log-time">[SYSTEM]</span> Initialisation Console Ynor... Prêt. Trafic API dynamique détecté.</div>
    </div>

    <script>
        // Simulation en temps réel des métriques Ynor
        let savedMoney = 142.50;
        let sys1Count = 42;
        let sys2Count = 3;
        
        function updateDashboard() {
            // Générer de nouvelles valeurs aléatoires pour simuler l'équation Ynor
            const isError = Math.random() < 0.15; // 15% de chance d'hallucination/erreur de l'agent
            
            let alpha = isError ? (Math.random() * 0.4).toFixed(4) : (0.7 + Math.random() * 0.3).toFixed(4);
            let beta = isError ? (0.5 + Math.random() * 0.5).toFixed(4) : (0.1 + Math.random() * 0.2).toFixed(4);
            let kappa = (0.05 + Math.random() * 0.15).toFixed(4);
            
            let mu = (parseFloat(alpha) - parseFloat(beta) - parseFloat(kappa)).toFixed(4);
            
            // Mise à jour de l'UI
            const muDisplay = document.getElementById('mu-display');
            const muStatus = document.getElementById('mu-status');
            const eqBox = document.getElementById('mu-eq-box');
            
            document.getElementById('val-a').innerText = `α(${alpha})`;
            document.getElementById('val-b').innerText = `β(${beta})`;
            document.getElementById('val-k').innerText = `κ(${kappa})`;
            muDisplay.innerText = mu;
            
            const logs = document.getElementById('terminal-logs');
            const now = new Date();
            const timeStr = now.getHours().toString().padStart(2, '0') + ':' + 
                          now.getMinutes().toString().padStart(2, '0') + ':' + 
                          now.getSeconds().toString().padStart(2, '0') + '.' + 
                          now.getMilliseconds().toString().padStart(3, '0');
            
            let newLog = document.createElement('div');
            newLog.className = 'log-entry';
            
            if (mu < 0) {
                // Agent is failing, saving money
                muDisplay.className = 'metric-value red';
                muStatus.innerText = "ALERTE: Divergence détectée. Requête coupée.";
                muStatus.style.color = 'var(--danger)';
                eqBox.style.borderColor = 'rgba(239, 68, 68, 0.5)';
                
                // Mettre à jour l'économie
                const savedThisTime = (Math.random() * 0.5 + 0.1).toFixed(2);
                savedMoney += parseFloat(savedThisTime);
                document.getElementById('saved-money').innerText = savedMoney.toFixed(2);
                
                sys2Count++;
                document.getElementById('sys2-count').innerText = sys2Count;
                
                newLog.innerHTML = `<span class="log-time">[${timeStr}]</span> <span class="log-crit">[INTERVENTION SYSTEM 2]</span> μ = ${mu}. Hallucination prévenue. Token API préservés (Sauvé: $${savedThisTime}).`;
            } else {
                // Agent is doing fine
                muDisplay.className = 'metric-value green';
                muStatus.innerText = "L'agent génère des tokens valides.";
                muStatus.style.color = 'var(--text-muted)';
                eqBox.style.borderColor = 'var(--border)';
                
                sys1Count++;
                document.getElementById('sys1-count').innerText = sys1Count;
                
                newLog.innerHTML = `<span class="log-time">[${timeStr}]</span> <span class="log-info">[INFERENCE SYSTEM 1]</span> μ = ${mu}. Contexte stable, alpha dominant.`;
            }
            
            // Ajouter le log en haut (prepend)
            logs.insertBefore(newLog, logs.firstChild);
            
            // Limiter le nombre de logs pour la performance (max 50)
            if (logs.children.length > 50) {
                logs.removeChild(logs.lastChild);
            }
        }

        // Lancer la boucle de simulation en temps réel (entre 800ms et 2500ms)
        function scheduleNextUpdate() {
            setTimeout(() => {
                updateDashboard();
                scheduleNextUpdate();
            }, Math.random() * 1700 + 800);
        }
        
        // Initialiser
        document.getElementById('saved-money').innerText = savedMoney.toFixed(2);
        setTimeout(scheduleNextUpdate, 1000);

    </script>
</body>
</html>
"""

```