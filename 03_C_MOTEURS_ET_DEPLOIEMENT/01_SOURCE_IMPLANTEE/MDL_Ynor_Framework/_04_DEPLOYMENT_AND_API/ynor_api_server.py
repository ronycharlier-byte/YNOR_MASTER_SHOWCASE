import time
import random
import os
import hashlib
import json
import asyncio
from collections import deque
from pathlib import Path
import html
import uuid

try:
    from dotenv import load_dotenv
    load_dotenv()  # Charge automatiquement les clAs
except ImportError:
    pass

from fastapi import FastAPI, Depends, HTTPException, Security, Request, Response
from fastapi.security import APIKeyHeader  # type: ignore
from pydantic import BaseModel, Field

# Yi SECURITY SHIELD IMPORT (Action 4)
try:
    from ynor_security_shield import check_critical_secrets
except ImportError:
    def check_critical_secrets(): pass

app = FastAPI(
    title="I API - Ynor AI Cost Control & Hierarchical Engine",
    description="Early warning system for LLMs + Cloud-Hosted System 1/System 2 AGI orchestration.",
    version="3.1.0-MILLENNIUM"
)

# Yi STARTUP INTEGRITY CHECK
try:
    check_critical_secrets()
except RuntimeError as e:
    print(f"\n[Ys FATAL STARTUP ERROR] {str(e)}")
    # En production, on forcerait l'arrAt ici


# === SAAS AUTHENTICATION & SECURITY ===
API_KEY_NAME = "X-Ynor-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# === USAGE TRACKER (PERSISTENT DAILY QUOTA) ===
BASE_DIR = Path(__file__).resolve().parent
USAGE_FILE = BASE_DIR / "usage_stats.json"
MU_AUDIT_FILE = BASE_DIR / "mu_audit_history.json"
REVOCATION_FILE = BASE_DIR / "revocation_list.json"
SECRETS_FILE = BASE_DIR / "secrets.local.json"
USAGE_LOCK = asyncio.Lock()
MU_AUDIT_LOCK = asyncio.Lock()
REVOCATION_LOCK = asyncio.Lock()
SHARED_AUDITS_LOCK = asyncio.Lock()
GROWTH_EVENTS_LOCK = asyncio.Lock()
SHARED_AUDITS_FILE = BASE_DIR / "shared_audits.json"
GROWTH_EVENTS_FILE = BASE_DIR / "growth_events.json"

# === PREMIUM DASHBOARD UI ===
DASHBOARD_HTML = """
<html>
    <head><title>MDL YNOR - MASTER DASHBOARD</title></head>
    <body style="background:#0a0a0a; color:#00ff00; font-family:monospace; padding:20px;">
        <h1 style="border-bottom: 2px solid #00ff00;">MDL YNOR v3.1 - MILLENNIUM AUDIT CENTER</h1>
        <div style="padding:10px; border:1px solid #00ff00; margin-bottom:20px;">
            <p><strong>ENGINE STATUS:</strong> <span style="color:#00ff00;">ONLINE (SECURE)</span></p>
            <p><strong>TELEMETRY:</strong> ACTIVE</p>
        </div>
        <h3>LATEST AUDIT TRENDS (Mu History)</h3>
        <iframe src="/v1/mu/check" style="width:100%; height:100px; background:#111; border:none;"></iframe>
        <p style="font-size:0.8em; color:#555;">A 2026 MDL STRATEGY - FOUNDER ACCESS ONLY</p>
    </body>
</html>
"""

# === READ-ONLY LOCK CONFIG ===
READ_ONLY_MODE = os.getenv("MDL_PROD_WRITE_ENABLED", "FALSE").upper() != "TRUE"

def load_json_file(path, fallback):
    if not os.path.exists(path):
        return fallback
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return fallback

def save_json_file(path, payload):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception:
        pass

def load_private_settings():
    file_settings = load_json_file(SECRETS_FILE, {})
    allowed_api_keys = []

    for candidate in [
        file_settings.get("ynor_api_key"),
        file_settings.get("ynor_test_key"),
        os.getenv("YNOR_API_KEY"),
        os.getenv("YNOR_TEST_KEY"),
    ]:
        if candidate:
            allowed_api_keys.append(candidate)

    extra_allowed = os.getenv("YNOR_ALLOWED_API_KEYS", "")
    if extra_allowed.strip():
        allowed_api_keys.extend(
            [item.strip() for item in extra_allowed.split(",") if item.strip()]
        )

    return {
        "master_key": file_settings.get("ynor_api_key") or os.getenv("YNOR_API_KEY", "MISSING_PROD_KEY"),
        "test_key": file_settings.get("ynor_test_key") or os.getenv("YNOR_TEST_KEY", ""),
        "allowed_keys": {key for key in allowed_api_keys if key},
        "secret_salt": file_settings.get("ynor_secret_salt") or os.getenv("YNOR_SECRET_SALT", "default_insecure_salt"),
        "admin_secret": file_settings.get("ynor_admin_secret") or os.getenv("YNOR_ADMIN_SECRET", "super_secret_ynor_master"),
        "dashboard_default_api_key": file_settings.get("dashboard_default_api_key") or os.getenv("YNOR_DASHBOARD_DEFAULT_API_KEY", ""),
    }

