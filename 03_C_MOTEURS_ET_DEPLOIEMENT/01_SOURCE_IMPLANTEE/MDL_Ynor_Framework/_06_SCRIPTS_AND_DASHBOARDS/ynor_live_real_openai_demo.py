"""
YNOR LIVE REAL OPENAI DEMO (v1.0.0)
----------------------------------
Démonstration en temps-réel utilisant l'API OpenAI (GPT-4o-mini).
Compare une exécution standard brute face à la gouvernance Ynor.
"""
import streamlit as st
import os
import sys
from openai import OpenAI

# SDK Integration (pour les comptages de tokens précis)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '_04_DEPLOYMENT_AND_API')))
try:
    from ynor_core.metrics import get_token_count
except ImportError:
    def get_token_count(text): return len(text.split())

# Configuration UI
st.set_page_config(page_title="Ynor Live | Real-Time OpenAI Audit", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# =========================
# YNOR LOGIC (Vitesse Maximale)
# =========================

class YnorState:
    def __init__(self):
        self.alpha = 0
        self.beta = 0
        self.kappa = 0
        self.history = []

    def update(self, a, b, k):
        self.alpha += a
        self.beta += b
        self.kappa += k

    @property
    def mu(self):
        # Marge dissipative simple pour la démo
        return self.alpha - self.beta - self.kappa

def measure_alpha(output):
    # Proxy : Densité d'information unique
    words = output.split()
    if not words: return 0
    return (len(set(words)) / len(words)) * 10 

# =========================
# UI SIDEBAR
# =========================
with st.sidebar:
    st.title("🛡️ Ynor Control")
    api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model_choice = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    mu_threshold = st.slider("Mu Threshold (Stop point)", -5.0, 5.0, 0.0)
    st.divider()
    st.info("Cette démo compare une exécution standard à une exécution protégée par Ynor.")

# =========================
# MAIN APP
# =========================
st.markdown("# 🚀 YNOR LIVE : OpenAI Real-Time Audit")
st.write("Démontrez l'arrêt intelligent et l'économie de coûts sur de vrais prompts.")

user_prompt = st.text_area("Entrez un prompt complexe (ex: raisonnement itératif, rédaction longue)", 
                         "Effectue une analyse itérative détaillée de l'impact de l'IA sur l'économie mondiale en 10 étapes.")

if st.button("Lancer la Démo Comparative"):
    if not api_key:
        st.error("Veuillez fournir une clé API OpenAI dans la barre latérale.")
    else:
        client = OpenAI(api_key=api_key)
        
        # --- 1. BASELINE ---
        with st.status("Exécution Baseline (Standart)..."):
            res_base = client.chat.completions.create(
                model=model_choice,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=300
            ).choices[0].message.content
            tokens_base = get_token_count(res_base)

        # --- 2. YNOR GUARDED ---
        with st.status("Exécution YNOR Core (Live Audit)..."):
            state = YnorState()
            context = user_prompt
            ynor_outputs = []
            mu_trace = []
            
            # Simulation multi-étapes ou génération contrôlée
            # Pour la démo, on simule une boucle de réflexion / génération atomique
            for step in range(8):
                chunk = client.chat.completions.create(
                    model=model_choice,
                    messages=[{"role": "user", "content": context if step == 0 else f"{context}\nPRODUIS L'ÉTAPE SUIVANTE EN DÉTAIL."}],
                    max_tokens=150
                ).choices[0].message.content
                
                # Mesures Ynor
                a = measure_alpha(chunk)
                b = get_token_count(chunk) / 50 # Coût normalisé
                k = get_token_count(context) / 500 # Inertie
                
                state.update(a, b, k)
                mu_trace.append(state.mu)
                
                ynor_outputs.append(chunk)
                context += "\n" + chunk
                
                if state.mu <= mu_threshold:
                    st.warning(f"🛑 YNOR STOP : Marge mu épuisée à l'étape {step+1} (mu={state.mu:.2f})")
                    break
        
        # --- DISPLAY RESULTS ---
        st.divider()
        col_out1, col_out2 = st.columns(2)
        
        with col_out1:
            st.subheader("Baseline Output")
            st.info(res_base[:500] + "...")
            st.metric("Tokens Baseline", tokens_base)
            
        with col_out2:
            st.subheader("Ynor Output")
            st.success(" ".join(ynor_outputs)[:500] + "...")
            ynor_tokens = sum(get_token_count(o) for o in ynor_outputs)
            st.metric("Tokens Ynor", ynor_tokens, delta=f"{(1 - ynor_tokens/tokens_base)*100:.1f}% saving")

        # Visualisation
        st.subheader("Graphique de Gouvernance mu(t)")
        if mu_trace:
            st.line_chart(mu_trace)
            st.caption("La génération s'arrête dès que la courbe rouge descend sous le seuil défini.")
        
        st.balloons()
