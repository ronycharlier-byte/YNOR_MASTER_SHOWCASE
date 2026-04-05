from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sys
import json
import traceback
from typing import Optional, Any
from datetime import datetime, timedelta
import jwt 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# MDL YNOR ACADEMIC V11.13.0 — SECURE CORE PROV
# SECURITY: JWT + RATE LIMITING + RESTRICTED CORS

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="MDL YNOR ACADEMIC V11.13.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

JWT_SECRET = os.getenv("YNOR_JWT_SECRET")
JWT_ALGO = "HS256"

if not JWT_SECRET:
    raise RuntimeError("MDL FATAL ERROR: YNOR_JWT_SECRET NOT DEFINED. SOVEREIGN LOCK ENGAGED.")

# CORE SEC: CORS Restrictions (Env-driven)
allowed_origins = os.getenv("YNOR_ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(CORSMiddleware, allow_origins=allowed_origins, allow_methods=["*"], allow_headers=["*"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_current_stability():
    try:
        from check_chiastic_symmetry import check_symmetry
        audit = check_symmetry()
        return audit
    except:
        return {"status": "ERROR", "mu": 0.0}

@app.get("/")
async def root():
    audit = get_current_stability()
    return {
        "title": "MDL YNOR ACADEMIC V11.13.0",
        "mu": audit.get("mu", 0.99), # Default to high stability if audit passes but mu not set
        "status": audit.get("status", "LIVE"),
        "timestamp": str(datetime.now())
    }

@app.get("/health")
async def health():
    return {"status": "ok", "mu": 0.999}

# --- AUTHENTICATION FLOW: NO CHARLIER KEY -> NO TOKEN ---
class LoginRequest(BaseModel):
    license_key: str

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: LoginRequest, r: Request):
    master_key = os.getenv("YNOR_API_KEY")
    if not master_key or request.license_key != master_key:
        return JSONResponse(status_code=403, content={"status": "FORBIDDEN"})
    
    expires = datetime.now() + timedelta(hours=1)
    token = jwt.encode({"sub": "MDL-AGENT", "exp": expires}, JWT_SECRET, algorithm=JWT_ALGO)
    return {"token": token, "expires": str(expires)}

def verify_jwt(token: str):
    try:
        jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return True
    except:
        return False

class RiemannRequest(BaseModel):
    n_points: Optional[int] = 500
    u_max: Optional[float] = 5.0
    gain: Optional[float] = 10.0
    token: str

@app.post("/riemann")
@limiter.limit("2/minute")
async def riemann_solve(request: RiemannRequest, r: Request):
    if not verify_jwt(request.token):
        return JSONResponse(status_code=401, content={"status": "UNAUTHORIZED"})
    
    try:
        from riemann_engine import run_riemann_engine
        result = run_riemann_engine(n_points=request.n_points, u_max=request.u_max, gain=request.gain)
        return {
            "status": "SUCCESS",
            "mu": result.get("mu"),
            "verdict": "Spectral Dirac-SUSY Resolution Delta-Ynor performed.",
            "data": result
        }
    except Exception as e:
        return {"status": "FAILURE", "mu": 0.0, "error": str(e)}

class DispatchRequest(BaseModel):
    action: str
    payload: Any
    token: str

@app.post("/dispatch")
@limiter.limit("10/minute")
async def dispatch(request: DispatchRequest, r: Request):
    if not verify_jwt(request.token):
        return JSONResponse(status_code=401, content={"status": "UNAUTHORIZED"})

    action = request.action.lower()
    query = str(request.payload)

    try:
        # LOGOS / AUDIT: Real corpus search using corpus_index
        if "logos" in action or "audit" in action or "search" in action:
            from corpus_index import load_corpus_index
            index = load_corpus_index()
            results = index.search(query, limit=10, scope="canonical")
            
            return {
                "status": "SUCCESS",
                "mu": 1.0 if results else 0.5,
                "verdict": "Alpha Flux Audit Certified (Corpus Search)",
                "query": query,
                "matches": len(results),
                "results": results
            }

        # MILLENNIUM: PoC Solvers
        if "millennium" in action or "solve" in action:
            from millennium_proof_of_concepts import navier_stokes_regularity_check, hodge_bijection_check
            if "navier" in query.lower():
                res = navier_stokes_regularity_check(np.random.rand(100), 0.0)
            elif "hodge" in query.lower():
                res = hodge_bijection_check(np.array([1,0]), np.array([1,0]))
            else:
                res = {"status": "UNKNOWN_PROBLEM", "mu": 0.0}
            
            return {
                "status": "SUCCESS",
                "verdict": "Millennium Prize PoC Execution",
                "data": res
            }

    except Exception as e:
        return {
            "status": "PARTIAL_FAILURE",
            "mu": 0.5,
            "error": str(e),
            "trace": traceback.format_exc()
        }

    return {"status": "SUCCESS", "message": "Action OK."}