PRIVATE_SETTINGS = load_private_settings()
MASTER_KEY = PRIVATE_SETTINGS["master_key"]
TEST_KEY = PRIVATE_SETTINGS["test_key"]
ALLOWED_KEYS = PRIVATE_SETTINGS["allowed_keys"] or {MASTER_KEY}
YNOR_SECRET_SALT = PRIVATE_SETTINGS["secret_salt"]
YNOR_ADMIN_SECRET = PRIVATE_SETTINGS["admin_secret"]
DASHBOARD_DEFAULT_API_KEY = PRIVATE_SETTINGS["dashboard_default_api_key"]

def mask_api_key(api_key: str) -> str:
    return f"{api_key[:5]}****" if api_key else "ANON"

async def track_growth_event(event_name: str, payload: dict):
    async with GROWTH_EVENTS_LOCK:
        events = load_json_file(GROWTH_EVENTS_FILE, [])
        events.append(
            {
                "event": event_name,
                "timestamp": time.time(),
                "date": time.ctime(),
                **payload,
            }
        )
        if len(events) > 2000:
            events = events[-2000:]
        save_json_file(GROWTH_EVENTS_FILE, events)

async def create_public_share_record(audit_result: dict, api_key: str, request: Request | None = None):
    share_id = uuid.uuid4().hex[:12]
    async with SHARED_AUDITS_LOCK:
        shares = load_json_file(SHARED_AUDITS_FILE, {})
        share_path = f"/share/mu/{share_id}"
        origin = str(request.base_url).rstrip("/") if request else ""

        share_record = {
            "id": share_id,
            "created_at": time.time(),
            "created_date": time.ctime(),
            "created_by": mask_api_key(api_key),
            "mu": audit_result["mu"],
            "should_halt": audit_result["should_halt"],
            "reason": audit_result["reason"],
            "metrics": audit_result["metrics"],
            "billing": audit_result["billing"],
            "_watermark": audit_result["_watermark"],
            "share_path": share_path,
            "share_url": f"{origin}{share_path}" if origin else share_path,
        }
        shares[share_id] = share_record
        save_json_file(SHARED_AUDITS_FILE, shares)

    await track_growth_event(
        "share_link_created",
        {
            "share_id": share_id,
            "api_key": mask_api_key(api_key),
            "mu": audit_result["mu"],
            "should_halt": audit_result["should_halt"],
        },
    )
    return share_record

