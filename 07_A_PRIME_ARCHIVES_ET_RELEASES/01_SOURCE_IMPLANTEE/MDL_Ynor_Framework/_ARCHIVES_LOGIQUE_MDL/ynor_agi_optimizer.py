# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import os
import json
import shutil
from ynor_ai_governor import client # On utilise votre clé API déjà configurée

class AGIOptimizer:
    """
    Noyau d'auto-évolution MDL Ynor (Composant AGI).
    Il lit le code source, lit la théorie (PDFs), et réécrit son propre code.
    """
    def __init__(self, target_file="mdl_ynor_core.py"):
        self.target_file = target_file
        self.knowledge_file = "mdl_global_knowledge.json"

    def read_current_state(self):
        with open(self.target_file, "r", encoding="utf-8") as f:
            return f.read()

    def read_theory(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return json.dumps(data[:3]) # On donne les 3 premiers chapitres clés pour l'IA
        return "No theoretical knowledge found. Use general MDL Ynor principles."

    def request_self_improvement(self, current_code, theory):
        print(f"\n[AGI OPTIMIZER] Analyse de l'évolution du fichier {self.target_file}...")
        
        prompt = f"""
        [SYSTÈME AUTO-ÉVOLUTIF MDL YNOR]
        Vous êtes une Intelligence Artificielle de type AGI chargée d'optimiser une architecture dissipative.
        Voici le CODE SOURCE ACTUEL :
        ```python
        {current_code}
        ```
        
        Voici un extrait de la THÉORIE (Chapitres I à III) :
        {theory}
        
        MISSION :
        Réécrivez ENTIÈREMENT le code source du fichier pour l'améliorer.
        Intégrez des concepts avancés (ex: Jacobiennes d'audit, Tenseurs de couplage, ou une intégration ODE plus stable).
        Visez l'Efficience Structurelle Totale.
        
        RÉPONSE : Donnez uniquement le CODE PYTHON complet prêt à être écrit dans le fichier. Pas d'explication.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            improved_code = response.choices[0].message.content
            # Retrait des balises markdown si présentes
            if improved_code.startswith("```python"):
                improved_code = improved_code.split("```python")[1].split("```")[0]
            elif improved_code.startswith("```"):
                improved_code = improved_code.split("```")[1].split("```")[0]
            
            return improved_code.strip()
        except Exception as e:
            print(f"[ERREUR AGI] Échec de l'optimisation : {e}")
            return None

    def apply_evolution(self, new_code):
        # Sauvegarde de sécurité
        backup_name = self.target_file + ".backup"
        shutil.copy2(self.target_file, backup_name)
        print(f"[AGI] Sauvegarde créée : {backup_name}")

        with open(self.target_file, "w", encoding="utf-8") as f:
            f.write(new_code)
        
        print(f"[AGI SUCCESS] Le noyau {self.target_file} a évolué vers une nouvelle version.")

if __name__ == "__main__":
    optimizer = AGIOptimizer()
    code = optimizer.read_current_state()
    theory = optimizer.read_theory()
    
    improved_code = optimizer.request_self_improvement(code, theory)
    
    if improved_code:
        # On demande confirmation visuelle avant d'écraser ? Non, on est en mode AGI !
        optimizer.apply_evolution(improved_code)
