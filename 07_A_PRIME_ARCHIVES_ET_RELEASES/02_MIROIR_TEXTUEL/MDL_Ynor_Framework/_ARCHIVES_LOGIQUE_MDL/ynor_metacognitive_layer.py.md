# MIROIR TEXTUEL - ynor_metacognitive_layer.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\ynor_metacognitive_layer.py
Taille : 4984 octets
SHA256 : 967dbf3c5f90331d1ee7a7016465dbe71a0a2008e6d1979efc4a24188db7c0e8

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import client # On réutilise le client OpenAI configuré

class MetacognitiveGovernor:
    """
    Couche de Métacognition MDL Ynor : Surveille et évalue l'efficacité de l'IA Gouverneur.
    """
    def __init__(self):
        self.intervention_history = []
        self.last_mutation_time = -1.0
        self.failure_counter = 0

    def evaluate_intervention(self, current_t, current_mu):
        """
        Analyse si la précédente mutation a été efficace.
        Si une nouvelle crise survient moins de 2 unités de temps après la dernière, 
        on considère que l'IA a fait une erreur de jugement.
        """
        if self.last_mutation_time > 0 and (current_t - self.last_mutation_time) < 2.0:
            if current_mu <= 0.0:
                print("\n[METACOGNITION] DÉTECTION D'ÉCHEC RÉCURSANT. L'IA a sous-estimé la crise.")
                self.failure_counter += 1
                return True # Besoin d'une réflexion critique
        return False

    def critical_reflection(self, mu, state, history):
        """
        Appel de réflexion métacognitive à OpenAI.
        L'IA doit analyser ses propres erreurs passées.
        """
        print("\n[METACOGNITION] Phase de Réflexion Critique en cours...")
        
        history_str = json.dumps(history[-3:]) # On donne les 3 dernières interventions
        
        prompt = f"""
        [DIRECTIVE METACOGNITIVE : ANALYSE D'ÉCHEC]
        Vous êtes le gouverneur d'un système MDL Ynor qui vient de RECHUTER.
        État actuel mu : {mu}. Évolution S : {state}.
        Historique de vos dernières décisions : {history_str}.
        
        VOTRE MISSION : 
        1. Analysez pourquoi vos précédentes mutations ont été insuffisantes.
        2. Proposez une mutation PIVOT (changement de logique Drastique).
        3. Augmentez la sévérité de 300%.
        
        RÉPONSE JSON : {{ "new_mutation_rate": float, "analysis": "string" }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            return {"new_mutation_rate": 5.0, "analysis": "Meta-Error, applying maximum safety coefficient."}

def run_metacognitive_simulation():
    print("=====================================================")
    print("   SIMULATION AVEC COUCHE DE MÉTACOGNITION (OVERLAY)")
    print("=====================================================\n")

    # Système très instable et résistant (Inertie forte)
    sys = YnorSystem(2, lambda S: 2.0 * S, lambda S: 0.5 * S)
    meta = MetacognitiveGovernor()
    
    S = np.array([2.0, 2.0])
    t = 0.0
    dt = 0.4
    
    for step in range(25):
        mu = sys.measure_dissipative_margin(S)
        regime = check_viability_regime(mu)
        
        print(f"t={t:<4.1f} | mu={mu:<5.2f} | {regime:<10}")

        # La Métacognition surveille le système
        needs_reflection = meta.evaluate_intervention(t, mu)

        if mu <= 0.0:
            if needs_reflection:
                # ÉCHEC DÉTECTÉ : On demande à l'IA de réfléchir
                decision = meta.critical_reflection(mu, S.tolist(), meta.intervention_history)
                r = decision["new_mutation_rate"]
                print(f"[META-ANALYSE] : {decision['analysis']}")
            else:
                # Première crise ou crise espacée : On demande une mutation standard
                from ynor_ai_governor import get_ai_reconstruction_strategy
                print("[IA] Demande de mutation standard...")
                strategy = get_ai_reconstruction_strategy(mu, S.tolist())
                r = strategy["mutation_rate"]

            # Appliquer la mutation
            old_D = sys.D
            sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
            
            # Logger l'intervention
            meta.intervention_history.append({"t": t, "mu_at_t": mu, "rate_applied": r})
            meta.last_mutation_time = t
            print(f"[SYSTÈME RECONSTRUIT] Taux: +{r*100}% | Prochaine vérification métacognitive activée.\n")

        # Dynamique
        S = S + sys.dynamics(t, S) * dt
        t += dt
        time.sleep(0.1)

if __name__ == "__main__":
    run_metacognitive_simulation()

```