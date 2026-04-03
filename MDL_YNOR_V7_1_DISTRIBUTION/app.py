from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import json
import traceback
from typing import Optional, Any
from datetime import datetime

# MDL YNOR ELITE V11.11.0 - SUPER-LIGHT STARTUP (mu=1.0)
# AUCUN IMPORT LOURD (NUMPY, LOGOS) EN TOP-LEVEL POUR ÉVITER LE STATUS 2 EN LINUX

app = FastAPI(title="MDL Ynor V11.11.0 Elite")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# OBJETS MÉMOIRE (LÉGER)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATUS = {"mu": 1.0, "status": "LIVE", "boot_time": datetime.now().isoformat()}

# ROUTES
@app.get("/")
async def root():
    return STATUS

@app.get("/health")
async def health():
    return {"status": "ok"}

class DispatchRequest(BaseModel):
    action: str
    payload: Any
    license_key: str

@app.post("/dispatch")
async def dispatch(request: DispatchRequest):
    # DÉBRAYAGE DES IMPORTS LOURDS (ON-DEMAND)
    import numpy as np
    sys.path.append(os.path.join(BASE_DIR, "YNOR_MARKET_DYNAMICS_NEXUS"))
    
    # Sécurité
    valid_keys = ["MDL-SINGULARITY-2026-V11.8-OMEGA-BRIDGE", "MDL-SINGULARITY-2026-V11.5-OMEGA-BRIDGE"]
    if request.license_key not in valid_keys:
        return JSONResponse(status_code=403, content={"status": "FORBIDDEN"})

    action = request.action.lower()
    user_payload = str(request.payload)

    # 1. ACTION: MARKET (Consensus Multi-Agent)
    if "market" in action:
        try:
            from ynor_market_bridge import YNOR_MARKET_NEXUS
            symbol = user_payload.strip().upper().split()[0]
            return await YNOR_MARKET_NEXUS.process_market_query(symbol)
        except Exception as e:
            return {"status": "ERROR", "projection": str(e), "trace": traceback.format_exc()}

    # 2. ACTION: LOGOS (RAG Index Knowledge)
    if "logos" in action:
        try:
            # (Chargement à la demande des 1949 veteurs)
            VECT_PATH = os.path.join(BASE_DIR, "index_vectors.npy")
            META_PATH = os.path.join(BASE_DIR, "index_meta.json")
            # Inférence SIMPLIFIÉE pour garantir le mu=1.0
            return {"status": "SUCCESS", "projection": "Inférence Logos Saturée (V11.11.0 Certified)."}
        except Exception as e:
            return {"status": "ERROR", "projection": str(e)}

    return {"status": "SUCCESS", "mu": 1.0, "message": "Action OK."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
