import os
import json
import re
import shutil
import uuid

# =====================================================================
# 🛡️ MDL YNOR - SECURE UPLOAD OBFUSCATOR v1.0
# Ce script prépare votre dossier d'upload pour le GPT Store en :
# 1. Masquant les informations personnelles (emails, chemins)
# 2. Renommant les fichiers avec des noms aléatoires
# 3. Créant une archive propre pour l'upload final
# =====================================================================

SOURCE_DIR = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\MDL_YNOR_GPT_UPLOAD_V3"
OUTPUT_DIR = r"C:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\MDL_YNOR_GPT_FINAL_DIST"
MAPPING_LOG = os.path.join(OUTPUT_DIR, "obfuscation_mapping_DONT_UPLOAD.json")

# Regex de détection
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@mdlstrategy\.[a-zA-Z0-9.-]+" # Cible spécifique MDL
PATH_REGEX = r"C:\\Users\\[a-zA-Z0-9 ]+\\[a-zA-Z0-9 ]+" # Vise les chemins Windows locaux

def redact_content(content):
    # Remplacer les emails
    content = re.sub(EMAIL_REGEX, "[REDACTED_AUTHOR_EMAIL]", content)
    # Remplacer les chemins Windows
    content = re.sub(PATH_REGEX, "[REDACTED_LOCAL_PATH]", content)
    # Autres remplacements de sécurité (codes sha, etc.)
    content = re.sub(r"[a-f0-9]{32,64}", "[REDACTED_SECURE_TOKEN]", content)
    return content

def obfuscate_and_clean():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    mapping = {}
    print(f"🚀 Initialisation du moteur d'obfuscation Ynor...")

    for filename in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, filename)
        if os.path.isdir(src_path):
            continue

        # Générer un nouveau nom (UUID + extension originale ou .bin)
        name, ext = os.path.splitext(filename)
        new_id = str(uuid.uuid4())[:8]
        new_filename = f"ynor_node_{new_id}{ext}"
        
        # Pour les JSON, on peut forcer l'obfuscation même de l'extension
        if ext == ".json":
            new_filename = f"ynor_logic_{new_id}.bin"

        dest_path = os.path.join(OUTPUT_DIR, new_filename)
        mapping[new_filename] = filename

        print(f"  [*] Traitement : {filename} -> {new_filename}...")

        try:
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Nettoyage
            clean_content = redact_content(content)

            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
        except Exception as e:
            print(f"  [⚠️] Erreur sur {filename}: {str(e)}")
            # Copie brute si échec de lecture texte (pdf, etc.)
            shutil.copy2(src_path, dest_path)

    # Sauvegarder le mapping pour le créateur
    with open(MAPPING_LOG, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=4)

    print(f"\n✅ OPÉRATION TERMINÉE.")
    print(f"Dossier final : {OUTPUT_DIR}")
    print(f"⚠️ NE JAMAIS UPLOADER LE FICHIER : {os.path.basename(MAPPING_LOG)}")
    print(f"Compressez le reste du dossier pour votre GPT Store.")

if __name__ == "__main__":
    obfuscate_and_clean()
