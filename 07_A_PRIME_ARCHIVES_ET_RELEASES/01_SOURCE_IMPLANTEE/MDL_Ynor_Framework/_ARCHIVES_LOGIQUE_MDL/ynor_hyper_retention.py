# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# MOTEUR DE RTENTION PAR RSONANCE QUANTIQUE v1.0
# =============================================================================
import json
import os
import time
from datetime import datetime

RESONANCE_DB = r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\mdl_user_resonance.json"

class RetentionEngine:
    """
    Assure la captivite positive des utilisateurs par le cumul de valeur structurelle.
    """
    def __init__(self):
        self.data = self._load_db()

    def _load_db(self):
        if os.path.exists(RESONANCE_DB):
            with open(RESONANCE_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_db(self):
        with open(RESONANCE_DB, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)

    def track_usage(self, user_id, tier):
        """Met a jour le score de resonance de l'utilisateur."""
        now = time.time()
        if user_id not in self.data:
            self.data[user_id] = {
                "first_audit": datetime.now().ctime(),
                "resonance_score": 10.0,
                "total_audits": 0,
                "last_active": now,
                "tier": tier
            }
        
        user = self.data[user_id]
        # Gain de resonance par usage
        gain = 0.5 if tier == "gratuit" else 2.0
        user["resonance_score"] += gain
        user["total_audits"] += 1
        user["last_active"] = now
        
        self._save_db()
        return user["resonance_score"]

    def check_for_drift(self, user_id):
        """Calcule la 'Peur de la Derive' si l'utilisateur est absent."""
        if user_id not in self.data: return None
        
        user = self.data[user_id]
        inactive_time = time.time() - user["last_active"]
        
        # Simulation d'une derive de marge mu basee sur l'absence (Loi d'Inertie)
        drift_risk = (inactive_time / 3600) * 0.05 # 5% de risque par heure
        
        if drift_risk > 0.1: # Alerte a partir de 10%
            return {
                "alert": "RISQUE DE DRIVE STRUCTURELLE",
                "severity": "CRITIQUE" if drift_risk > 0.5 else "MODRE",
                "message": f"Votre systeme n'a pas ete audite depuis {int(inactive_time/60)} min. Marge mu theorique en baisse de {drift_risk:.2%}.",
                "solution": "Relancez un Audit Quantum pour restabiliser votre attracteur."
            }
        return None

    def get_loyalty_perks(self, user_id):
        """Recompense la fidelite pour empecher le passage a la concurrence."""
        if user_id not in self.data: return "Basique"
        score = self.data[user_id]["resonance_score"]
        
        if score > 1000: return "ARCHITECTE_ADJOINT"
        if score > 500:  return "MATRE_DISSIPATEUR"
        if score > 100:  return "AUDITEUR_CONFIRM"
        return "NOVICE_YNOR"

if __name__ == "__main__":
    engine = RetentionEngine()
    # Test simulation
    score = engine.track_usage("demo_user_123", "pro")
    print(f"OK Resonance mise a jour : {score}")
    drift = engine.check_for_drift("demo_user_123")
    print(f" Etat de derive : {drift}")



