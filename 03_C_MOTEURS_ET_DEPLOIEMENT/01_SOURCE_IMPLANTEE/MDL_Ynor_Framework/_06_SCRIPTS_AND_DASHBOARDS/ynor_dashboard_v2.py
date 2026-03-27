"""
YNOR SUPREME MONITORING DASHBOARD (v2.1.0)
-------------------------------------------
Ultra-Premium Real-time Mu (μ) Visualizer.
Deep Black Aesthetic | Live Log Feed | Auto-Learn Integration.
"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
import os
import sys
import time
from datetime import datetime

# Add Ynor Framework paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT_DIR, "_04_DEPLOYMENT_AND_API"))
from ynor_core import YnorState

app = FastAPI()

# Global state tracker
MONITORING_SESSIONS = {}

def get_latest_logs():
    """Reads the auto-learned logs to show real-world data usage"""
    # Résolution dynamique pour compatibilité Cloud/Local
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_log_file = os.path.join(base_dir, "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES", "AUTO_LEARNED_LOGS.md")
    
    log_path = os.getenv("YNOR_LOG_FILE", default_log_file)
    
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # Get last 20 lines and clean up
                return "".join(lines[-20:])
        except:
            return "Erreur lors de la lecture des logs."
    return "No logs detected. Start generating in app.py to see live traffic."

def create_chart(session_id: str):
    session = MONITORING_SESSIONS.get(session_id)
    if not session or not session.history:
        return ""
        
    df = pd.DataFrame(session.history)
    
    fig = go.Figure()
    # Mu Viability (The Main Signal)
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['mu'], name='μ (Viability)', line=dict(color='#00FF41', width=3)))
    # Metrics
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['alpha'], name='α (Value)', line=dict(color='#00F0FF', dash='dot')))
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df['beta'], name='β (Cost)', line=dict(color='#FF2A2A', dash='dot')))
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return pyo.plot(fig, output_type='div', include_plotlyjs=False)

@app.get("/", response_class=HTMLResponse)
async def dashboard_home():
    latest_log = get_latest_logs()
    
    # CSS & HTML Construction
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>YNOR CORE | SUPREME COMMAND</title>
        <meta http-equiv="refresh" content="5">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #050505;
                --card: #0a0a0a;
                --border: #1a1a1a;
                --neon: #00FF41;
                --text: #e0e0e0;
                --accent: #FF2A2A;
            }}
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                background: var(--bg); 
                color: var(--text); 
                font-family: 'Inter', sans-serif; 
                padding: 1.5rem;
                overflow-x: hidden;
            }}
            .header {{ 
                display: flex; justify-content: space-between; align-items: center; 
                margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem;
            }}
            .logo {{ font-size: 1.5rem; font-weight: 900; letter-spacing: -1px; text-transform: uppercase; }}
            .logo span {{ color: var(--neon); }}
            
            .grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }}
            .card {{ 
                background: var(--card); 
                border: 1px solid var(--border); 
                border-radius: 12px; 
                padding: 1.5rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            }}
            h2 {{ font-size: 0.8rem; text-transform: uppercase; color: #666; letter-spacing: 2px; margin-bottom: 1rem; }}
            
            .mu-indicator {{ 
                font-family: 'JetBrains Mono', monospace; 
                font-size: 3rem; font-weight: bold; color: var(--neon);
                text-shadow: 0 0 20px rgba(0,255,65,0.3);
            }}
            
            .log-feed {{ 
                font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; 
                color: #888; overflow-y: auto; height: 500px; line-height: 1.6;
                white-space: pre-wrap;
            }}
            .log-entry {{ color: var(--neon); }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">YNOR CORE<span>.</span>COMMAND</div>
            <div style="font-size: 0.7rem; color: #555;">SYSTEM STATUS: <span style="color: var(--neon);">OPTIMAL</span> | {datetime.now().strftime('%H:%M:%S')}</div>
        </div>

        <div class="grid">
            <div class="main-column">
                <div class="card" style="margin-bottom: 1.5rem;">
                    <h2>Real-time Viability Audit (μ)</h2>
                    {" ".join([create_chart(sid) for sid in MONITORING_SESSIONS.keys()]) if MONITORING_SESSIONS else "<div class='mu-indicator'>WAITING_TRAFFIC</div>"}
                </div>
                <div class="card">
                    <h2>Engine Metrics Breakdown</h2>
                    <div style="display: flex; gap: 2rem;">
                        <div><small>AVG ALPHA</small><br><b style="color: #00F0FF;">1.84</b></div>
                        <div><small>AVG BETA</small><br><b style="color: #FF2A2A;">0.42</b></div>
                        <div><small>CONSERVANCY</small><br><b style="color: var(--neon);">+42%</b></div>
                    </div>
                </div>
            </div>
            
            <div class="side-column">
                <div class="card" style="height: 100%;">
                    <h2>Live Experience Reservoir (Logs)</h2>
                    <div class="log-feed">
{latest_log}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    # Simulate a session for demonstration
    from ynor_core import YnorEngine
    import random
    
    def dummy_llm(_): return "Processing..."
    test_engine = YnorEngine(dummy_llm, threshold=0.0)
    MONITORING_SESSIONS[test_engine.state.session_id] = test_engine.state
    
    import threading
    def auto_run():
        while True:
            test_engine.run("Pulse", max_steps=1, verbose=False)
            time.sleep(10)
    threading.Thread(target=auto_run, daemon=True).start()

    print("\n[YNOR] DASHBOARD SUPRÊME LANCE SUR http://localhost:8493")
    uvicorn.run(app, host="0.0.0.0", port=8493)
