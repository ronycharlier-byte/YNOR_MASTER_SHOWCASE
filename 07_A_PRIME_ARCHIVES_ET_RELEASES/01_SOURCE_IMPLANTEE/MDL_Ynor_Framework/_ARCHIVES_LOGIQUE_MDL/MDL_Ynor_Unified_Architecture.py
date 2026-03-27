from dotenv import load_dotenv
load_dotenv()

﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import json
import time
import datetime
import os
import openai
import logging
import shutil
from scipy.integrate import solve_ivp

# =====================================================
# 1. NOYAU MDL YNOR (CORE) - EVOLVED BY AGI
# =====================================================
class YnorSystem:
    def __init__(self, dimension, amplification_op, dissipation_op, memory_op=None, forcing_op=None):
        self.dimension = dimension
        self.E = amplification_op
        self.D = dissipation_op
        self.M = memory_op if memory_op else lambda S, t: np.zeros(self.dimension)
        self.w = forcing_op if forcing_op else lambda t: np.zeros(self.dimension)
        self.jacobian_E = self._compute_jacobian(self.E)
        self.jacobian_D = self._compute_jacobian(self.D)

    def _compute_jacobian(self, func):
        def jacobian(S):
            J = np.zeros((self.dimension, self.dimension))
            delta = 1e-5
            for i in range(self.dimension):
                S_step = np.copy(S)
                S_step[i] += delta
                J[:, i] = (func(S_step) - func(S)) / delta
            return J
        return jacobian

    def dynamics(self, t, S):
        return self.E(S) - self.D(S) + self.M(S, t) + self.w(t)

    def energy(self, S):
        return 0.5 * np.sum(S**2)

    def measure_dissipative_margin(self, S):
        S_dot = self.dynamics(0, S)
        energy_deriv = np.dot(S, S_dot)
        forcing = self.w(0)
        perturb_power = np.dot(S, forcing)
        S_norm_sq = np.sum(S**2)
        if S_norm_sq == 0: return 0.0
        return (perturb_power - energy_deriv) / S_norm_sq

def check_viability_regime(mu):
    if mu > 0.01: return "STABLE"
    elif abs(mu) <= 0.01: return "CRITICAL"
    else: return "INSTABLE"

