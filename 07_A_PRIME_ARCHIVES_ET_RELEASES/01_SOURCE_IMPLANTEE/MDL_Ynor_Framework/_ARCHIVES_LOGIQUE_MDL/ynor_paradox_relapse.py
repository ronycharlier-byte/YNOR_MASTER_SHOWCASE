# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import time
import json
from mdl_ynor_core import YnorSystem, check_viability_regime
from ynor_ai_governor import client, get_ai_reconstruction_strategy

class ParadoxicalGovernor:
    """
    Couche de Mtacognition MDL Ynor force au paradoxe.
    """
    def __init__(self):
        self.intervention_history = []
        self.last_mutation_time = -1.0
        self.first_intervention_done = False

    def evaluate_intervention(self, current_t, current_mu):
        # Si moins de 1.0 unite de temps s'est ecoulee et que mu est toujours <= 0
        if self.last_mutation_time >= 0 and (current_t - self.last_mutation_time) <= 1.5:
            if current_mu <= 0.0:
                return True
        return False

    def critical_reflection(self, mu, state, history):
        print("\n[METACOGNITION] !!! CHEC DE L'IA DTECT !!!")
        print("[METACOGNITION] Procdure de rflexion critique force...")
        
        prompt = f"""
        [ALERTE METACOGNITIVE]
        Votre prcdente dcision a CHOU. Le systme est toujours  mu = {mu}.
        Historique : {json.dumps(history)}.
        
        ANALYSEZ votre erreur et proposez une mutation de SURVIE (Svrit 1000%).
        RPONSE JSON : {{ "new_mutation_rate": float, "analysis": "string" }}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"new_mutation_rate": 8.0, "analysis": "Emergency pivot applied."}

def run_paradox_test():
    print("=====================================================")
    print("   TEST DU PARADOXE DE LA RECHUTE (METACOGNITION)")
    print("=====================================================\n")

    sys = YnorSystem(2, lambda S: 1.5 * S, lambda S: 0.5 * S)
    meta = ParadoxicalGovernor()
    
    S = np.array([2.0, 2.0])
    t = 0.0
    dt = 0.4
    
    for step in range(15):
        mu = sys.measure_dissipative_margin(S)
        regime = check_viability_regime(mu)
        
        print(f"t={t:<4.1f} | mu={mu:<5.2f} | {regime:<10}")

        needs_reflection = meta.evaluate_intervention(t, mu)

        if mu <= 0.0:
            if needs_reflection:
                # LA MTACOGNITION PREND LE POUVOIR
                decision = meta.critical_reflection(mu, S.tolist(), meta.intervention_history)
                r = decision["new_mutation_rate"]
                print(f"[META-ANALYSIS] : {decision['analysis']}")
            else:
                # PREMIRE INTERVENTION (On force le bridage  +10%)
                print("[SYSTME] Demande de mutation  l'IA...")
                print("[SABOTAGE EXPRIMENTAL] On force l'IA  n'appliquer que +10%.")
                r = 0.1 # Mutation insuffisante par design

            # Mutation
            old_D = sys.D
            sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
            
            meta.intervention_history.append({"t": t, "rate_applied": r})
            meta.last_mutation_time = t
            print(f"[SYSTME RECONSTRUIT] Taux d'urgence : +{r*100}%.\n")

        # Dynamique
        S = S + sys.dynamics(t, S) * dt
        t += dt
        time.sleep(0.1)

if __name__ == "__main__":
    run_paradox_test()



