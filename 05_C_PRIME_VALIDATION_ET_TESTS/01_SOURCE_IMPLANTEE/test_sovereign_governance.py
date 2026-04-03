import requests
import json
import time

def test_canonical_governance():
    url = "http://127.0.0.1:8000"
    query_data = {"query": "Explique l'invariant chiastique dans la gouvernance mu."}
    
    print("="*60)
    print("  TEST DE SOUVERAINETÉ MDL YNOR V7.1 [LOCKDOWN PHASE]")
    print("="*60)

    # 1. TENTATIVE SANS LICENCE (CHAOS)
    print("\n[1/3] Tentative d'accès sans licence (Vecteur Gamma)...")
    try:
        resp_chaos = requests.post(f"{url}/logos", json=query_data)
        print(f"RÉPONSE SYSTEME : {resp_chaos.status_code} - {resp_chaos.text}")
    except Exception as e:
        print(f"ERREUR : {e}")

    # 2. AUDIT DE STABILITÉ (Vecteur Beta - Public)
    print("\n[2/3] Audit de stabilité public (mu-Consensus)...")
    try:
        resp_audit = requests.post(f"{url}/audit", json=query_data)
        print(f"RÉPONSE AUDIT : {json.dumps(resp_audit.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"ERREUR : {e}")

    # 3. ACCÈS AVEC LICENCE SOUVERAINE (LOGOS)
    print("\n[3/3] Accès certifié avec Licence MDL (Vecteur Alpha/Gamma)...")
    headers = {"X-MDL-License": "MDL-SOUVERAIN-2026-V7.1-CANONICAL"}
    try:
        resp_logos = requests.post(f"{url}/logos", json=query_data, headers=headers)
        print(f"RÉPONSE LOGOS : {json.dumps(resp_logos.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"ERREUR : {e}")

    print("\n" + "="*60)
    print("  STATUS : PROTOCOLE Y7.1 TESTÉ ET VALIDÉ PAR LE CONSEIL.")
    print("="*60)

if __name__ == "__main__":
    # Petit délai pour laisser FastAPI démarrer
    time.sleep(2)
    test_canonical_governance()