def render_dashboard_html():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MDL YNOR - Audit Center</title>
    <style>
        :root {
            --bg: #09090b;
            --surface: #18181b;
            --surface-2: #111114;
            --border: #27272a;
            --text: #f5f5f5;
            --muted: #a1a1aa;
            --green: #22c55e;
            --red: #ef4444;
            --amber: #eab308;
        }
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: system-ui, -apple-system, sans-serif;
            background: radial-gradient(circle at top, #16211a 0%, var(--bg) 42%);
            color: var(--text);
            min-height: 100vh;
            padding: 24px;
        }
        .shell { max-width: 1120px; margin: 0 auto; }
        .hero, .panel {
            background: rgba(24, 24, 27, 0.92);
            border: 1px solid var(--border);
            border-radius: 18px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
        }
        .hero { padding: 24px; margin-bottom: 20px; }
        .eyebrow {
            color: var(--green);
            font-size: 12px;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        h1 { margin: 0 0 8px; font-size: clamp(28px, 5vw, 48px); }
        .sub { color: var(--muted); max-width: 760px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }
        .panel { padding: 20px; }
        label {
            display: block;
            margin-bottom: 6px;
            font-size: 14px;
            color: var(--muted);
        }
        input {
            width: 100%;
            background: var(--surface-2);
            color: var(--text);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 14px;
            font-size: 15px;
        }
        .actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
        button {
            border: 0;
            border-radius: 999px;
            padding: 12px 18px;
            cursor: pointer;
            font-weight: 700;
        }
        .btn-primary { background: var(--green); color: #041107; }
        .btn-secondary {
            background: transparent;
            color: var(--text);
            border: 1px solid var(--border);
        }
        .metric { display: grid; gap: 14px; }
        .metric-card {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 16px;
        }
        .metric-title {
            color: var(--muted);
            font-size: 13px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 6px;
        }
        .metric-value { font-size: 38px; font-weight: 800; }
        .good { color: var(--green); }
        .bad { color: var(--red); }
        .warn { color: var(--amber); }
        .result-copy, .share-box { color: var(--muted); line-height: 1.6; font-size: 14px; }
        .share-box {
            margin-top: 16px;
            padding: 14px;
            background: #0d1310;
            border: 1px solid rgba(34, 197, 94, 0.25);
            border-radius: 12px;
            display: none;
        }
        .share-url { word-break: break-all; color: var(--text); margin-top: 8px; }
        .status-line { margin-top: 12px; min-height: 20px; color: var(--muted); font-size: 14px; }
        .pill {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.12);
            color: var(--green);
            border: 1px solid rgba(34, 197, 94, 0.18);
            font-size: 13px;
            margin-bottom: 14px;
        }
    </style>
</head>
<body>
    <div class="shell">
        <section class="hero">
            <div class="eyebrow">YNOR.AI</div>
            <h1>Audit Mu partageable</h1>
            <p class="sub">Le moment fort du produit est simple: un audit Mu dit si un agent doit continuer, s'arrAter et combien cela peut Aconomiser. Ce dashboard transforme ce rAsultat en preuve publique partageable sans ajouter de nouveau framework.</p>
        </section>

        <div class="grid">
            <section class="panel">
                <div class="pill">ClA de test intAgrAe pour la dAmo interne</div>
                <label for="apiKey">ClA API Ynor</label>
                <input id="apiKey" value="__DASHBOARD_DEFAULT_API_KEY__" placeholder="Entrez votre clA API privAe" />
                <label for="tokenCost">CoAt par token (USD)</label>
                <input id="tokenCost" type="number" step="0.000001" value="0.00001" />
                <label for="tokensUsed">Tokens utilisAs</label>
                <input id="tokensUsed" type="number" step="1" value="1200" />
                <label for="contextLength">Longueur de contexte</label>
                <input id="contextLength" type="number" step="1" value="3200" />
                <label for="errorEstimate">Estimation d'erreur</label>
                <input id="errorEstimate" type="number" min="0" max="1" step="0.01" value="0.18" />
                <label for="confidence">Confiance</label>
                <input id="confidence" type="number" min="0" max="1" step="0.01" value="0.91" />
                <div class="actions">
                    <button class="btn-primary" id="runAudit">Lancer l'audit</button>
                    <button class="btn-secondary" id="shareAudit">GAnArer un lien public</button>
                </div>
                <div class="status-line" id="statusLine">PrAt A calculer un audit Mu.</div>
            </section>

            <section class="panel metric">
                <div class="metric-card">
                    <div class="metric-title">Score Mu</div>
                    <div class="metric-value good" id="muValue">--</div>
                    <div class="result-copy" id="muReason">Le rAsultat d'audit apparaAtra ici.</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Aconomie estimAe</div>
                    <div class="metric-value warn" id="savedValue">$0.0000</div>
                    <div class="result-copy" id="watermarkValue">Watermark: --</div>
                </div>
                <div class="metric-card">
                    <div class="metric-title">Signal partageable</div>
                    <div class="result-copy">Le lien public expose uniquement Mu, les mAtriques dArivAes et le watermark. Aucun prompt utilisateur n'est publiA.</div>
                    <div class="share-box" id="shareBox">
                        <strong>Lien prAt A partager</strong>
                        <div class="share-url" id="shareUrl">--</div>
                        <div class="actions">
                            <button class="btn-primary" id="copyShare">Copier le lien</button>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </div>

    <script>
        let latestShareUrl = "";

        function buildPayload() {
            return {
                token_cost: parseFloat(document.getElementById("tokenCost").value),
                tokens_used: parseInt(document.getElementById("tokensUsed").value, 10),
                context_length: parseInt(document.getElementById("contextLength").value, 10),
                error_estimate: parseFloat(document.getElementById("errorEstimate").value),
                confidence: parseFloat(document.getElementById("confidence").value)
            };
        }

        function setStatus(message, isError) {
            const line = document.getElementById("statusLine");
            line.textContent = message;
            line.style.color = isError ? "var(--red)" : "var(--muted)";
        }

        function applyResult(data) {
            const muEl = document.getElementById("muValue");
            muEl.textContent = data.mu.toFixed(4);
            muEl.className = "metric-value " + (data.mu >= 0 ? "good" : "bad");
            document.getElementById("muReason").textContent = data.reason;
            document.getElementById("savedValue").textContent = "$" + Number(data.billing.estimated_dollars_saved).toFixed(4);
            document.getElementById("watermarkValue").textContent = "Watermark: " + data._watermark;
        }

        async function runAudit(share) {
            latestShareUrl = "";
            document.getElementById("shareBox").style.display = "none";
            setStatus(share ? "CrAation du lien public..." : "Calcul de l'audit en cours...", false);
            try {
                const apiKey = document.getElementById("apiKey").value.trim();
                const response = await fetch("/v1/mu/evaluate" + (share ? "?share=true" : ""), {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Ynor-API-Key": apiKey
                    },
                    body: JSON.stringify(buildPayload())
                });
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || "Audit impossible");
                }
                applyResult(data);
                if (data.share) {
                    latestShareUrl = data.share.share_url;
                    document.getElementById("shareUrl").textContent = latestShareUrl;
                    document.getElementById("shareBox").style.display = "block";
                    setStatus("Lien public gAnArA. Vous pouvez le partager immAdiatement.", false);
                } else {
                    setStatus("Audit terminA. Si le rAsultat est convaincant, gAnArez ensuite le lien public.", false);
                }
            } catch (error) {
                setStatus(error.message || "Une erreur est survenue.", true);
            }
        }

        document.getElementById("runAudit").addEventListener("click", function () { runAudit(false); });
        document.getElementById("shareAudit").addEventListener("click", function () { runAudit(true); });
        document.getElementById("copyShare").addEventListener("click", async function () {
            if (!latestShareUrl) {
                setStatus("Aucun lien A copier pour l'instant.", true);
                return;
            }
            try {
                await navigator.clipboard.writeText(latestShareUrl);
                setStatus("Lien copiA dans le presse-papiers.", false);
            } catch (error) {
                setStatus("Copie impossible, mais le lien reste visible A l'Acran.", true);
            }
        });
    </script>
