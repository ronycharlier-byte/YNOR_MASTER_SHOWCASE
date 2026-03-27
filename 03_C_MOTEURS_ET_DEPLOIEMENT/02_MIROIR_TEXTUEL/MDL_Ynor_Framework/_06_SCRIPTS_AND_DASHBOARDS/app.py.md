# MIROIR TEXTUEL - app.py

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\app.py
Taille : 5078 octets
SHA256 : 19fc39ac24d4e3fa4d43048c58110c14965ca59868dc6f1f0a97825b3cf0a7e1

```text
import streamlit as st
from openai import OpenAI
import os
import pandas as pd
import plotly.graph_objects as go

# =========================
# YNOR LOGIC (Pure & Fast)
# =========================
class YnorState:
    def __init__(self, alpha_mult=10, beta_div=50, kappa_div=500):
        self.alpha = 0
        self.beta = 0
        self.kappa = 0
        self.alpha_mult = alpha_mult
        self.beta_div = beta_div
        self.kappa_div = kappa_div
        self.history = []

    def update(self, output, context):
        words = output.split()
        a = (len(set(words)) / (len(words) + 1e-5)) * self.alpha_mult
        b = len(words) / self.beta_div
        k = len(context.split()) / self.kappa_div
        
        self.alpha += a
        self.beta += b
        self.kappa += k
        self.history.append({"mu": self.mu, "alpha": self.alpha, "beta": self.beta, "kappa": self.kappa})

    @property
    def mu(self):
        return self.alpha - self.beta - self.kappa

# =========================
# UI SETUP
# =========================
st.set_page_config(page_title="YNOR.IO LIVE", layout="wide")

st.markdown("""
<style>
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border-left: 5px solid #ff3333; }
    h1 { color: #ff3333; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ YNOR.IO | Real-Time LLM Control")
st.write("Stop LLM wasting tokens. Mathematically.")

with st.sidebar:
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    mu_target = st.slider("Mu Threshold", -5.0, 5.0, 0.0)
    st.divider()
    st.write("μ = α - β - κ")

prompt = st.text_area("Your Prompt", "Provide a 10-step recursive analysis of the global economy.")

if st.button("RUN AUDIT"):
    if not api_key:
        st.error("Missing API Key.")
    else:
        client = OpenAI(api_key=api_key)
        state = YnorState()
        context = prompt
        outputs = []
        
        # 1. Baseline (Simulated / Est)
        with st.spinner("Baseline..."):
            base_out = client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=300).choices[0].message.content
            base_tokens = len(base_out.split())

        # 2. YNOR CORE EXECUTION
        container = st.container()
        out_col1, out_col2 = container.columns(2)
        out_col1.subheader("Baseline")
        out_col1.info(base_out)
        
        out_col2.subheader("Ynor Protected")
        ynor_ui = out_col2.empty()
        
        for i in range(10):
            chunk = client.chat.completions.create(
                model=model, 
                messages=[{"role": "user", "content": context if i==0 else f"{context}\nCONTINUE."}],
                max_tokens=150
            ).choices[0].message.content
            
            state.update(chunk, context)
            outputs.append(chunk)
            context += "\n" + chunk
            
            ynor_ui.success(" ".join(outputs))
            
            if state.mu <= mu_target:
                st.error(f"🛑 YNOR STOP : mu ({state.mu:.2f}) <= threshold")
                break
        
        # 3. STATS
        ynor_tokens = sum(len(o.split()) for o in outputs)
        gain = (1 - ynor_tokens/base_tokens) * 100
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Unchecked Cost", f"{base_tokens} tokens")
        c2.metric("Ynor Cost", f"{ynor_tokens} tokens")
        c3.metric("SAVING", f"{gain:.1f}%", delta=f"{gain:.1f}%", delta_color="normal")
        
        # 4. CHART
        df = pd.DataFrame(state.history)
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['mu'], name='Mu (Viability)', line=dict(color='#ff3333', width=4)))
        fig.update_layout(template="plotly_dark", title="Real-time Viability Drift")
        st.plotly_chart(fig, use_container_width=True)

        # 🚀 5. AUTO-LEARNING BRIDGE (DISSIPATIVE AUTO-SYNC)
        # Every run is a learning opportunity for the AGI
        import requests
        from datetime import datetime
        
        try:
            full_log = f"PROMPT: {prompt}\n\nYNOT OUTPUT: {' '.join(outputs)}"
            learn_payload = {
                "session_id": f"streamlit_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "experience_summary": full_log,
                "quality_score": gain / 100.0 if gain > 0 else 0.5
            }
            # Appel asynchrone à l'API locale Ynor pour l'auto-apprentissage
            # Note: L'API doit être lancée (Option [2] du Manager)
            requests.post(
                "http://localhost:8492/v1/archive/auto_learn", 
                json=learn_payload, 
                headers={"X-Ynor-API-Key": os.getenv("YNOR_API_KEY", "MISSING_PROD_KEY")},
                timeout=2 # Fast timeout to not block UI
            )
            st.toast("Brain Synced (Auto-Learning Active) 🧠")
        except:
            pass # Silent fail if API is offline

```