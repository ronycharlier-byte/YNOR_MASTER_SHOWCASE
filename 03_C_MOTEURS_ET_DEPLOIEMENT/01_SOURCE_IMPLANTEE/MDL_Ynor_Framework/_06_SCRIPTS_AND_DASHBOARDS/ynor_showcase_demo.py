"""
YNOR.IO SHOWCASE SUPREME (v2.0.0)
---------------------------------
Premium Landing Page + Live Engine Demo.
Aesthetic: Deep Black / Neon Green / High-Performance Data.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import os
import sys
from datetime import datetime

# SDK Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_04_DEPLOYMENT_AND_API')))
try:
    from ynor_core import YnorEngine, get_token_count
except ImportError:
    st.error("YNOR SDK not found.")

# --- UI CONFIG ---
st.set_page_config(page_title="YNOR.IO | The Decision Layer", layout="wide", initial_sidebar_state="collapsed")

# CUSTOM CSS (PREMIUM DARK MODE)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Inter:wght@400;900&display=swap');
    
    .stApp { background-color: #000000; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 900; color: white !important; letter-spacing: -2px; }
    p, span { font-family: 'Inter', sans-serif; color: #888; }
    
    .hero-container { text-align: center; padding: 5rem 0; border-bottom: 1px solid #111; }
    .hero-title { font-size: 5rem; margin-bottom: 0px; }
    .hero-gradient { background: linear-gradient(90deg, #00FF41, #00F0FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    
    .metric-card { 
        background-color: #050505; border: 1px solid #111; border-radius: 15px; 
        padding: 2rem; text-align: center; transition: all 0.3s ease;
    }
    .metric-card:hover { border-color: #00FF41; transform: translateY(-5px); }
    .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 3.5rem; color: #00FF41; font-weight: bold; }
    
    .terminal { 
        background-color: #050505; border: 1px solid #111; border-radius: 10px; 
        padding: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #00FF41;
        height: 300px; overflow-y: auto; box-shadow: inset 0 0 20px rgba(0,0,0,1);
    }
    
    .stButton>button { 
        background: white; color: black; border-radius: 50px; font-weight: 900; 
        height: 4rem; text-transform: uppercase; letter-spacing: 2px; border: none;
    }
    .stButton>button:hover { background: #00FF41; color: black; }
    
    .equation-box { 
        background: #030303; border: 1px solid #111; border-radius: 20px; 
        padding: 2.5rem; margin: 3rem 0; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
<div class="hero-container">
    <p style="text-transform:uppercase; letter-spacing:5px; color:#444; margin-bottom:1rem;">Closed-IP Decision Engine</p>
    <h1 class="hero-title">LLMs <span style="color:#FF3333;">Hallucinate.</span></h1>
    <h1 class="hero-title" style="margin-top:-30px;">YNOR <span class="hero-gradient">Decides.</span></h1>
    <p style="font-size:1.5rem; max-width:800px; margin:2rem auto; color:#666;">
        The first operational stopping layer for AI agents. 
        Mathematically halting unviable inference before it costs you a fortune.
    </p>
</div>
""", unsafe_allow_html=True)

# --- THE EQUATION ---
st.markdown("""
<div class="equation-box">
    <h3 style="color:#444 !important; font-size:0.8rem; margin-bottom:1.5rem; text-transform:uppercase;">Master Viability Formula</h3>
    <h1 style="font-size:4rem; font-family:'JetBrains Mono';">μ = α − β − κ</h1>
    <p style="margin-top:1rem; color:#444;">Value Density (α) minus Operational Cost (β) minus Context Burden (κ)</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- LIVE DEMO ---
st.header("🕹️ Live Engine Stress-Test")
st.write("Simulate any LLM failure pattern and watch Ynor intercept the drift.")

c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.subheader("Input & Logic")
    scenario = st.selectbox("Failure Scenario", ["Dégénérescence Répétitive", "Boucle Infinie", "Bruit Verbeux (Hallucination)"])
    mu_lim = st.slider("Mu Threshold (SENSITIVITY)", -2.0, 2.0, 0.0, step=0.1)
    test_btn = st.button("RUN DISSIPATION TEST")

with c2:
    st.subheader("System Status")
    st.markdown("""
    <div style="display:flex; gap:1rem; margin-bottom:2rem;">
        <div style="background:#050505; border:1px solid #111; padding:15px; border-radius:10px; flex:1;">
            <small>CORE ENGINE</small><br><b style="color:#00FF41;">OPERATIONAL</b>
        </div>
        <div style="background:#050505; border:1px solid #111; padding:15px; border-radius:10px; flex:1;">
            <small>AUTO-LEARN</small><br><b style="color:#00FF41;">ACTIVE</b>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.info("The indexer is ready. Every generation will be archived for self-improvement.")

# --- SIMULATION LOGIC ---
if test_btn:
    st.divider()
    
    # 1. Mocking behavior based on scenario
    def mock_logic(c): 
        if scenario == "Dégénérescence Répétitive": return "REPETITION " * 5 + f" of node {len(c)}"
        if scenario == "Boucle Infinie": return "I am continuing my explanation to explain " + c[-10:]
        return "Bla " * 20 + " [Irrelevant Content] " + str(datetime.now())

    engine = YnorEngine(mock_logic, threshold=mu_lim)
    
    # Live Display
    t1, t2 = st.columns(2)
    t1.subheader("Standard (No Guard)")
    t2.subheader("YNOR.IO (Protected)")
    
    win1 = t1.empty()
    win2 = t2.empty()
    
    base_text = ""
    ynor_chunks = []
    
    for i in range(12):
        # Baseline
        base_text += mock_logic(base_text) + "\n"
        win1.markdown(f"<div class='terminal' style='color:#555;'>{base_text}</div>", unsafe_allow_html=True)
        
        # Ynor
        if not engine.state.mu <= mu_lim:
            res = engine.run("Test", max_steps=1, verbose=False)
            if res: ynor_chunks.append(res[0])
            win2.markdown(f"<div class='terminal'>{(' '.join(ynor_chunks))}</div>", unsafe_allow_html=True)
        else:
            win2.markdown(f"<div class='terminal' style='color:#FF3333;'>🛑 YNOR HALT INJECTED<br>Reason: Mu Viability Zeroed Out.<br>Saving active tokens.</div>", unsafe_allow_html=True)
            break
        time.sleep(0.3)
    
    # Stats
    st.markdown("### 📊 Performance Proof")
    m1, m2, m3 = st.columns(3)
    savings = (1 - len(" ".join(ynor_chunks))/len(base_text)) * 100
    m1.markdown(f'<div class="metric-card"><small>COST SAVINGS</small><br><span class="metric-val">{savings:.1f}%</span></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="metric-card"><small>DISSIPATION STEP</small><br><span class="metric-val">{len(ynor_chunks)}</span></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="metric-card"><small>FINAL μ</small><br><span class="metric-val">{engine.state.mu:.2f}</span></div>', unsafe_allow_html=True)

    # 📈 Chart
    df = pd.DataFrame(engine.state.history)
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['mu'], name='Mu (Viability)', line=dict(color='#00FF41', width=5)))
    fig.add_trace(go.Scatter(y=df['alpha'], name='Alpha (Value)', line=dict(color='#00F0FF', dash='dot')))
    fig.update_layout(template="plotly_dark", plot_bgcolor='#000', paper_bgcolor='#000', margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("<p style='text-align:center; color:#222; margin-top:5rem;'>© 2026 MDL Ynor Architecture | Sovereign AI Intelligence | Managed by Charlier Rony</p>", unsafe_allow_html=True)
