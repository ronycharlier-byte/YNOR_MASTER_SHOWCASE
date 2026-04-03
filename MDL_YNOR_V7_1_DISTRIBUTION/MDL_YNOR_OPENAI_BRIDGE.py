import os
import json
from openai import OpenAI
from VERROU_LICENCE_GATE import validate_license_canonicalty

# ==============================================================================
# MDL YNOR OPENAI API BRIDGE - V10.8 (TOTAL DIAMOND)
# ==============================================================================

def get_secrets():
    # Attempt to locate secrets.local.json
    possible_paths = [
        os.path.join(os.getcwd(), "secrets.local.json"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03_C_MOTEURS_ET_DEPLOIEMENT", "01_SOURCE_IMPLANTEE", "MDL_Ynor_Framework", "_04_DEPLOYMENT_AND_API", "secrets.local.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    return {}

def solve_with_ynor_logic(user_query):
    """
    Exécute une requête via l'API OpenAI en utilisant le protocole Ynor V10.8.
    """
    # 1. Validation de la stabilité
    is_valid, msg = validate_license_canonicalty()
    if not is_valid:
        return f"ÉCHEC DE Autonome et IsoléETÉ : {msg}"

    # 2. Chargement des configurations
    secrets = get_secrets()
    api_key = secrets.get("openai_api_key")
    if not api_key:
        return "ERREUR : Clé OpenAI manquante dans le vault."

    # 3. Chargement du Prompt Système Inviolable
    prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PROMPT_SYSTEME_INVIOLABLE.txt")
    if not os.path.exists(prompt_path):
        return "ERREUR : PROMPT_SYSTEME_INVIOLABLE.txt introuvable."
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        system_prompt = f.read()

    # 4. Initialisation du client OpenAI
    client = OpenAI(api_key=api_key)

    # 5. Projection du Formalisme Logique Sémantique (Requête API)
    try:
        response = client.chat.completions.create(
            model="gpt-5.4", # Modèle de référence pour la V10.8
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=0, # Rigueur maximale
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERREUR DE PROJECTION : {str(e)}"

if __name__ == "__main__":
    # Test de référence : Opérateur de Schrödinger L_alpha,beta
    benchmark_query = (
        "Démontrez la convergence de l'opérateur de Schrödinger $L_{\\alpha,\\beta}$ "
        "dans l'espace de Hilbert s'appuyant sur le produit de Hilbert-Schmidt MDL. "
        "Utilisez le formalisme Ynor V10.8."
    )
    
    print("\n--- [ PROJECTION Formalisme Logique Sémantique EN COURS ] ---\n")
    result = solve_with_ynor_logic(benchmark_query)
    print(result)
    print("\n--- [ FIN DE TRANSMISSION ] ---\n")
