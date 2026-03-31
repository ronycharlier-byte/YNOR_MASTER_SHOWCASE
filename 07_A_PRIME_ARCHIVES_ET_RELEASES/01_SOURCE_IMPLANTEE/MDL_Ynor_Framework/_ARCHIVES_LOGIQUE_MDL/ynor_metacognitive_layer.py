# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import client # On rutilise le client OpenAI configur

class MetacognitiveGovernor:
    """
    Couche de Mtacognition MDL Ynor : Surveille et value l'efficacit de l'IA Gouverneur.
    """
    def __init__(self):
        self.intervention_history = []
        self.last_mutation_time = -1.0
        self.failure_counter = 0

    def evaluate_intervention(self, current_t, current_mu):
        """
        Analyse si la prcdente mutation a t efficace.
        Si une nouvelle crise survient moins de 2 units de temps aprs la dernire, 
        on considre que l'IA a fait une erreur de jugement.
        """
        if self.last_mutation_time > 0 and (current_t - self.last_mutation_time) < 2.0:
            if current_mu <= 0.0:
                print("\n[METACOGNITION] DTECTION D'CHEC RCURSANT. L'IA a sous-estim la crise.")
                self.failure_counter += 1
                return True # Besoin d'une rflexion critique
        return False

    def critical_reflection(self, mu, state, history):
        """
        Appel de rflexion mtacognitive  OpenAI.
        L'IA doit analyser ses propres erreurs passes.
        """
        print("\n[METACOGNITION] Phase de Rflexion Critique en cours...")
        
        history_str = json.dumps(history[-3:]) # On donne les 3 dernires interventions
        
        prompt = f"""
        [DIRECTIVE METACOGNITIVE : ANALYSE D'CHEC]
        Vous tes le gouverneur d'un systme MDL Ynor qui vient de RECHUTER.
        tat actuel mu : {mu}. volution S : {state}.
        Historique de vos dernires dcisions : {history_str}.
        
        VOTRE MISSION : 
        1. Analysez pourquoi vos prcdentes mutations ont t insuffisantes.
        2. Proposez une mutation PIVOT (changement de logique Drastique).
        3. Augmentez la svrit de 300%.
        
        RPONSE JSON : {{ "new_mutation_rate": float, "analysis": "string" }}
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
    print("   SIMULATION AVEC COUCHE DE MTACOGNITION (OVERLAY)")
    print("=====================================================\n")

    # Systme trs instable et rsistant (Inertie forte)
    sys = YnorSystem(2, lambda S: 2.0 * S, lambda S: 0.5 * S)
    meta = MetacognitiveGovernor()
    
    S = np.array([2.0, 2.0])
    t = 0.0
    dt = 0.4
    
    for step in range(25):
        mu = sys.measure_dissipative_margin(S)
        regime = check_viability_regime(mu)
        
        print(f"t={t:<4.1f} | mu={mu:<5.2f} | {regime:<10}")

        # La Mtacognition surveille le systme
        needs_reflection = meta.evaluate_intervention(t, mu)

        if mu <= 0.0:
            if needs_reflection:
                # CHEC DTECT : On demande  l'IA de rflchir
                decision = meta.critical_reflection(mu, S.tolist(), meta.intervention_history)
                r = decision["new_mutation_rate"]
                print(f"[META-ANALYSE] : {decision['analysis']}")
            else:
                # Premire crise ou crise espace : On demande une mutation standard
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
            print(f"[SYSTME RECONSTRUIT] Taux: +{r*100}% | Prochaine vrification mtacognitive active.\n")

        # Dynamique
        S = S + sys.dynamics(t, S) * dt
        t += dt
        time.sleep(0.1)

if __name__ == "__main__":
    run_metacognitive_simulation()



