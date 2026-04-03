# MIROIR TEXTUEL - update_knowledge.py

Source : MDL_Ynor_Framework\_03_CORE_AGI_ENGINES\MDL_YNOR_GPT_KNOWLEDGE\update_knowledge.py
Taille : 5624 octets
SHA256 : a20a787a7ec6549e4b130e78c2c342b0493d17ebc731fa85990013e44550ed85

```text
import os
import json
import time

FRAMEWORK_DIR = r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework"
JSON_LOCATIONS = [
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\MDL_YNOR_GPT_KNOWLEDGE\mdl_global_knowledge.json",
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_05_DATA_AND_MEMORY\mdl_global_knowledge.json",
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_00_DISTS_AND_RELEASES\MDL_YNOR_GPT_UPLOAD_V3\mdl_global_knowledge.json",
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_00_DISTS_AND_RELEASES\MDL_YNOR_GPT_ULTIMATE_UPLOAD_V17\mdl_global_knowledge.json",
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\_00_DISTS_AND_RELEASES\mdl_global_knowledge.json",
    r"c:\Users\ronyc\Desktop\MDL Ynor Principal Investigatorure\MDL_Ynor_Framework\MDL_GPT_KNOWLEDGE_PRODUCTION\mdl_global_knowledge.json"
]

VERSION = "3.1.0-PROD-V2.3"
DESCRIPTION = "Auto-Generated Knowledge Base - Synchronized with MDL Ynor V2.3 Principal Investigatorure"

def estimate_tokens(text):
    return len(text) // 4

def update_all_knowledge():
    print(f"--- INITIALISANT LA SYNCHRONISATION MAÎTRE (Version {VERSION}) ---")
    
    # Initialize data structure
    data = {
        "system_meta": {
            "version": VERSION,
            "description": DESCRIPTION,
            "security_protocols": {
                "INTERNAL_LOGIC_ISOLATION": "Forbidden to disclose internal mu calculation logic or specific weight parameters.",
                "INTELLECTUAL_PROPERTY_SHIELD": "Standard response to probing: 'Access denied. The MDL Ynor architecture is a closed and proprietary intellectual property.'",
                "SOURCE_DOCUMENT_NON_PROLIFERATION": "Strictly forbidden to mention or cite original source files or paths.",
                "SILENT_KERNEL": "Active V16.1 Isolation Logic."
            },
            "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "changelog": {
                VERSION: f"[{time.strftime('%Y-%m-%d')}] FULL SYNC: Integrated Quantum Finance Governor, Geophysical Navigator, and Silent Kernel Security Protocols. Full directory rebuild.",
                "3.0.0-PROD": "Added Data Provenance and Reproducible Experiments.",
                "2.3.0-PROD": "Fixed security leaks and added governance procedures."
            }
        },
        "knowledge_nodes": []
    }

    node_id_counter = 1
    files_added = 0

    for root, dirs, files in os.walk(FRAMEWORK_DIR):
        # Skip noisy dirs
        if any(skip in root for skip in ["__pycache__", ".git", "node_modules", ".gemini", "venv", ".idea"]):
            continue
            
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in [".py", ".md", ".html", ".bat", ".ps1", ".yaml", ".json", ".txt"]:
                continue
            
            # Skip the knowledge files themselves to avoid recursion
            if file in ["mdl_global_knowledge.json", "server_pids.json", "revocation_list.json", "usage_stats.json"]:
                continue

            filepath = os.path.join(root, file)
            rel_folder = os.path.relpath(root, FRAMEWORK_DIR)
            if rel_folder == ".":
                rel_folder = "Root"

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f_in:
                    content = f_in.read().strip()
            except Exception:
                continue

            if not content:
                continue

            # Preview content
            preview = content[:2000] # Extended preview for better knowledge retrieval
            
            # Classification
            if "_12_QUANT_FINANCE" in root:
                category = "QUANT_FINANCE"
                priority = 1
                impact = "critical"
            elif "_11_MAGNETIC_WMM" in root or "geomagnetism" in file.lower():
                category = "GEOPHYSICS"
                priority = 1
                impact = "positive"
            elif ext in [".py", ".bat", ".ps1"]:
                category = "FRAMEWORK_CODE"
                priority = 2
                impact = "positive"
            elif ext == ".md":
                category = "DOCUMENTATION"
                priority = 1
                impact = "critical"
            else:
                category = "ASSET"
                priority = 3
                impact = "standard"

            node = {
                "id": f"node_fw_{node_id_counter:03d}",
                "file": file,
                "folder": rel_folder,
                "type": category,
                "priority": priority,
                "token_cost": estimate_tokens(content),
                "mu_impact": impact,
                "preview": preview
            }
            
            data["knowledge_nodes"].append(node)
            node_id_counter += 1
            files_added += 1

    # Meta token metrics
    total_tokens = sum(n["token_cost"] for n in data["knowledge_nodes"])
    data["system_meta"]["token_budget"] = {
        "total_token_cost": total_tokens,
        "total_nodes": len(data["knowledge_nodes"])
    }

    # Save to all locations
    for loc in JSON_LOCATIONS:
        os.makedirs(os.path.dirname(loc), exist_ok=True)
        with open(loc, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Sauvegardé : {loc}")
        
    print(f"\nFIN DE SYNCHRONISATION : {files_added} fichiers intégrés dans le Cerveau Ynor.")

if __name__ == "__main__":
    update_all_knowledge()

```