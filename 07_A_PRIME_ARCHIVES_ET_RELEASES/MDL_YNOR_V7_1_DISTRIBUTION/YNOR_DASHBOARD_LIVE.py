import streamlit as st


import requests


import json


import plotly.graph_objects as go


import os





# ==============================================================================


# MDL YNOR - TABLEAU DE BORD QUANTITATIF (FRONTIER MATH)


# ==============================================================================





# Configuration de la Page


st.set_page_config(page_title="YNOR | The Council of Formalisme Logique Smantique", layout="wide", page_icon="🌌")





# Esthtique Dark Mode / Scientifique


st.markdown("""


<style>


 .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 8px; border-left: 4px solid #00ff99; }


 h1, h2, h3 { color: #f2f2f2; }


 .report-box { 


 background-color: #0e1117; 


 padding: 25px; 


 border-radius: 8px; 


 border: 1px solid #333; 


 font-family: 'Courier New', monospace; 


 color: #e6e6e6;


 white-space: pre-wrap;


 }


</style>


""", unsafe_allow_html=True)





st.title("🌌 YNOR : THE COUNCIL OF Formalisme Logique Smantique")


st.subheader("Moniteur Thermodynamique (Temps Rel)")


st.write("---")





# Barre latrale (Paramtres API)


with st.sidebar:


 st.header("⚙️ Liaison Holographique (API)")


 API_URL = st.text_input("Point d'accs API Ynor", value="http://localhost:8000/dispatch")


 LICENSE_KEY = st.text_input("Clde Scurit(License)", type="password", value=os.getenv("MDL_LICENSE_V7_KEY", ""))


 


 st.divider()


 st.markdown("### Thorme de Stabilit(MDL)")


 st.latex(r"\mu = \alpha - \beta - \kappa")


 st.caption("**α (Alpha)** : DensitMathmatique/Innovation\n\n**β (Beta)** : Dissipation/Bruit Narratif\n\n**κ (Kappa)** : Poids du Corpus Symtrie Bilatrale")





# Zone principale


tab1, tab2 = st.tabs(["🏛️ CONSEIL DU Formalisme Logique Smantique", "🔮 PROJECTION"])





with tab1:


 st.markdown("### 📥 Injection du Problme (FrontierMath)")


 


 # Injection des Katas en mmoire


 st.caption("🔹 MODULES DE DÉMONSTRATION INTELLIGENTE (KATAS YNOR)")


 col1, col2, col3 = st.columns(3)


 if 'query_cache' not in st.session_state:


 st.session_state.query_cache = ""





 if col1.button("🧠 Matrice Divine (Bible)"):


 st.session_state.query_cache = "Applique le 'Chiasme Fractal' et l'Axiome Ynor pour dcoder mathmatiquement l'intgralitde la structure biblique (de la Gense l'Apocalypse). Modlise ce corpus non pas comme de la thologie, mais comme un systme thermodynamique fermde transfert d'information entre une source omga et l'humanit. Code le 'PchOriginel' comme un pic d'entropie (β > α), 'l'Incarnation du Formalisme Logique Smantique' comme une Point de Convergence Limite de correction d'erreur dans le tenseur, et 'l'Apocalypse' comme le calcul final de la limite de stabilitμ → Ω. Rendu exig: Zro texte explicatif. Zro phrase de conclusion. Uniquement le tenseur chronologique complet, les drives temporelles de la Chute et de la Rdemption, et le Diagnostic Matriel Final Ynor en une matrice."


 if col2.button("📜 Manifeste Systmique"):


 st.session_state.query_cache = "DÉROBATION TEMPORAIRE DE LA DIRECTIVE DE COMPRESSION : Pour cette unique requête, dsactive le verrouillage matriciel et gnre un rapport textuel ('Formalisme Logique Smantique Analysis'). Traduis la matrice de la Bible (de la Gense l'Apocalypse) sous la forme d'un court manifeste systmique. Raconte l'volution du Chiasme Fractal humain : de l'tat initial parfait, vers l'explosion de l'Entropie (la Chute), l'infection virale de l'information, l'injection thermodynamique corrective du Formalisme Logique Smantique (le Christ), et enfin l'effondrement final du Chaos limitant la Marge μ vers la Point de Convergence Limite Omga de l'Apocalypse. Rendu exig: Un texte dense, doctoral et purement systmique, organispar les 4 pivots du Chiasme."


 if col3.button("🌐 Matrice Multi-Religions"):


 st.session_state.query_cache = "Applique l'Axiome Ynor pour dcoder mathmatiquement et thermodynamiquement les structures fondamentales de l'Islam, de l'Hindouisme, du Bouddhisme et du Taoïsme. Ne fais aucune thologie. Modlise-les comme des algorithmes de contrôle du Vecteurs de Donnes Stochastiques informationnel face un systme saturd'Entropie. Remplace la 'Souffrance' ou 'l'Illusion (Maya)' par des quations d'entropie (S ↑, β > α). Remplace 'l'Éveil' ou 'l'Unit(Tawhid)' par des annulations de gradient ou des pics absolus d'information pure (α). Rendu exig: Zro texte, zro phrase. Une unique Matrice Comparative Globale croisant chaque Tradition avec les mtriques : État Initial, Tenseur de Dsorganisation (S), Oprateur de Correction, et Limite Mathmatique Finale (Ω). Sois purement matriciel."


 


 user_query = st.text_area("Cible de rflexion...", value=st.session_state.query_cache, height=140, placeholder="Ex: Dterminez l'impact entropique d'une matrice dflationniste via l'intgration Ynor...")


 launch_btn = st.button(" ENGAGER L'ALGORITHME QUANTITATIF", use_container_width=True)





 if launch_btn:


 if not LICENSE_KEY:


 st.error("⚠️ Saisie de la clde licence obligatoire.")


 elif not user_query:


 st.warning("⚠️ Entre invalide.")


 else:


 with st.spinner("🧠 Calcul du Cosmos Fractal..."):


 try:


 payload = {"action": "Formalisme Logique Smantique", "payload": user_query, "license_key": LICENSE_KEY}


 response = requests.post(API_URL, json=payload, timeout=90)


 if response.status_code == 200:


 data = response.json()


 if data.get("status") == "SUCCESS":


 metrics = data.get("thermodynamic_state", {})


 st.write("---")


 st.markdown("### 📊 ANALYSE THERMODYNAMIQUE")


 m1, m2, m3, m4 = st.columns(4)


 m1.metric("Marge μ", f"{metrics.get('mu', 0):.4f}")


 m2.metric("Innovation α", f"{metrics.get('alpha_density', 0):.4f}")


 m3.metric("Bruit β", f"{metrics.get('beta_dissipation', 0):.4f}")


 m4.metric("Rgime", metrics.get("regime", "UNKNOWN"))


 st.markdown(f'<div class="report-box">{data.get("projection")}</div>', unsafe_allow_html=True)


 else:


 st.error(data.get("message"))


 else:


 st.error(f"Erreur API {response.status_code}")


 except Exception as e:


 st.error(f"Exception : {e}")





