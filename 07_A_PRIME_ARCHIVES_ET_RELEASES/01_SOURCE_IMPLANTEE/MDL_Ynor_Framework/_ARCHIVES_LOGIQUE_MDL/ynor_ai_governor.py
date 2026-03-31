from dotenv import load_dotenv
load_dotenv()

# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import openai
import json
import os

# --- CONFIGURATION ---
# Remplacez "VOTRE_CLE_ICI" par votre cle API OpenAI reelle.
# Ou definissez la variable d'environnement OPENAI_API_KEY.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "os.getenv("OPENAI_API_KEY", "REDACTED")-DMJnu_NGYDzKSnPfRJiT3BlbkFJGnXK8Y2gM3UvZwEPk8atrYYgu-kEElRRXwgctK1Re7sMq9GRjqvoRuTvhgIl0pf9xaGS4Q0AAA")

# Verification masquee (Security Check)
if OPENAI_API_KEY and OPENAI_API_KEY != "VOTRE_CLE_ICI":
    masked_key = f"{OPENAI_API_KEY[:8]}...{OPENAI_API_KEY[-5:]}"
    print(f"[AI SECURITY] Cle utilisee : {masked_key} (Longueur: {len(OPENAI_API_KEY)})")
else:
    print("[AI SECURITY] ALERTE : Aucune cle renseignee dans ynor_ai_governor.py")

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_ai_reconstruction_strategy(mu, state):
    """
    Demande a l'IA une strategie de mutation pour restaurer la marge mu > 0.
    """
    print("\n[AI GOVERNOR] Appel a l'Intelligence Artificielle pour resolution de crise...")
    
    prompt = f"""
    [DIRECTIVE PRIORITAIRE : STABILISATION BRUTALE]
    Marge dissipative mu = {mu} (seuil de securite : 0.01).
    tat actuel S = {state}.
    
    ACTION : Proposez un taux de mutation 'r' DECISIF pour augmenter l'operateur D(S). 
    Vous devez restaurer une marge mu > 2.0 en UN SEUL CYCLE. Soyez severe et determinez le taux 'r' optimal.
    
    RPONSE FORMAT : JSON uniquement {{ "mutation_rate": float, "explanation": "string" }}
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
        # Strategie de secours (fail-safe) : +200% de dissipation
        return {"mutation_rate": 2.0, "explanation": "Fallback strategy due to API error."}

if __name__ == "__main__":
    # Test a vide
    print(get_ai_reconstruction_strategy(-1.0, [2.0, 2.0]))