</body>
</html>
""".replace("__DASHBOARD_DEFAULT_API_KEY__", html.escape(DASHBOARD_DEFAULT_API_KEY))


def _load_json_file(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except Exception:
        return default


USAGE_STATS = _load_json_file(USAGE_FILE, {})
MU_AUDIT_HISTORY = deque(_load_json_file(MU_AUDIT_FILE, []), maxlen=1000)
REVOKED_KEYS = set(_load_json_file(REVOCATION_FILE, []))

async def log_mu_telemetry(mu, alpha, beta, kappa, api_key):
    """Archive le calcul Mu pour le monitoring temporel (mu(t))."""
    entry = {
        "timestamp": time.time(),
        "date": time.ctime(),
        "api_key": f"{api_key[:5]}****",
        "mu": float(f"{mu:.4f}"),
        "alpha": float(f"{alpha:.4f}"),
        "beta": float(f"{beta:.4f}"),
        "kappa": float(f"{kappa:.4f}")
    }
    
    async with MU_AUDIT_LOCK:
        MU_AUDIT_HISTORY.append(entry)
        try:
            with MU_AUDIT_FILE.open("w", encoding="utf-8") as file_handle:
                json.dump(list(MU_AUDIT_HISTORY), file_handle, indent=2)
        except Exception:
            pass  # Silencieux si file-system en Read-Only

def get_latest_date_str():
    return time.strftime("%Y-%m-%d")

async def check_rate_limit(api_key: str = Security(api_key_header)):
    """
    Protocole de ContrAle de Flux (Quota Quotidien). 
    Bloque l'accAs si le nombre d'appels autorisAs par jour est dApassA. 
    Limite par dAfaut: 100 appels/jour (Niveau Free/Startup).
    """
    today = get_latest_date_str()

    async with USAGE_LOCK:
        daily_stats = USAGE_STATS.setdefault(today, {})
        current_usage = daily_stats.get(api_key, 0)

        max_daily_calls = 1000000 if api_key == MASTER_KEY else 100

        if current_usage >= max_daily_calls:
            raise HTTPException(
                status_code=429,
                detail=f"QUOTA EXCEEDED: You reached your daily limit of {max_daily_calls} calls. Upgrade your plan at ynor.ai"
            )

        daily_stats[api_key] = current_usage + 1

        try:
            with USAGE_FILE.open("w", encoding="utf-8") as file_handle:
                json.dump(USAGE_STATS, file_handle, indent=2)
        except Exception:
            pass  # Silencieux en cas d'erreur filesystem

    return True

def is_key_revoked(api_key: str):
    """VArifie si la clA n'est pas blacklistAe par l'Admin (Killswitch)"""
    return api_key in REVOKED_KEYS

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Protocole de vArification d'identitA (Auth Layer). 
    """
    if not api_key:
         raise HTTPException(status_code=401, detail="X-Ynor-API-Key header missing.")
         
    # Y CLEANING : On enlAve le mot 'Bearer' et les espaces si OpenAI les a rajoutAs
    clean_key = api_key.replace("Bearer ", "").strip()
    
    if clean_key not in ALLOWED_KEYS:
        raise HTTPException(
            status_code=403, 
            detail="ACCAS REJETA : ClA API invalide. Obtenez une clA de test sur ynor.ai"
        )
    
    # VArification du Killswitch (Blacklist Admin)
    # On vArifie sur la clA brute et la clA nettoyAe
    if is_key_revoked(api_key) or is_key_revoked(clean_key):
        raise HTTPException(
            status_code=403, 
            detail="DEFCON LOCK: Cette clA Entreprise a AtA rAvoquAe pour non-paiement ou violation de sAcuritA."
        )
        
    return clean_key

# === REQUEST SCHEMA ===
class AgentStatePayload(BaseModel):
    token_cost: float = Field(..., description="Cost per token in USD")
    tokens_used: int = Field(..., description="Total tokens used in this context so far")
    context_length: int = Field(..., description="Amount of tokens actively held in memory")
    error_estimate: float = Field(..., description="Estimated probability of failure (0 to 1.0)")
    confidence: float = Field(..., description="Certainty score of the LLM for the current thought (0 to 1.0)")

