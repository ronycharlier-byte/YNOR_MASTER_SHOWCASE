# MIROIR TEXTUEL - ynor_ai_governor.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\ynor_ai_governor.py
Taille : 2616 octets
SHA256 : ad7a188df4a115408c666da817a59230050963561a514f5b5371ac50ef11dd2a

```text
from dotenv import load_dotenv
load_dotenv()

﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import openai
import json
import os

# --- CONFIGURATION ---
# Remplacez "VOTRE_CLE_ICI" par votre clé API OpenAI réelle.
# Ou définissez la variable d'environnement OPENAI_API_KEY.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "os.getenv("OPENAI_API_KEY", "REDACTED")-DMJnu_NGYDzKSnPfRJiT3BlbkFJGnXK8Y2gM3UvZwEPk8atrYYgu-kEElRRXwgctK1Re7sMq9GRjqvoRuTvhgIl0pf9xaGS4Q0AAA")

# Vérification masquée (Security Check)
if OPENAI_API_KEY and OPENAI_API_KEY != "VOTRE_CLE_ICI":
    masked_key = f"{OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-5:]}"
    print(f"[AI SECURITY] Clé utilisée : {masked_key} (Longueur: {len(OPENAI_API_KEY)})")
else:
    print("[AI SECURITY] ALERTE : Aucune clé renseignée dans ynor_ai_governor.py")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_ai_reconstruction_strategy(mu, state):
    """
    Demande à l'IA une stratégie de mutation pour restaurer la marge mu > 0.
    """
    print("\n[AI GOVERNOR] Appel à l'Intelligence Artificielle pour résolution de crise...")
    
    prompt = f"""
    [DIRECTIVE PRIORITAIRE : STABILISATION BRUTALE]
    Marge dissipative mu = {mu} (seuil de sécurité : 0.01).
    État actuel S = {state}.
    
    ACTION : Proposez un taux de mutation 'r' DECISIF pour augmenter l'opérateur D(S). 
    Vous devez restaurer une marge mu > 2.0 en UN SEUL CYCLE. Soyez sévère et déterminez le taux 'r' optimal.
    
    RÉPONSE FORMAT : JSON uniquement {{ "mutation_rate": float, "explanation": "string" }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        strategy = json.loads(response.choices[0].message.content)
        return strategy
    except Exception as e:
        print(f"[ERREUR AI] Impossible de contacter OpenAI : {e}")
        # Stratégie de secours (fail-safe) : +200% de dissipation
        return {"mutation_rate": 2.0, "explanation": "Fallback strategy due to API error."}

if __name__ == "__main__":
    # Test à vide
    print(get_ai_reconstruction_strategy(-1.0, [2.0, 2.0]))

```