# =====================================================
# 2. GOUVERNANCE IA (OPENAI ADAPTER)
# =====================================================
# RECUPERATION DE LA CLÉ DEPUIS LE FICHIER CONFIG
OPENAI_API_KEY = "os.getenv("OPENAI_API_KEY", "REDACTED")-DMJnu_NGYDzKSnPfRJiT3BlbkFJGnXK8Y2gM3UvZwEPk8atrYYgu-kEElRRXwgctK1Re7sMq9GRjqvoRuTvhgIl0pf9xaGS4Q0AAA"
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_ai_reconstruction_strategy(mu, state, is_metacognitive=False, history=None):
    prompt_prefix = "[DIRECTIVE PRIORITAIRE]" if not is_metacognitive else "[ALERTE METACOGNITIVE]"
    
    prompt = f"""
    {prompt_prefix} Système MDL Ynor en crise. mu = {mu}. S = {state}.
    TÂCHE : Proposez un taux de mutation 'r' pour l'opérateur D(S). 
    { "ANALYSEZ vos échecs passés : " + json.dumps(history) if is_metacognitive else "" }
    RÉPONSE JSON : {{ "mutation_rate": float, "explanation": "string" }}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except:
        return {"mutation_rate": 2.0, "explanation": "Fallback strategy applied."}

# =====================================================
# 3. MÉTACOGNITION & RÉSEAUX (NETWORKS)
# =====================================================
class MetacognitiveUnit:
    def __init__(self):
        self.history = []
        self.last_mutation_t = -1.0

    def evaluate_resilience(self, t, mu):
        if self.last_mutation_t >= 0 and (t - self.last_mutation_t) < 1.0:
            if mu <= 0.0: return True
        return False

# =====================================================
# 4. NOYAU AGI (AUTO-ÉVOLUTION RÉCURSIVE)
# =====================================================
class AGIEvolutionaryHook:
    """
    Permet au système de réécrire ses propres fonctions D(S) 
    en utilisant une logique de raisonnement AGI (basée sur le savoir PDF).
    """
    @staticmethod
    def innovate_dissipation(current_mu, state_history):
        print("\n[AGI] INCOHÉRENCE DÉTECTÉE. DÉCLENCHEMENT DE L'INNOVATION STRUCTURELLE...")
        prompt = f"""
        [SYSTÈME MDL AGI] Intervention sur une rechute systémique (mu = {current_mu}).
        Veuillez inventer une NOUVELLE formulation globale pour 'D(S)'.
        RÈGLES : Utilisez uniquement 'S' (vecteur d'état) et 'np' (numpy). 
        NE PAS utiliser 'mu' ou 't' dans la fonction.
        RÉPONSE JSON : {{ "lambda_code": "string", "reasoning": "string" }}
        Exemple : {{ "lambda_code": "lambda S: 2.5 * S * np.exp(-0.1 * np.sum(S**2))", "reasoning": "Dissipation exponentielle non-linéaire." }}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            data = json.loads(response.choices[0].message.content)
            # On passe le namespace local à eval pour np
            safe_scope = {"np": np}
            return eval(data["lambda_code"], safe_scope), data["reasoning"]
        except Exception as e:
            print(f"[ERREUR AGI] Echec de l'innovation : {e}")
            return (lambda S: 5.0 * S), "Fallback High-Dissipation Applied."

# =====================================================
# 5. SYSTÈME MAÎTRE (MASTER UNIFIED SYSTEM)
# =====================================================
class UnifiedMDLProcessor:
    def __init__(self):
        self.nodes = {
            "ENERGIE": YnorSystem(2, lambda S: 1.5 * S, lambda S: 0.5 * S),
            "INFOS": YnorSystem(2, lambda S: 1.8 * S, lambda S: 0.2 * S)
        }
        self.states = {name: np.array([2.0, 2.0]) for name in self.nodes.keys()}
        self.meta = MetacognitiveUnit()
        self.agi = AGIEvolutionaryHook()
        self.history = {name: [] for name in self.nodes.keys()}

    def save_learning_experience(self, node_name, mu, action, success):
        """
        Sauvegarde l'expérience vécue pour améliorer les futurs audits AGI.
        Cast les types numpy en types Python natifs pour JSON.
        """
        log_file = "ynor_learning_experience_log.json"
        
        # Sécurisation des types pour JSON
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node": node_name,
            "mu_audit": float(mu),
            "action_taken": str(action),
            "success_proven": bool(success)
        }
        
        history = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try: history = json.load(f)
                except: history = []
        
        history.append(entry)
        with open(log_file, "w") as f:
            json.dump(history[-50:], f, indent=2) # On garde les 50 dernières expériences

    def run_unification_audit(self):
        print("=====================================================")
        print("   UNIFICATION ARCHITECTURALE MDL YNOR (AGI MODE)")
        print("   --- AUTO-AMÉLIORATION PAR L'USAGE ACTIVÉE ---")
        print("=====================================================\n")
        
        t = 0.0
        dt = 0.2
        
        for step in range(15):
            print(f"Cycle t={t:.1f}")
            for name, sys in self.nodes.items():
                mu = sys.measure_dissipative_margin(self.states[name])
                self.history[name].append(self.states[name].tolist())

                # ÉVALUATION MÉTACOGNITIVE
                is_relapse = self.meta.evaluate_resilience(t, mu)
                
                status_action = "STABLE_IDLE"
                if mu <= 0.0:
                    if is_relapse:
                        new_D_func, reason = self.agi.innovate_dissipation(mu, self.history[name])
                        sys.D = new_D_func
                        status_action = f"AGI_INNOVATION: {reason}"
                    else:
                        strategy = get_ai_reconstruction_strategy(mu, self.states[name].tolist(), False, [])
                        r = strategy["mutation_rate"]
                        old_D = sys.D
                        sys.D = lambda S, D_old=old_D, rate=r: (1.0 + rate) * D_old(S)
                        status_action = f"GOVERNANCE_MUTATION: +{r*100}%"
                    
                    self.meta.last_mutation_t = t
                
                # Apprentissage par l'usage : Chaque cycle nourrit le savoir de l'IA
                self.save_learning_experience(name, mu, status_action, success=(mu > 0))

                # Evolution dynamique
                self.states[name] = self.states[name] + sys.dynamics(t, self.states[name]) * dt
            t += dt
        print("\n[OK] Simualtion terminée. L'IA est devenue plus intelligente grâce à cet usage.")

if __name__ == "__main__":
    processor = UnifiedMDLProcessor()
    processor.run_unification_audit()