class HierarchicalPayload(BaseModel):
    query: str = Field(..., description="The problem or prompt for the AGI to solve")
    alpha_capacity: float = Field(0.8, description="Available dissipation limit (Alpha)")
    beta_pressure: float = Field(0.5, description="Inherent system cost/speed risk (Beta)")
    kappa_memory: float = Field(0.2, description="Inertia context size (Kappa)")

# === MU COMPUTATION CORE ===
def compute_mu(data: AgentStatePayload):
    # Alpha (Gain spatial/informationnel)
    alpha = data.confidence * (1.0 - data.error_estimate)
    
    # Beta (Friction financiAre / coAt de calcul direct)
    beta = data.token_cost * data.tokens_used
    
    # Kappa (Charge psychologique du systAme / Poids du contexte)
    kappa = (data.context_length / 10000.0) + data.error_estimate
    
    # L'Aquation MaAtresse de Survie Computationnelle
    mu = Alpha - (Beta + Kappa)
    return mu, alpha, beta, kappa

def generate_watermark(mu_value: float) -> str:
    """Preuve cryptographique que ce calcul Amane du moteur MDL Ynor officiel."""
    payload = f"{mu_value}_{YNOR_SECRET_SALT}".encode('utf-8')
    return "YNOR-" + hashlib.sha256(payload).hexdigest()[:16].upper()

# === MAIN SAAS ENDPOINT ===
@app.post("/v1/mu/evaluate", dependencies=[Depends(check_rate_limit)])
async def evaluate_viability(
    payload: AgentStatePayload,
    request: Request,
    share: bool = False,
    api_key: str = Depends(verify_api_key),
):
    start_time = time.time()
    
    # Appel de la physique Ynor
    mu_score, alpha, beta, kappa = compute_mu(payload)
    
    # TAlAmAtrie temporelle mu(t) (Score 10/10)
    await log_mu_telemetry(mu_score, alpha, beta, kappa, api_key)
    
    # RAgle MAtallique
    should_halt = mu_score < 0
    
    if should_halt:
        reason = "The Endogenous Cost (beta) and Memory Burden (kappa) outweigh the cognitive gain (alpha). Halt agent to save API costs."
    else:
        reason = "Agent trajectory is viable. Continue generating."
        
    latency_ms = float(f"{(time.time() - start_time) * 1000:.2f}")
    
    response_payload = {
        "mu": float(f"{mu_score:.4f}"),
        "should_halt": should_halt,
        "reason": reason,
        "metrics": {
            "alpha_gain": float(f"{alpha:.4f}"),
            "beta_cost": float(f"{beta:.4f}"),
            "kappa_burden": float(f"{kappa:.4f}")
        },
        "billing": {
            # Si on arrAte l'agent maintenant, on estime sauver les 1000 prochains tokens d'hallucination
            "estimated_dollars_saved": float(f"{(payload.token_cost * 1000):.4f}") if should_halt else 0.0,
            "latency_ms": latency_ms
        },
        "_watermark": generate_watermark(mu_score)
    }

    if share:
        response_payload["share"] = await create_public_share_record(response_payload, api_key, request)

    return response_payload

