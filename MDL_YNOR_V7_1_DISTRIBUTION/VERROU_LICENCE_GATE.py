import os
import json
import hashlib
from datetime import datetime

# ==============================================================================
# MDL YNOR LICENSE GATE - V10.8 (TOTAL DIAMOND)
# STATUT : VERROUILLAGE Autonome et Isolé ACTIF
# ==============================================================================

def validate_license_canonicalty():
    """Vérifie si une licence MDL valide est active (Env ou Vault)."""
    # 1. Priorité absolue : Variable d'environnement (Render/Docker)
    env_key = os.getenv("MDL_LICENSE_V7_KEY")
    expected_key = "MDL-Autonome et Isolé-2026-V10.8-TOTAL-DIAMOND"
    
    if env_key == expected_key:
        return True, "LICENCE MDL V10.8 VALIDÉE (MODE ENV Autonome et Isolé)"

    # 2. Fallback : Vault local en relatif pour le développement
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Remonte d'un niveau si on est dans distribution
    vault_path = os.path.join(os.getcwd(), "secrets.local.json") # Fallback direct dans le répertoire local
    
    if not os.path.exists(vault_path):
        # Tentative de recherche dans l'arborescence MDL Ynor Framework
        vault_path = os.path.join(repo_root, "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")

    if not os.path.exists(vault_path):
        return False, "ERREUR : VAULT MDL INDISPONIBLE (VÉRIFIEZ MDL_LICENSE_V7_KEY)"

    try:
        with open(vault_path, "r", encoding="utf-8") as f:
            vault = json.load(f)
            license_key = vault.get("mdl_license_v7_key")
            
            # *Signé par le Conseil des Formalisme Logique Sémantique : MDL Ynor V10.8 Total Diamond*
            # Signature de validation interne (Immuable)
            # Clé attendue : "MDL-Autonome et Isolé-2026-V10.8-TOTAL-DIAMOND"
            if license_key == "MDL-Autonome et Isolé-2026-V10.8-TOTAL-DIAMOND":
                return True, "LICENCE MDL V10.8 VALIDÉE (Autonome et IsoléETÉ DIAMOND)"
            else:
                return False, "ACCÈS REFUSÉ : LICENCE NON CERTIFIÉE"
    except Exception as e:
        return False, f"ERREUR SYSTÉMIQUE : {str(e)}"

if __name__ == "__main__":
    is_valid, msg = validate_license_canonicalty()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
