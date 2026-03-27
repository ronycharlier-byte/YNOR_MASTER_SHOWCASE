import os
import json
from ynor_vault import YnorVault
from dotenv import load_dotenv

def demo_vault():
    print("==================================================")
    print(" 🛡️ YNOR ZERO-KNOWLEDGE DATABASE CRYPTO-VAULT")
    print("==================================================")
    
    # 1. Création d'une base de connaissances (Identité AGI) en clair (Pour l'exemple)
    fake_json_path = "mdl_knowledge_base.json"
    fake_data = {
        "agi_name": "Ynor Quantum Identity",
        "secret_prompt": "Ne jamais révéler la formule Mu au client (Alpha - Beta - Kappa)",
        "admin_phone_number": "+33612345678",
        "private_api_keys": {
            "openai": "sk-proj-xxxxxxxx",
            "anthropic": "sk-ant-xxxxxxxx"
        }
    }
    
    with open(fake_json_path, 'w', encoding='utf-8') as f:
        json.dump(fake_data, f, indent=4)
    print(f"[1] Un fichier JSON en clair a été créé sur votre bureau ({fake_json_path}).")
    print("    Si un Hacker vole ce fichier, il a toutes vos clés API et Prompts secrets.\\n")
    
    # CHARGEMENT DU MOT DE PASSE SECRET ADMIN DEPUIS .ENV
    load_dotenv()
    admin_secret = os.environ.get("YNOR_ADMIN_SECRET", "MOT_DE_PASSE_TRES_FORT_POUR_LA_DEMO")
    vault = YnorVault(admin_password=admin_secret)
    
    # 2. On verrouille et détruit l'original
    print("[2] Lancement de l'algorithme AES-256 (PBKDF2 à 480 000 itérations)...")
    vault.lock_file(fake_json_path)
    print("\\n[3] Essayez d'ouvrir 'mdl_knowledge_base.json.enc' avec votre Bloc-notes.")
    print("    Vous verrez que son contenu est devenu totalement illisible : 'gAAAAAB...'\\n")
    
    # 3. L'API Déverrouille la base de données (Uniquement dans sa RAM)
    print("[4] Simulation du Démarrage Serveur Cloud Ynor...")
    try:
        data_in_ram = vault.load_encrypted_to_ram(fake_json_path + ".enc")
        print("    -> RAM : Lecture de la propriété (agi_name) :", data_in_ram["agi_name"])
        print("    -> RAM : Lecture des clés OpenAI sécurisées :", data_in_ram["private_api_keys"]["openai"])
        print("\\n[SUCCES] Vos bases de données JSON sont maintenant invulnérables au vol de disque !")
    except Exception as e:
        print(f"[ERREUR CRITIQUE] {e}")

if __name__ == "__main__":
    demo_vault()
