# MIROIR TEXTUEL - streamlit_dashboard.py

Source : MDL_Ynor_Framework\_06_SCRIPTS_AND_DASHBOARDS\streamlit_dashboard.py
Taille : 1807 octets
SHA256 : 499e21b9bfe3d0d87bc9188d989f56f910f7ab12cd27fbb8c6d2c467ae34e82a

```text
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Charge les secrets (API Key)
load_dotenv()
API_KEY = os.getenv("YNOR_API_KEY", "MISSING_PROD_KEY")

st.set_page_config(page_title="YNOR AGI Terminal", layout="centered")

st.title(" YNOR AGI - Terminal Deploiement")
st.markdown("Interface utilisateur connectee a l'API *Ynor Cognitive Engine* (Port 8492).")

user_input = st.text_input("Requete a l'AGI :", "Analyse les modeles emergents du web.")

if st.button("RUN YNOR COGNITIVE ENGINE"):
    with st.spinner("L'AGI Ynor percoit, decide, agit..."):
        try:
            # Appel a l'API Ynor officielle sur le port 8492
            headers = {"X-Ynor-API-Key": API_KEY}
            res = requests.post("http://localhost:8492/run", json={"input": user_input}, headers=headers)
            
            if res.status_code == 200:
                data = res.json()
                st.success("Tache terminee avec succes")
                st.subheader("Decision du Meta-Controller :")
                st.write(f" **Outil utilise** : `{data['cognitive_tool_selected'].upper()}`")
                
                # Extraction des resultats imbriques
                results = data['action_result']
                st.subheader("Retour Environnement :")
                st.info(results['response'])
                
                st.divider()
                st.write(f"**Viabilite ** : `{results['mu']}`")
                st.write(f"**Systeme utilise** : `{results['system_used']}`")
            else:
                st.error(f"Erreur API ({res.status_code}) : {res.text}")
        except Exception as e:
            st.error(f"Serveur API injoignable sur le port 8492. Verifiez que `ynor_api_server.py` est lance.\nException: {e}")

```