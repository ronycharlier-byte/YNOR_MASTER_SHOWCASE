# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# EXTRACTEUR HYPER-KNOWLEDGE v3.0 (MAXIMUM POWER)
# Prepared pour GPT Store & AGI Intelligence
# =============================================================================
import sys
import os
import io
import zipfile
import PyPDF2
import json
import re
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# =====================================================
# ANALYSE ET EXTRACTION PROFONDE
# =====================================================
def harvest_axioms(text):
    """Extrait les regles supremes du texte pour le Super-Index."""
    axioms = []
    # Recherche de patterns : Axiome 1, Loi, Mu = , etc.
    patterns = [
        r"(Axiome\s+\d+[:\s-\-].+)",
        r"(Loi\s+\d+[:\s-\-].+)",
        r"(mu\s*=\s*alpha\s*-\s*[^\n]+)",
        r"([Pp]rincipe\s+nucleaire[^.]+)"
    ]
    for p in patterns:
        matches = re.findall(p, text)
        axioms.extend(matches)
    return list(set(axioms))[:20]

def extract_full_pdf(pdf_file_obj, filename):
    try:
        reader = PyPDF2.PdfReader(pdf_file_obj)
        text = ""
        # On passe a 50 pages max (couverture totale de vos traites)
        num_pages = min(len(reader.pages), 50)
        for i in range(num_pages):
            text += reader.pages[i].extract_text() + "\n"
        return text
    except Exception as e:
        print(f"  [ERR PDF] {filename} : {e}")
        return ""

# =====================================================
# MOTEUR DE HYPER-FUSION
# =====================================================
def run_hyper_fusion():
    base_dir = r"c:\Users\ronyc\Desktop\MDL Ynor Architecture"
    output_dir = os.path.join(base_dir, "MDL_Ynor_Framework")
    
    # --- EXECUTION DES VALidATEURS ET EVOLUTION AVANT FUSION ---
    try:
        import subprocess
        print(" Appel des Gardiens JURIDIQUES, SCIENTIFIQUES et VOLUTIFS...")
        subprocess.run(["python", os.path.join(output_dir, "ynor_legal_harvester.py")], check=True)
        subprocess.run(["python", os.path.join(output_dir, "ynor_empirical_validator.py")], check=True)
        subprocess.run(["python", os.path.join(output_dir, "ynor_asymptotic_evolution.py")], check=True)
        subprocess.run(["python", os.path.join(output_dir, "ynor_master_offensive.py")], check=True)
        subprocess.run(["python", os.path.join(output_dir, "ynor_strategic_surveillance.py")], check=True)
        subprocess.run(["python", os.path.join(output_dir, "ynor_hyper_retention.py")], check=True)
    except Exception as e:
        print(f"  [AVERT] Gardiens indisponibles : {e}")

    # Structure Alpha du Corpus
    hyper_corpus = {
        "identity": {
            "master": "Charlier Rony",
            "role": "Architecte Supreme",
            "project": "MDL YNOR - Unified AGI Architecture",
            "status": "Maximum Intelligence Level",
            "self_improvement": "ACTIVE (Asymptotic Evolution Loop Enabled)",
            "surveillance": "ACTIVE (Strategic Intelligence & OSINT)",
            "legal_status": "EU AI ACT / RGPD COMPLIANT",
            "laws_summary": []
        },
        "structure_map": {}, 
        "knowledge_nodes": []
    }

    print(" DEMARRAGE HYPER-FUSION MDL YNOR v3.0 ")

    all_raw_text = ""

    for root, dirs, files in os.walk(base_dir):
        if any(skip in root for skip in ["__pycache__", ".git", ".cloudflared", "logs"]):
            continue

        rel_path = os.path.relpath(root, base_dir)
        hyper_corpus["structure_map"][rel_path] = files

        for filename in files:
            filepath = os.path.join(root, filename)
            ext = filename.lower().split('.')[-1] if '.' in filename else ""

            # --- TRAITEMENT TEXTE / CODE ---
            if ext in ["py", "md", "txt", "json", "ps1"]:
                if filename == "mdl_global_knowledge.json": continue
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    
                    all_raw_text += content + "\n"
                    hyper_corpus["knowledge_nodes"].append({
                        "id": filename,
                        "class": "CODE_SOURCE" if ext in ["py", "ps1"] else "THESE_DOCUMENTAIRE",
                        "content": content[:15000] # Augmentation de la capacite par noeud
                    })
                    print(f"  [INDEXED] {filename}")
                except: pass

            # --- TRAITEMENT PDF ---
            elif ext == "pdf":
                with open(filepath, "rb") as f:
                    text = extract_full_pdf(f, filename)
                if text:
                    all_raw_text += text + "\n"
                    hyper_corpus["knowledge_nodes"].append({
                        "id": filename,
                        "class": "CORE_THEORY_PDF",
                        "content": text
                    })
                    print(f"  [CAPTURED] {filename} (Full Text)")

    # --- GENERATION DU NOYAU AXIOMATIQUE ---
    print(" Extraction des Lois Supremes...")
    hyper_corpus["identity"]["laws_summary"] = harvest_axioms(all_raw_text)

    # --- SAUVEGARDE FINALE ---
    out_path = os.path.join(output_dir, "mdl_global_knowledge.json")
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(hyper_corpus, out, indent=2, ensure_ascii=False)

    print("\n" + "" * 60)
    print("  [MAXIMUM REACHED] Corpus MDL Ynor unifie avec succes.")
    print(f"  [FICHIER] {out_path}")
    print("  [STATUT] Pret pour importation GPT Store.")
    print("" * 60)

if __name__ == "__main__":
    run_hyper_fusion()



