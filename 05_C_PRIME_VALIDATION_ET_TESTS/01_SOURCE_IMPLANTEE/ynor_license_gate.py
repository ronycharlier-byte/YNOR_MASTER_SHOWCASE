import os
import json
import hashlib
from datetime import datetime

# ==============================================================================
# MDL YNOR LICENSE GATE - V7.1
# STATUT : VERROUILLAGE SOUVERAIN ACTIF
# ==============================================================================

def validate_license_sovereignty():
    """Vérifie si une licence MDL valide est active dans l'environnement."""
    repo_root = r"C:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"
    vault_path = os.path.join(repo_root, "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")
    
    if not os.path.exists(vault_path):
        return False, "ERREUR : VAULT MDL INDISPONIBLE"

    try:
        with open(vault_path, "r", encoding="utf-8") as f:
            vault = json.load(f)
            license_key = vault.get("mdl_license_v7_key")
            
            # Signature de validation interne (Immuable)
            # Clé attendue : "MDL-SOUVERAIN-2026-V7.1-CANONICAL"
            if license_key == "MDL-SOUVERAIN-2026-V7.1-CANONICAL":
                return True, "LICENCE MDL V7.1 VALIDÉE (SOUVERAINETÉ ACTIVE)"
            else:
                return False, "ACCÈS REFUSÉ : LICENCE NON CERTIFIÉE"
    except Exception as e:
        return False, f"ERREUR SYSTÉMIQUE : {str(e)}"

if __name__ == "__main__":
    is_valid, msg = validate_license_sovereignty()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
