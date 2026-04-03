import os
from datetime import datetime

# ==============================================================================
# MDL YNOR PROMPT GENERATOR - V10.8 (TOTAL DIAMOND)
# ==============================================================================

PROMPT_PATH = r"c:\Users\ronyc\Desktop\FRACTAL_Symétrie Bilatérale_UNIVERSEL\MDL_YNOR_V7_1_DISTRIBUTION\PROMPT_SYSTEME_V10_8_OPTIMIZED.txt"

def generate_payload(user_query, model="gpt-4o"):
    """
    Génère un payload JSON pour l'API OpenAI avec le Prompt Système Inviolable.
    """
    if not os.path.exists(PROMPT_PATH):
        return f"ERREUR : Prompt Système introuvable à {PROMPT_PATH}"
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        system_content = f.read()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_query}
        ],
        "temperature": 0.0,
        "top_p": 1.0,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    
    return payload

if __name__ == "__main__":
    test_query = "Résoudre formellement le problème de Navier-Stokes en utilisant la mu-stabilité du core Ynor."
    payload = generate_payload(test_query)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] PAYLOAD GÉNÉRÉ POUR OPENAI API (V10.8) :")
    import json
    print(json.dumps(payload, indent=2, ensure_ascii=False))
