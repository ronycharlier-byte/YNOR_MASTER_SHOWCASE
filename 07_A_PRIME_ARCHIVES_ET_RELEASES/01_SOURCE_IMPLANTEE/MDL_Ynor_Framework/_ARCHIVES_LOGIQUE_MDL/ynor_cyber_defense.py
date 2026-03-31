# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# SYSTME DE DFENSE ACTIVE ET CONTRE-ATTAQUE CYBER-YNOR v1.0
# =============================================================================
import time
import json
import os
from fastapi.responses import StreamingResponse

BAN_LIST_PATH = r"c:\Users\ronyc\Desktop\MDL Ynor Architecture\MDL_Ynor_Framework\mdl_cyber_banlist.json"

class CyberDefense:
    """
    Protege et contre-attaque les intrusions via la Dissipation Coercive des ressources de l'adversaire.
    """
    def __init__(self):
        self._load_ban_list()

    def _load_ban_list(self):
        if os.path.exists(BAN_LIST_PATH):
            with open(BAN_LIST_PATH, "r", encoding="utf-8") as f:
                self.ban_list = json.load(f)
        else:
            self.ban_list = {}

    def _save_ban_list(self):
        with open(BAN_LIST_PATH, "w", encoding="utf-8") as f:
            json.dump(self.ban_list, f, indent=4)

    def is_banned(self, ip):
        return ip in self.ban_list

    def ban_ip(self, ip, reason):
        print(f" [ALERTE CYBER] BANNISSEMENT DE L'IP : {ip} | RAISON : {reason}")
        self.ban_list[ip] = {
            "reason": reason,
            "timestamp": time.ctime(),
            "severity": "CRITICAL"
        }
        self._save_ban_list()

    def generate_quantum_data_bomb(self):
        """Contre-attaque par saturation de memoire (Crash du script adverse)."""
        def bomb_generator():
            # Genere des giga-octets de donnees recursives pour saturer le buffer adverse
            yield "{\"MDL_FIREWALL_ACTIVE\": true, \"ATTACK_DETECTED\": \"REDIRECTING_ENERGY\", \"Vortex_Payload\": [" 
            for i in range(1000000):
                yield f"\"{ 'A' * 1024 }\", "  # Payload massif
            yield "]}"
        
        return StreamingResponse(bomb_generator(), media_type="application/json")

    def apply_tarpit(self, ip, count):
        """Ralentit l'adversaire exponentiellement (Loi d'Inertie)."""
        delay = min(pow(2, count), 60) # Jusqu'a 60s de delai
        print(f" [TARPIT] Application d'une latence de {delay}s sur {ip}")
        time.sleep(delay)

if __name__ == "__main__":
    defense = CyberDefense()
    # Test simple
    defense.ban_ip("1.2.3.4", "Scraping non-autorise sur endpoint critique.")



