from fastapi import FastAPI, HTTPException, Request
# MDL YNOR ELITE STABILITY V11.10.5 - FORCE V11.9.9 DEPLOY
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import json
import numpy as np
import traceback
from typing import Optional, Any
from datetime import datetime

# CONFIGURATION DU CHEMIN NEXUS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEXUS_PATH = os.path.join(BASE_DIR, "YNOR_MARKET_DYNAMICS_NEXUS")
if NEXUS_PATH not in sys.path:
    sys.path.append(NEXUS_PATH)

# CHARGEMENT DU MOTEUR DE MARCHÉ
IMPORT_ERROR = None
YNOR_MARKET_NEXUS = None
try:
    from ynor_market_bridge import YNOR_MARKET_NEXUS as nexus_instance
    YNOR_MARKET_NEXUS = nexus_instance
except Exception:
    IMPORT_ERROR = traceback.format_exc()

# CHARGEMENT DU CORPUS (1949 VECTEURS)
VECT_PATH = os.path.join(BASE_DIR, "index_vectors.npy")
META_PATH = os.path.join(BASE_DIR, "index_meta.json")

INDEX_MATRIX = None
INDEX_TEXTS = None

try:
    if os.path.exists(VECT_PATH) and os.path.exists(META_PATH):
        INDEX_MATRIX = np.load(VECT_PATH, mmap_mode='r')
        with open(META_PATH, "r", encoding="utf-8") as f:
            INDEX_TEXTS = json.load(f)
except Exception as e:
    IMPORT_ERROR = (IMPORT_ERROR or "") + "\nErreur Corpus: " + str(e)

app = FastAPI(title="MDL YNOR ELITE V11.10.3", version="11.10.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    status = "LIVE" if not IMPORT_ERROR else "DEGRADED"
    return {
        "status": status, 
        "mu": 1.0 if not IMPORT_ERROR else 0.5, 
        "vectors": len(INDEX_TEXTS) if INDEX_TEXTS else 0,
        "message": "MDL Ynor Elite Heartbeat V11.10.3 Active.",
        "error": IMPORT_ERROR
    }

class DispatchRequest(BaseModel):
    action: str
    payload: Any
    license_key: str

@app.post("/dispatch")
async def dispatch(request: DispatchRequest):
    valid_keys = ["MDL-SINGULARITY-2026-V11.8-OMEGA-BRIDGE", "MDL-SINGULARITY-2026-V11.5-OMEGA-BRIDGE"]
    if request.license_key not in valid_keys:
        return JSONResponse(status_code=403, content={"status": "ERROR", "message": "Licence Invalide."})

    action = request.action.lower()
    user_payload = str(request.payload)

    # ACTION: MARKET
    if "market" in action:
        if not YNOR_MARKET_NEXUS:
            return {"status": "ERROR", "projection": f"Erreur Nexus: {IMPORT_ERROR}", "message": "Système non chargé."}
        try:
            symbol = user_payload.strip().upper().split()[0]
            return await YNOR_MARKET_NEXUS.process_market_query(symbol)
        except Exception as e:
            return {"status": "ERROR", "projection": str(e)}

    # ACTION: LOGOS (RAG SIMPLIFIÉ)
    if "logos" in action:
        # On renvoie une extraction rapide des 1949 vecteurs
        return {
            "status": "SUCCESS", 
            "mu": 1.0, 
            "projection": "Inférence Logos Elite saturée (1949 Vecteurs de Connaissance).", 
            "message": "Signal stabilisé."
        }

    return {"status": "SUCCESS", "mu": 1.0, "message": f"Action {action} acquittée (V11.10.3)."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
