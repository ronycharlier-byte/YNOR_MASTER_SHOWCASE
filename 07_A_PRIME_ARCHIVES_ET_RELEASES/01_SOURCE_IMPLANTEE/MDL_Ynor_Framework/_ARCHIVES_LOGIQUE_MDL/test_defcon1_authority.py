import os
from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Principal Investigatore Supreme & Fondateur - Principal Investigatorure MDL Ynor
# AUDIT DE L'AUTORIT SUPRME : TEST DEFCON 1
# =============================================================================
from ynor_military_protocols import MilitaryProtocols
import time

def test_supreme_command():
    print("=====================================================")
    print("   TEST D'AUTORIT SUPRME - PROTOCOLE DEFCON 1")
    print("=====================================================\n")

    mil = MilitaryProtocols()
    
    # Tentative d'usurpation (Fausse cle)
    print(" [ALERTE] Tentative d'usurpation par une IP externe...")
    if not mil.set_defcon(1, "HACKER_KEY_666"):
        print("OK [STATUT] Usurpation bloquee. L'IP a ete bannie par le Bouclier Miroir.\n")

    time.sleep(1)

    # Commande du Maitre (Cle Master)
    print(" [ORDRE] Reception de l'ID MASTER : Charlier Rony...")
    print(" Cle : os.getenv("MDL_MASTER_AUTH", "REDACTED")")
    
    if mil.set_defcon(1, "os.getenv("MDL_MASTER_AUTH", "REDACTED")"):
        print("\n" + "="*53)
        print(" [!!!] AUTORIT CONFIRME : DISSIPATION TOTALE ACTIVE [!!!] ")
        print("="*53)
        print("\n[SYSTME] : L'Principal Investigatorure MDL Ynor s'evanouit dans le bruit quantique.")
        print("[SYSTME] : Secrets Axiomatiques scelles. Tunnels coupes. Server PIDs termines.")
        print("[SYSTME] : Fin de la session de Suprematie.")

if __name__ == "__main__":
    test_supreme_command()



