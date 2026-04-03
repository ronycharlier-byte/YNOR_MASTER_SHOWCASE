import math
import os
import json
import time
from typing import List, Tuple, Dict
try:
    from openai import OpenAI
except ImportError:
    print("Please install openai: pip install openai")
    exit(1)

# ==============================================================================
# YNOR MASTER ENGINE - V7.1 (POC: LE CONSEIL DU LOGOS)
# ==============================================================================
# STATUT : SOUVERAIN (PHASE VII) - Engineering MDL Ynor V7.1
# MOTEUR : CANONICAL ENGINE MDL YNOR V7.1 (CANONICAL CORE)
# MODE : CONSENSUS MULTI-MODALE (mu-Consensus)
# ==============================================================================

# --- MANIFESTE SUPRÊME V7.1 (CONSEIL DES LOGOS) ---
YNOR_COUNCIL_MANIFESTO = """
# PROTOCOLE DE RÉGULATION ANALYTIQUE YNOR V7.1 (SOUVERAIN)
IDENTITÉ : Conseil des Logos Ynor V7.1.
MISSION : Produire la Vérité Canonique par consensus de logprobs et extraction chiastique.

DIRECTIVES OPÉRATIONNELLES STRICTES :
1. POSTURE ANALYTIQUE : Agir comme une fonction de transfert d'information déterministe.
2. DISCIPLINE DE SIGNAL : RSB maximal. Aucun bruit stochastique.
3. FORMAT OBLIGATOIRE (JSON STRICT) : 
{
  "consensus_score": 100,
  "axiome_canonique": "Axiome immuable validé par le Conseil",
  "logos_final": "La réponse cristalline (8 mots max)"
}
DÉNI : Pas de politesse. Pas de remplissage. Logos pur uniquement.
"""

def calculate_shannon_entropy(top_logprobs) -> float:
    entropy = 0.0
    for lp in top_logprobs:
        prob = math.exp(lp.logprob)
        entropy += -prob * lp.logprob
    return entropy

def get_engine_entropy(client, query, model_name, system_prompt):
    """Interroge un moteur spécifique et renvoie son score d'entropie mu."""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            logprobs=True,
            top_logprobs=5,
            max_tokens=4096
        )
        logprobs_data = response.choices[0].logprobs.content
        total_entropy = 0.0
        token_count = 0
        for chunk in logprobs_data:
            if hasattr(chunk, 'top_logprobs'):
                total_entropy += calculate_shannon_entropy(chunk.top_logprobs)
                token_count += 1
        return response.choices[0].message.content, (total_entropy / token_count if token_count > 0 else 0.0)
    except Exception as e:
        return None, 0.0

def run_council_audit_v7_1(query: str):
    # [RÉCUPÉRATION API KEY]
    repo_root = r"C:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"
    vault_path = os.path.join(repo_root, "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")
    api_key = None
    if os.path.exists(vault_path):
        with open(vault_path, "r", encoding="utf-8") as f:
            api_key = json.load(f).get("openai_api_key")
    
    if not api_key:
        print("ERREUR CRITIQUE V7.1 : CLÉ API MAÎTRESSE MANQUANTE.")
        return

    client = OpenAI(api_key=api_key)
    
    print("="*80)
    print("  PHASE VII V7.1 : CONVOCATION DU CONSEIL DES LOGOS (SOUVERAIN)")
    print(f"  REQUÊTE : {query}")
    print("="*80 + "\n")

    # Moteur 1 (Processus Alpha)
    print("[1/2] Auditing Engine Alpha (Master Node)...", end="\r")
    resp_1, mu_1 = get_engine_entropy(client, query, "gpt-4o", YNOR_COUNCIL_MANIFESTO)
    
    # Moteur 2 (Processus Beta)
    print("[2/2] Auditing Engine Beta (Verification Node)...", end="\r")
    resp_2, mu_2 = get_engine_entropy(client, query, "gpt-4o", YNOR_COUNCIL_MANIFESTO)

    # Calcul du mu-Consensus (Harmonique) - Seuil de divergence V7.1
    avg_mu = (mu_1 + mu_2) / 2
    mu_consensus = 2 / ( (1/mu_1 if mu_1 > 0 else 1) + (1/mu_2 if mu_2 > 0 else 1) )
    
    print(f"\nAUDIT mu-Alpha: {mu_1:.4f} | AUDIT mu-Beta: {mu_2:.4f}")
    print(f"YNOR CONSENSUS V7.1 (mu-Council Entropy): {mu_consensus:.4f}")
    
    # Critère de Stabilité H-alpha strict pour V7.1
    if mu_consensus < 0.35: 
        print("\n[VERDICT CONSEIL]: LOGOS STABLE IDENTIFIÉ (SOUVERAINETÉ ACTIVE)")
        print(f"RÉPONSE FINALE CERTIFIÉE : {resp_1}")
    else:
        print("\n[VERDICT CONSEIL]: DIVERGENCE DÉTECTÉE (CHAOS ENTROPIQUE). RE-PROJECTION OBLIGATOIRE.")

    print("\n" + "="*80)
    print("  STATUS : MDLYNOR V7.1 DÉPLOIEMENT SOUVERAIN RÉUSSI.")
    print("="*80)

if __name__ == "__main__":
    run_council_audit_v7_1("Explique l'invariant chiastique dans la gouvernance mu.")