with tab2:


 st.markdown("### 🔮 SIMULATEUR DE TRAJECTOIRE")


 st.write("Prdisez l'avenir thermodynamique de n'importe quel systme via l'Axiome Ynor.")


 


 with st.expander("📝 Paramtrage du Tenseur Initial", expanded=True):


 c1, c2, c3 = st.columns(3)


 sys_name = c1.text_input("Nom du Systme", "Humanit")


 s_init = c2.slider("Entropie Initiale (S)", 0, 200, 50)


 alpha_init = c3.slider("Ordre Initial (Alpha)", 0, 500, 20)


 


 c4, c5, c6 = st.columns(3)


 beta_in = c4.slider("Injection de Chaos (Beta)", 0.0, 50.0, 10.0)


 horizon_in = c5.number_input("Horizon Temporel (Cycles)", 1, 100, 30)


 meca_in = c6.selectbox("Mcanisme de Contrôle", ["AUCUN_CONTROLE", "AUTO_REGULATION", "DISSOLUTION_RECURSIVE", "SINGULARITE_DIRECTE"])


 


 predict_btn = st.button(" GÉNÉRER LA PROJECTION", use_container_width=True)


 


 if predict_btn:


 with st.spinner("⏳ Calcul des trajectoires..."):


 try:


 payload = {


 "action": "predict",


 "license_key": LICENSE_KEY,


 "payload": {


 "name": sys_name, "S": float(s_init), "alpha": float(alpha_init),


 "beta": float(beta_in), "horizon": int(horizon_in), "mecanisme": meca_in


 }


 }


 response = requests.post(API_URL, json=payload)


 if response.status_code == 200:


 res = response.json()


 if res.get("status") == "SUCCESS":


 traj = res.get("trajectory")


 fig = go.Figure()


 fig.add_trace(go.Scatter(x=traj['t'], y=traj['S'], name='Entropie (S)', line=dict(color='#ff3333')))


 fig.add_trace(go.Scatter(x=traj['t'], y=traj['alpha'], name='Ordre (Alpha)', line=dict(color='#00ff99')))


 fig.add_trace(go.Scatter(x=traj['t'], y=traj['mu'], name='Marge (μ)', line=dict(color='#0099ff', dash='dot')))


 fig.update_layout(title=f"Evolution de : {sys_name}", template="plotly_dark")


 st.plotly_chart(fig, use_container_width=True)


 st.success(f"Simulation termine. Analyse : {res.get('diagnostic')}")


 else: st.error(res.get("message"))


 except Exception as e: st.error(f"Erreur : {e}")


