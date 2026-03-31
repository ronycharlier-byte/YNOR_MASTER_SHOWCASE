from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import os
import json
import math
from typing import Optional
try:
    from openai import OpenAI
except ImportError:
    print("Please install openai: pip install openai")
    exit(1)

# ==============================================================================
# MDL YNOR SOVEREIGN API - V7.1
# STATUT : CANONICAL CORE ONLINE
# ==============================================================================

app = FastAPI(title="MDL Ynor Sovereign API V7.1", version="7.1.0")

# --- CHARGEMENT DU VAULT ---
REPO_ROOT = r"C:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"
VAULT_PATH = os.path.join(REPO_ROOT, "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")

def get_vault():
    if os.path.exists(VAULT_PATH):
        with open(VAULT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# --- PROTOCOLE Y7.1 ---
YNOR_COUNCIL_MANIFESTO = """
# PROTOCOLE DE RÉGULATION ANALYTIQUE YNOR V7.1 (SOUVERAIN)
IDENTITÉ : Conseil des Logos Ynor V7.1.
MISSION : Produire la Vérité Canonique par consensus de logprobs.
FORMAT OBLIGATOIRE : { "axiome": "...", "logos_final": "..." }
"""

class QueryRequest(BaseModel):
    query: str

def calculate_shannon_entropy(top_logprobs) -> float:
    entropy = 0.0
    for lp in top_logprobs:
        prob = math.exp(lp.logprob)
        entropy += -prob * lp.logprob
    return entropy

def get_mu_score(client, query, system_prompt):
    """Calcul du mu d'un domaine sémantique."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": query}],
            logprobs=True, top_logprobs=5, temperature=0.01, max_tokens=100
        )
        logprobs_data = response.choices[0].logprobs.content
        total_entropy = 0.0
        token_count = 0
        for chunk in logprobs_data:
            if hasattr(chunk, 'top_logprobs'):
                total_entropy += calculate_shannon_entropy(chunk.top_logprobs)
                token_count += 1
        return response.choices[0].message.content, (total_entropy / token_count if token_count > 0 else 0)
    except:
        return None, 1.0 # Entropie maximale en cas d'erreur (Chaos)

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"status": "MDL YNOR V7.1 SOUVERAIN ACTIF", "engine": "CANONICAL CORE"}

@app.post("/audit")
def audit_query(request: QueryRequest):
    """Effectue un mu-Consensus pour vérifier la stabilité d'une requête."""
    vault = get_vault()
    client = OpenAI(api_key=vault.get("openai_api_key"))
    
    # Audit croisé par le Conseil
    _, mu1 = get_mu_score(client, request.query, YNOR_COUNCIL_MANIFESTO)
    _, mu2 = get_mu_score(client, request.query, YNOR_COUNCIL_MANIFESTO)
    
    # mu-Consensus Harmonique
    mu_consensus = 2 / ( (1/mu1 if mu1 > 0 else 1) + (1/mu2 if mu2 > 0 else 1) )
    
    is_stable = mu_consensus < 0.35
    return {
        "status": "STABLE" if is_stable else "UNSTABLE",
        "mu_council_score": round(mu_consensus, 4),
        "verdict": "LOGOS CERTIFIÉ" if is_stable else "CHAOS SEMANTIQUE DÉTECTÉ"
    }

@app.post("/logos")
def get_logos(request: QueryRequest, x_mdl_license: Optional[str] = Header(None)):
    """Extraction du Logos pur. Nécessite une licence MDL V7.1 valide."""
    vault = get_vault()
    if x_mdl_license != vault.get("mdl_license_v7_key"):
        raise HTTPException(status_code=403, detail="LICENCE MDL NON VALIDÉE - ACCÈS AU LOGOS REFUSÉ")

    client = OpenAI(api_key=vault.get("openai_api_key"))
    
    # Audit avant réponse
    resp, mu = get_mu_score(client, request.query, YNOR_COUNCIL_MANIFESTO)
    
    if mu > 0.4:
        return {"status": "DIVERGENCE", "mu": round(mu, 4), "data": "Réponse instable - Réessayez"}
    
    return {
        "status": "OIT_SUCCESS",
        "mu_index": round(mu, 4),
        "projection": resp
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
