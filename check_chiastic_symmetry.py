import os
import json

def check_symmetry():
    print("--- AUDIT DE COHÉRENCE CHIASTIQUE YNOR ---")
    
    layers = {
        "C": "03_C_MOTEURS_ET_DEPLOIEMENT",
        "C_PRIME": "05_C_PRIME_VALIDATION_ET_TESTS"
    }
    
    # Check if files in C have corresponding validation in C'
    c_files = [f for f in os.listdir(layers["C"]) if os.path.isfile(os.path.join(layers["C"], f))]
    c_prime_files = [f for f in os.listdir(layers["C_PRIME"]) if os.path.isfile(os.path.join(layers["C_PRIME"], f))]
    
    print(f"Fichiers Moteur (C) : {len(c_files)}")
    print(f"Fichiers Validation (C') : {len(c_prime_files)}")
    
    missing = []
    for f in c_files:
        if f == "README.md" or f == "00_NODE.md": continue
        # Simple heuristic: look for similar names or prefixes
        found = False
        base = f.split('.')[0]
        for pf in c_prime_files:
            if base in pf:
                found = True
                break
        if not found:
            missing.append(f)
            
    if missing:
        print("\n[ALERTE] Rupture de symétrie détectée !")
        print("Les fichiers suivants n'ont pas de pendant de validation directe :")
        for m in missing:
            print(f" - {m}")
    else:
        print("\n[SUCCÈS] Symétrie C <-> C' maintenue (mu = 1.0).")

    return {
        "status": "VALIDATED" if not missing else "ASYMMETRIC",
        "missing_count": len(missing)
    }

if __name__ == "__main__":
    report = check_symmetry()
    with open("chiastic_audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