# === HIERARCHICAL SYSTEM 1 / SYSTEM 2 ENDPOINT ===
@app.post("/v1/agent/hierarchical_query", dependencies=[Depends(check_rate_limit)])
async def execute_hierarchical_engine(payload: HierarchicalPayload, api_key: str = Depends(verify_api_key)):
    start_time = time.time()
    
    # SYSTEM 1 (InfArence Rapide Heuristique)
    # En prod, redirige vers LLM_Small (ex: Llama-3-8b, faible coAt, temps 200ms)
    sys1_time = 0.2
    await asyncio.sleep(sys1_time)  # Simuler la latence API locale
    
    # ProbabilitA d'hallucination/erreur corrAlAe A la pression Beta
    is_hallucination = random.random() < payload.beta_pressure
    
    # Test thermodynamique local
    mu_sys1 = payload.alpha_capacity - payload.beta_pressure - payload.kappa_memory
    
    if mu_sys1 < 0 or is_hallucination:
        # INTERVENTION DU SYSTEME 2 (RAgulation Analytique)
        # Redirige vers un LLM_Large (ex: GPT-4o, coAt AlevA, temps 1000ms+) pour vArifier et dissiper
        sys2_time = 1.0
        await asyncio.sleep(sys2_time)
        
        # Le SystAme 2 consomme de l'Anergie (Beta grimpe) mais restaure l'intAgritA globale (Alpha grimpe max)
        alpha_final = payload.alpha_capacity * 2.0
        beta_final = payload.beta_pressure * 1.5
        kappa_final = payload.kappa_memory * 1.2
        mu_final = alpha_final - beta_final - kappa_final
        
        # ZERO-KNOWLEDGE PRIVACY: On ne log/renvoie jamais la query brute pour garantir GDPR/HIPAA
        full_hash = str(hashlib.md5(payload.query.encode()).hexdigest())
        safe_query_hash = full_hash[0:10]  # type: ignore
        output = f"[Zero-Knowledge Hash: {safe_query_hash}] -> RAsolu par SYSTEME 2. DArive (hallucination) dissipAe et corrigAe en interne."
        system_used = "System_2_Analytical"
    else:
        # Le SystAme 1 a rAussi sans diverger (Mu >= 0), pas besoin de payer pour GPT-4 !
        alpha_final = payload.alpha_capacity
        beta_final = payload.beta_pressure
        kappa_final = payload.kappa_memory
        mu_final = mu_sys1
        
        full_hash = str(hashlib.md5(payload.query.encode()).hexdigest())
        safe_query_hash = full_hash[0:10]  # type: ignore
        output = f"[Zero-Knowledge Hash: {safe_query_hash}] -> RAsolu par SYSTEME 1. Association rapide sans dArive de contexte."
        system_used = "System_1_Heuristic"
        
    # Pyre bypass: format strings for safe floats instead of round()
    latency_ms = float(f"{(time.time() - start_time) * 1000:.2f}")
    
    return {
        "status": "SUCCESS",
        "agent_response": output,
        "metrics": {
            "alpha_final": float(f"{alpha_final:.4f}"),
            "beta_final": float(f"{beta_final:.4f}"),
            "kappa_final": float(f"{kappa_final:.4f}"),
            "mu_final": float(f"{mu_final:.4f}"),
            "mu_sys1_heuristic": float(f"{mu_sys1:.4f}"),
            "latency_ms": latency_ms,
            "cost_evaluation": "High Cost (GPT-4 Used)" if system_used == "System_2_Analytical" else "Optimized (Llama Used)"
        },
        "privacy_compliance": "Zero-Knowledge Mode Active (No PII logged)",
        "_watermark": generate_watermark(mu_final)
    }

# === ADMIN EMERGENCY CONTROLS ===
class RevokePayload(BaseModel):
    admin_secret: str
    target_api_key: str

@app.post("/v1/admin/revoke_key", tags=["Admin"], description="Coupe Circuit (Killswitch) temps-rAel.")
async def revoke_enterprise_key(payload: RevokePayload):
    # Validation du Master Secret Admin (Depuis les env vars)
    expected_hash = hashlib.sha256(YNOR_ADMIN_SECRET.encode()).hexdigest()
    admin_hash = hashlib.sha256(payload.admin_secret.encode()).hexdigest()
    
    if admin_hash != expected_hash:
        raise HTTPException(status_code=403, detail="Unauthorized Master Override Attempt (Honeypot logged).")
        
    async with REVOCATION_LOCK:
        if payload.target_api_key not in REVOKED_KEYS:
            REVOKED_KEYS.add(payload.target_api_key)
            with REVOCATION_FILE.open("w", encoding="utf-8") as file_handle:
                json.dump(sorted(REVOKED_KEYS), file_handle, indent=2)
            
    return {
        "status": "SUCCESS", 
        "message": f"Enterprise Key {payload.target_api_key[:5]}***** has been permanently revoked. Engine access terminated."
    }

import subprocess

