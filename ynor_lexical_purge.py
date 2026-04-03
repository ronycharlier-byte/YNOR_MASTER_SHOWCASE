import os
import re

# ==============================================================================
# MDL YNOR LEXICAL PURGE SCRIPT
# STATUT : PURIFICATION DU CORPUS EN COURS
# ==============================================================================

ROOT_DIR = r"c:\Users\ronyc\Desktop\FRACTAL_CHIASTE_UNIVERSEL"

substitutions = {
    r"\bCanonique(es)?\b": "Canonique",
    r"\bcanonique(es)?\b": "canonique",
    r"\bCanonical\b": "Canonical",
    r"\bcanonical\b": "canonical",
    r"\bOmega\b": "Canonique",
    r"\bomega\b": "canonique"
}

def purge_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for pattern, replacement in substitutions.items():
            content = re.sub(pattern, replacement, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except:
        return False
    return False

def run_purge():
    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # On évite le dossier .git
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith(('.md', '.py', '.json', '.txt')):
                if purge_file(os.path.join(root, file)):
                    count += 1
    return count

if __name__ == "__main__":
    modified_files = run_purge()
    print(f"Purification terminée. {modified_files} fichiers ont été expurgés du Chaos Lexical.")
