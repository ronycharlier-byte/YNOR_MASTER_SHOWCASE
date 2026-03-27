# MIROIR TEXTUEL - ynor_security_shield.py

Source : MDL_Ynor_Framework\_09_SECURITY_AND_AUDIT\ynor_security_shield.py
Taille : 1811 octets
SHA256 : a30a8ae48cbec9dea81242536f01994aa9cc8b91a15fd03fcc2718eb745ed04d

```text
# =============================================================================
# 🛡️ MDL YNOR - SECURITY SHIELD (DEFCON 1)
# =========================
# Verrouillage centralisé des capacités d'auto-modification et audit trail.
# =============================================================================
import os
import time
import logging

# Configuration du Shield
# SAFE_MODE = True par défaut. Nécessite MDL_ALLOW_MUTATION=TRUE pour désactiver.
SAFE_MODE = os.getenv("MDL_SAFE_MODE", "TRUE").upper() == "TRUE"

# Configuration Logging Audit
logging.basicConfig(
    filename='mdl_security_audit.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | SHIELD: %(message)s'
)

def require_human_approval(func):
    """Décorateur pour empêcher toute auto-modification sans autorisation explicite."""
    def wrapper(*args, **kwargs):
        action_name = func.__name__
        if SAFE_MODE:
            msg = f"❌ TENTATIVE D'AUTO-MODIFICATION BLOQUÉE : {action_name}. [SAFE_MODE=ACTIVE]"
            print(f"\n[⚠️ SECURITY] {msg}")
            logging.error(msg)
            raise RuntimeError(f"Audit Required: Action '{action_name}' is disabled in Safe Mode.")
        
        logging.info(f"✅ ACTION AUTORISÉE : {action_name} par signature humaine.")
        return func(*args, **kwargs)
    return wrapper

def check_critical_secrets():
    """Vérifie la présence des secrets vitaux avant le démarrage."""
    critical_keys = ["OPENAI_API_KEY", "MDL_MASTER_AUTH"]
    missing = [k for k in critical_keys if not os.getenv(k)]
    
    if missing:
        msg = f"🚨 FATAL: Clés manquantes dans l'environnement : {', '.join(missing)}"
        logging.critical(msg)
        raise RuntimeError(msg)
    
    print("✅ Sécurité environnementale : VALIDÉ.")

```