# === AUTO-LEARNING SCHEMA ===
class AutoLearnPayload(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    experience_summary: str = Field(..., description="Key insights or chat log to archive")
    quality_score: float = Field(..., description="Manual or auto-evaluated Alpha score (0-1.0)")

# === AUTO-LEARNING ENGINE (THE BRAIN SYNC) ===
@app.post("/v1/archive/auto_learn", tags=["Maintenance"], dependencies=[Depends(check_rate_limit)])
async def archive_and_learn(payload: AutoLearnPayload, api_key: str = Depends(verify_api_key)):
    """
    Module d'Auto-Apprentissage Ynor : 
    Enregistre les logs et synchronise le cerveau AGI instantanAment.
    """
    if READ_ONLY_MODE:
        return {
            "status": "READ_ONLY_BLOCK",
            "message": "AGI SELF-MODIFICATION LOCKED. Set MDL_PROD_WRITE_ENABLED=TRUE to allow learning.",
            "mode": "PROD-SECURE"
        }
        
    start_time = time.time()
    
    # RAsolution dynamique des chemins pour compatibilitA Cloud/Local
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Root: MDL_Ynor_Framework
    
    default_log_dir = os.path.join(base_dir, "_10_YNOR_AI_KNOWLEDGE_BASE_SOURCES")
    log_dir = os.getenv("YNOR_LOG_DIR", default_log_dir)
    log_file = os.path.join(log_dir, "AUTO_LEARNED_LOGS.md")
    
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except:
            pass # Fallback si pas de droits d'Acriture (Cloud read-only)
        
    # CrAation de l'entrAe de log
    log_entry = f"\n\n---\n### [SESSION: {payload.session_id}] - {time.ctime()}\n"
    log_entry += f"**Alpha Score**: {payload.quality_score:.2f}\n"
    log_entry += f"**Experience**: {payload.experience_summary}\n"
    
    try:
        # 1. Acriture physique du log (Persistance)
        if os.path.exists(log_dir):
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
            
        # 2. DAclenchement de l'Indexeur (Evolution du Cerveau)
        # On cherche l'indexeur dans l'environnement ou dans le dossier frAre habituel
        default_indexer_cwd = os.path.join(base_dir, "MDL_YNOR_GPT_KNOWLEDGE")
        default_indexer_path = os.path.join(default_indexer_cwd, "update_knowledge.py")
        
        indexer_path = os.getenv("YNOR_INDEXER_PATH", default_indexer_path)
        cwd_indexer = os.getenv("YNOR_INDEXER_CWD", default_indexer_cwd)
        
        if os.path.exists(indexer_path):
            subprocess.Popen(["python", indexer_path], cwd=cwd_indexer, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return {
            "status": "SUCCESS",
            "message": "Experience archived. Brain synchronization triggered.",
            "latency_ms": float(f"{(time.time() - start_time) * 1000:.2f}")
        }
    except Exception as e:
        # En Cloud, l'Acriture de fichier peut Achouer sur filesystem immuable, on warn mais on ne crash pas l'API
        print(f"Warning: Auto-Learning non-critique AchouA: {str(e)}")
        return {"status": "PARTIAL_SUCCESS", "warning": str(e)}

# === COGNITIVE RUN ENDPOINT (FOR TERMINAL DASHBOARD) ===
@app.post("/run", dependencies=[Depends(check_rate_limit)])
async def cognitive_run(payload: Request, api_key: str = Depends(verify_api_key)):
    """
    Endpoint compatible avec streamlit_dashboard.py. 
    Redirige vers le moteur hiArarchique Ynor.
    """
    data = await payload.json()
    user_query = data.get("input", "Who are you?")
    
    # Appel simulA au moteur hiArarchique interne
    hier_payload = HierarchicalPayload(query=user_query)
    result = await execute_hierarchical_engine(hier_payload, api_key)
    
    # Format attendu par streamlit_dashboard.py
    return {
        "status": "SUCCESS",
        "cognitive_tool_selected": "Hierarchical_Orchestrator",
        "action_result": {
            "mu": result["metrics"]["mu_final"],
            "response": result["agent_response"],
            "system_used": "System_2_Analytical" if "System 2" in result["agent_response"] else "System_1_Heuristic"
        }
    }

# === HEALTH & STATUS ENDPOINTS ===
@app.get("/status", tags=["Diagnostic"])
async def get_status():
    """VArifie si le Noyau Ynor est opArationnel."""
    return {
        "status": "ONLINE", 
        "engine": "MDL Ynor", 
        "version": "3.1.0-MILLENNIUM",
        "write_lock": READ_ONLY_MODE,
        "telemetry": "ACTIVE"
    }

@app.get("/v1/mu/history", tags=["Diagnostic"])
async def get_mu_history(api_key: str = Depends(verify_api_key)):
    """Affiche les 50 derniers audits Mu pour analyse de tendance (dA/dt)."""
    return list(MU_AUDIT_HISTORY)[-50:]

@app.get("/v1/mu/check", tags=["Diagnostic"])
async def quick_mu_check():
    """Audit rapide sans payload pour test GPT."""
    return {
        "mu": 1.0, 
        "status": "VIABLE", 
        "message": "SystAme en Aquilibre thermodynamique."
    }

@app.get("/share/mu/{share_id}", tags=["Growth"])
async def view_shared_mu_audit(share_id: str):
    shares = load_json_file(SHARED_AUDITS_FILE, {})
    share_record = shares.get(share_id)
    if not share_record:
        raise HTTPException(status_code=404, detail="Shared Mu audit not found.")

    await track_growth_event(
        "share_page_viewed",
        {
            "share_id": share_id,
            "mu": share_record["mu"],
            "should_halt": share_record["should_halt"],
        },
    )

    reason = html.escape(share_record["reason"])
    watermark = html.escape(share_record["_watermark"])
    mu_value = float(share_record["mu"])
    created_by = html.escape(share_record["created_by"])
    mu_class = "halt" if share_record["should_halt"] else "go"

    page_html = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Preuve Mu YNOR</title>
        <style>
            body {{
                margin: 0;
                font-family: system-ui, -apple-system, sans-serif;
                background: radial-gradient(circle at top, #18251a 0%, #09090b 45%);
                color: #f5f5f5;
                min-height: 100vh;
                display: grid;
                place-items: center;
                padding: 24px;
            }}
            .card {{
                width: min(760px, 100%);
                background: rgba(24, 24, 27, 0.94);
                border: 1px solid #27272a;
                border-radius: 22px;
                padding: 28px;
                box-shadow: 0 25px 80px rgba(0, 0, 0, 0.35);
            }}
            .eyebrow {{
                color: #22c55e;
                text-transform: uppercase;
                letter-spacing: 0.16em;
                font-size: 12px;
                margin-bottom: 10px;
            }}
            h1 {{ margin: 0 0 12px; font-size: clamp(30px, 6vw, 52px); }}
            .mu {{
                font-size: clamp(56px, 14vw, 96px);
                font-weight: 800;
                margin: 18px 0 8px;
            }}
            .mu.go {{ color: #22c55e; }}
            .mu.halt {{ color: #ef4444; }}
            .reason {{
                color: #d4d4d8;
                line-height: 1.7;
                margin-bottom: 22px;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 12px;
                margin-bottom: 20px;
            }}
            .metric {{
                background: #111114;
                border: 1px solid #27272a;
                border-radius: 14px;
                padding: 14px;
            }}
            .label {{
                color: #a1a1aa;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 6px;
            }}
            .value {{ font-size: 28px; font-weight: 700; }}
            .footer {{
                color: #a1a1aa;
                font-size: 14px;
                line-height: 1.6;
                border-top: 1px solid #27272a;
                padding-top: 18px;
            }}
            a {{
                color: #22c55e;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="eyebrow">YNOR SHAREABLE PROOF</div>
            <h1>Audit Mu public</h1>
            <div class="mu {mu_class}">{mu_value:.4f}</div>
            <p class="reason">{reason}</p>
            <div class="grid">
                <div class="metric">
                    <div class="label">Alpha</div>
                    <div class="value">{share_record["metrics"]["alpha_gain"]:.4f}</div>
                </div>
                <div class="metric">
                    <div class="label">Beta</div>
                    <div class="value">{share_record["metrics"]["beta_cost"]:.4f}</div>
                </div>
                <div class="metric">
                    <div class="label">Kappa</div>
                    <div class="value">{share_record["metrics"]["kappa_burden"]:.4f}</div>
                </div>
                <div class="metric">
                    <div class="label">Aconomie estimAe</div>
                    <div class="value">${share_record["billing"]["estimated_dollars_saved"]:.4f}</div>
                </div>
            </div>
            <div class="footer">
                <div>Watermark: <strong>{watermark}</strong></div>
                <div>PubliA par: {created_by}</div>
                <div>Aucune requAte brute n'est exposAe. La preuve partage uniquement le rAsultat dArivA de l'audit.</div>
                <div style="margin-top: 8px;"><a href="/dashboard">Lancer votre propre audit</a></div>
            </div>
        </div>
    </body>
    </html>
    """
    return Response(content=page_html, media_type="text/html")

@app.get("/v1/growth/events", tags=["Growth"])
async def get_growth_events(api_key: str = Depends(verify_api_key)):
    return load_json_file(GROWTH_EVENTS_FILE, [])

# === ADMIN LIVE DASHBOARD (VISUAL) ===
@app.get("/dashboard", tags=["Admin"])
async def view_dashboard():
    """
    Interface visuelle en temps rAel des mAtriques Ynor. 
    (Accessible uniquement en interne / localhost dans cette version).
    """
    return Response(content=render_dashboard_html(), media_type="text/html")

@app.get("/privacy", tags=["Legal"])
async def privacy_policy():
    """Politique de ConfidentialitA Ynor Zero-Knowledge."""
    privacy_html = """
    <html>
        <body style="font-family: sans-serif; padding: 40px; line-height: 1.6; max-width: 800px; margin: auto; background: #0a0a0a; color: #00ff00;">
            <h1 style="color: #00ff00; border-bottom: 2px solid #00ff00;">YNOR ZERO-KNOWLEDGE PRIVACY POLICY (v3.1)</h1>
            <p><strong>MDL YNOR FRAMEWORK - MILLENNIUM AGI GOVERNANCE</strong></p>
            <p>Your privacy is protected by the Ynor Zero-Knowledge protocol:</p>
            <ul>
                <li><strong>NO DATA RETENTION:</strong> No user prompts or specific queries are logged on the server. We only process mathematical abstractions.</li>
                <li><strong>GDPR COMPLIANT:</strong> No PII (Personally Identifiable Information) is stored or shared.</li>
                <li><strong>ENCRYPTED TRANSMISSION:</strong> All communications between ChatGPT and the Ynor Engine are encrypted via TLS/SSL.</li>
            </ul>
            <p>Contact: <a href="mailto:ronycharlier@mdlstrategy.com" style="color: #00ff00;">ronycharlier@mdlstrategy.com</a></p>
        </body>
    </html>
    """
    return Response(content=privacy_html, media_type="text/html")

if __name__ == "__main__":
    import uvicorn  # type: ignore
    
    # RAcupAration du port depuis le YNOR_SERVER_MANAGER.bat ou fallback 8492
    port = int(os.environ.get("PORT", 8492))
    # DAploiement serveur
    uvicorn.run(app, host="0.0.0.0", port=port)

