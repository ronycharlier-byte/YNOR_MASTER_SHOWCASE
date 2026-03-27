# MIROIR TEXTUEL - mdl_api_keys.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\mdl_api_keys.py
Taille : 6431 octets
SHA256 : 9e9c16c51fd243ab8561e81a0d2a28d697f293939c1e9a0195731979757c954b

```text
# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
# Gestion des clés API et abonnements MDL Ynor
# =============================================================================

import json
import os
import uuid
import hashlib
from datetime import datetime, timedelta

KEYS_FILE = os.path.join(os.path.dirname(__file__), "api_keys.json")

# --- NIVEAUX D'ABONNEMENT ---
TIERS = {
    "gratuit": {
        "name": "Gratuit",
        "price": "0€",
        "daily_limit": 10,
        "endpoints": ["/audit_mu"],
        "description": "Audit Mu classique uniquement — 10 requêtes/jour"
    },
    "pro": {
        "name": "Pro",
        "price": "9.99€/mois",
        "daily_limit": 500,
        "endpoints": ["/audit_mu", "/quantum_audit_mu", "/trigger_decoherence_shock"],
        "description": "Accès complet aux outils quantiques — 500 requêtes/jour"
    },
    "entreprise": {
        "name": "Entreprise",
        "price": "49.99€/mois",
        "daily_limit": 10000,
        "endpoints": ["/audit_mu", "/quantum_audit_mu", "/trigger_decoherence_shock", "/full_system_audit"],
        "description": "Accès illimité + Noyau Axiomatique + Support prioritaire"
    }
}


def _load_keys() -> dict:
    """Charge les clés API depuis le fichier JSON."""
    if os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keys": {}}


def _save_keys(data: dict):
    """Sauvegarde les clés API dans le fichier JSON."""
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_api_key(email: str, tier: str = "free") -> dict:
    """
    Génère une nouvelle clé API pour un utilisateur.
    Retourne les infos de la clé créée.
    """
    if tier not in TIERS:
        raise ValueError(f"Tier invalide. Choisir parmi: {list(TIERS.keys())}")

    # Générer une clé unique : mdl_ynor_XXXX
    raw_key = f"mdl_ynor_{uuid.uuid4().hex[:24]}"

    # Hash de la clé pour le stockage sécurisé
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

    data = _load_keys()
    data["keys"][key_hash] = {
        "email": email,
        "tier": tier,
        "created_at": datetime.now().isoformat(),
        "expires_at": (datetime.now() + timedelta(days=30)).isoformat() if tier != "free" else None,
        "daily_usage": {},
        "total_requests": 0,
        "active": True
    }
    _save_keys(data)

    return {
        "api_key": raw_key,
        "email": email,
        "tier": tier,
        "tier_info": TIERS[tier],
        "message": "IMPORTANT: Sauvegardez cette clé, elle ne sera plus affichée."
    }


def validate_api_key(api_key: str, endpoint: str) -> dict:
    """
    Valide une clé API et vérifie les permissions.
    Retourne le statut de la validation.
    """
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    data = _load_keys()

    # Vérifier que la clé existe
    if key_hash not in data["keys"]:
        return {"valid": False, "error": "CLÉ API INVALIDE", "code": 401}

    key_info = data["keys"][key_hash]

    # Vérifier que la clé est active
    if not key_info["active"]:
        return {"valid": False, "error": "CLÉ API DÉSACTIVÉE", "code": 403}

    # Vérifier l'expiration (pour les plans payants)
    if key_info["expires_at"]:
        if datetime.now() > datetime.fromisoformat(key_info["expires_at"]):
            return {"valid": False, "error": "ABONNEMENT EXPIRÉ — Renouvelez sur notre page de paiement", "code": 402}

    tier = key_info["tier"]
    tier_config = TIERS[tier]

    # Vérifier les permissions d'endpoint
    if endpoint not in tier_config["endpoints"]:
        allowed = ", ".join(tier_config["endpoints"])
        return {
            "valid": False,
            "error": f"ENDPOINT NON AUTORISÉ pour le plan {tier_config['name']}. Endpoints autorisés: {allowed}. Passez au plan Pro pour débloquer.",
            "code": 403
        }

    # Vérifier la limite journalière
    today = datetime.now().strftime("%Y-%m-%d")
    daily_count = key_info["daily_usage"].get(today, 0)

    if daily_count >= tier_config["daily_limit"]:
        return {
            "valid": False,
            "error": f"LIMITE JOURNALIÈRE ATTEINTE ({tier_config['daily_limit']} req/jour pour le plan {tier_config['name']}). Passez au plan supérieur.",
            "code": 429
        }

    # Incrémenter l'usage
    key_info["daily_usage"][today] = daily_count + 1
    key_info["total_requests"] += 1
    _save_keys(data)

    return {
        "valid": True,
        "tier": tier,
        "remaining_today": tier_config["daily_limit"] - daily_count - 1,
        "total_requests": key_info["total_requests"]
    }


def get_usage_stats(api_key: str) -> dict:
    """Retourne les statistiques d'utilisation d'une clé API."""
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    data = _load_keys()

    if key_hash not in data["keys"]:
        return {"error": "CLÉ API INVALIDE"}

    info = data["keys"][key_hash]
    tier = TIERS[info["tier"]]
    today = datetime.now().strftime("%Y-%m-%d")

    return {
        "email": info["email"],
        "tier": info["tier"],
        "tier_name": tier["name"],
        "price": tier["price"],
        "daily_limit": tier["daily_limit"],
        "used_today": info["daily_usage"].get(today, 0),
        "remaining_today": tier["daily_limit"] - info["daily_usage"].get(today, 0),
        "total_requests": info["total_requests"],
        "created_at": info["created_at"],
        "expires_at": info["expires_at"],
        "active": info["active"]
    }


def list_all_keys_admin() -> list:
    """Liste toutes les clés (admin uniquement). Retourne des infos sans les clés."""
    data = _load_keys()
    result = []
    for key_hash, info in data["keys"].items():
        result.append({
            "email": info["email"],
            "tier": info["tier"],
            "total_requests": info["total_requests"],
            "active": info["active"],
            "created_at": info["created_at"]
        })
    return result

```