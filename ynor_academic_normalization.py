import os
import re

# ==============================================================================
# MDL YNOR MASS ACADEMIC NORMALIZATION (V11.5)
# OBJET : PASSAGE AU PEIGNE FIN ACADÉMIQUE DE TOUS LES FICHIERS (.md, .txt, .tex)
# ==============================================================================

ROOT_DIR = r"c:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"

# Liste de paires (pattern, replacement)
replacements = [
    # Hyper-Structure titres
    (r"CONCLUSION DE CONVERGENCE", "CONCLUSION DE CONVERGENCE"),
    (r"Conclusion de Convergence", "Conclusion de Convergence"),
    (r"COMPLÉTUDE DU SYSTÈME", "COMPLÉTUDE DU SYSTÈME"),
    (r"Complétude du Système", "Complétude du Système"),
    
    # Stabilité / Canonicité -> Stabilité/Canonicité
    (r"STABILITÉ ASYMPTOTIQUE TOTALE", "STABILITÉ ASYMPTOTIQUE TOTALE"),
    (r"Stabilité Asymptotique Totale", "Stabilité Asymptotique Totale"),
    (r"Stabilité / Canonicité", "Stabilité / Canonicité"),
    (r"Canonique", "Canonique"),
    (r"Canonique", "Canonique"),
    (r"stabilité", "stabilité"),
    (r"canonique", "canonique"),
    (r"canonique", "canonique"),
    
    # Canonical -> Canonical/Stable
    (r"CANONICAL UNIFICATION", "CANONICAL UNIFICATION"),
    (r"CANONICAL", "CANONICAL"),
    (r"Canonical", "Canonical"),
    (r"canonical", "canonical"),
    
    # Principal Investigatore -> PI/Auteur
    (r"L'Auteur Principal", "L'Auteur Principal"),
    (r"Principal Investigator", "Principal Investigator"),
    
    # Math/Physics
    (r"mu = 1\.0", r"$\\$\mu = 1.0$$"),
    (r"mu=1\.0", r"$\\$\mu = 1.0$$"),
    (r"SATURATED INFORMATION FRAMEWORK", "SATURATED INFORMATION FRAMEWORK"),
    (r"SINGULARITY BRIDGE (UNIFIED FRAMEWORK)", "SINGULARITY BRIDGE (UNIFIED FRAMEWORK) (UNIFIED FRAMEWORK)"),
]

def process_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in replacements:
            # On utilise re.sub pour supporter les regex basiques
            new_content = re.sub(pattern, replacement, new_content)
            
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except:
        return False
    return False

def main():
    print("Démarrage de la normalisation massive...")
    count = 0
    scanned = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(x in root for x in [".git", "__pycache__"]):
            continue
        for file in files:
            if file.endswith((".md", ".txt", ".tex", ".py", ".json")):
                scanned += 1
                if process_file(os.path.join(root, file)):
                    count += 1
    print(f"\nTerminé. {scanned} fichiers scannés.")
    print(f"{count} fichiers normalisés au format académique.")

if __name__ == "__main__":
    main()
