import os
import subprocess
from datetime import datetime

# ==============================================================================
# MDL YNOR CANONICAL API - V7.4.9 (AUTO-AUTH ON FREE TIER)
# STATUT : PERSISTANCE SANS SHELL ACTIVÉE
# ==============================================================================

def git_sync():
    try:
        # 1. Récupération du jeton depuis l'environnement
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN non trouvé dans l'environnement.")
            return False
        
        # 2. Construction de l'URL sécurisée (Rony-Charlier repo)
        repo_url = f"https://{token}@github.com/ronycharlier-byte/MDL_YNOR_V7_1_DISTRIBUTION.git"
        
        # 3. Injection dynamique du remote sur Render
        subprocess.run(["git", "remote", "set-url", "origin", repo_url], check=True)
        
        # 4. Configuration d'identité (Obligatoire pour commit)
        subprocess.run(["git", "config", "user.email", "ronycharlier@mdlstrategy.com"], check=True)
        subprocess.run(["git", "config", "user.name", "MDL-Canonical-Engine"], check=True)
        
        # 5. Cycle de persistance Canonique - TOTAL DIAMOND V10.8
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"V10.8 TOTAL DIAMOND : Autonome et IsoléETÉ Formalisme Logique Sémantique - {datetime.now()}"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        return True
    except Exception as e:
        print(f"Sync failed: {e}")
        return False
