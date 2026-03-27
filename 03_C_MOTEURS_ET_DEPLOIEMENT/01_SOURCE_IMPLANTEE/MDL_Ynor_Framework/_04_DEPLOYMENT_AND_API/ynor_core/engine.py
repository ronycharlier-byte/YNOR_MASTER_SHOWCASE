"""
YNOR CORE ENGINE - INDUSTRIAL GRADE
-----------------------------------
Industrial Loop Runner with full metrics and callback support.
"""
import time
from typing import Callable, List

import numpy as np
from .metrics import get_token_count, measure_alpha, measure_beta, measure_kappa
from .state import YnorState
from .controller import YnorController


class YnorSystem:
    """Numerical mu evaluator used by the validation and experiment suites."""

    def __init__(self, dim: int, amplification_op: Callable, dissipation_op: Callable):
        self.dim = dim
        self.E = amplification_op
        self.D = dissipation_op

    def measure_dissipative_margin(self, state) -> float:
        vector = np.asarray(state, dtype=float)
        if vector.shape != (self.dim,):
            raise ValueError(f"Expected state shape {(self.dim,)}, got {vector.shape}")

        base_norm = float(np.linalg.norm(vector))
        amp_norm = float(np.linalg.norm(np.asarray(self.E(vector), dtype=float)))
        diss_norm = float(np.linalg.norm(np.asarray(self.D(vector), dtype=float)))

        if np.isclose(base_norm, 0.0):
            return float(diss_norm - amp_norm)

        alpha = diss_norm / base_norm
        beta = amp_norm / base_norm
        return float(alpha - beta)

class YnorEngine:
    def __init__(self, llm_callable: Callable, model_name: str = "gpt-4o", threshold: float = 0.0):
        self.llm = llm_callable
        self.model_name = model_name
        self.state = YnorState()
        self.controller = YnorController(threshold=threshold)

    def run(self, prompt: str, max_steps: int = 20, verbose: bool = True) -> List[str]:
        """
        Execute an adaptive LLM session under Ynor Governance.
        Returns the finalized outputs list.
        """
        outputs = []
        context = prompt
        context_tokens = get_token_count(prompt, model=self.model_name)
        
        if verbose:
            print(f"--- YNOR CORE ::: DEPLOYING INDUSTRIAL GUARD (SESSION: {self.state.session_id}) ---")
            print(f"--- MODEL: {self.model_name} ---")

        for step in range(max_steps):
            t_start = time.time()
            
            # Step 1: Request LLM for tokens (Injection)
            try:
                response = self.llm(context)
            except Exception as e:
                print(f"[!] YNOR ERROR: LLM CALL FAILED: {str(e)}")
                break
            
            # Step 2: Extract Physics from text (Dissipation measurement)
            d_alpha = measure_alpha(response)
            response_tokens = get_token_count(response, model=self.model_name)
            d_beta = measure_beta(response, model=self.model_name, token_count=response_tokens)
            d_kappa = measure_kappa(model=self.model_name, token_count=context_tokens)
            
            # Step 3: Update Universal State
            d_mu = (d_alpha - d_beta - d_kappa)
            self.state.update(d_alpha, d_beta, d_kappa, step_metadata={"step": step, "duration": time.time() - t_start})
            
            # Step 4: Decision (Governance)
            result = self.controller.decide(self.state, last_d_mu=d_mu)
            
            if verbose:
                print(f" [Step {step:02d}] mu = {self.state.mu:.4f} (D_mu={d_mu:+.4f}) | alpha={self.state.alpha_total:.2f} | beta={self.state.beta_total:.2f} | kappa={self.state.kappa_total:.2f} | --> {result['decision']}")

            outputs.append(response)
            context += "\n" + response
            context_tokens += response_tokens
            
            if result["decision"] == "STOP":
                if verbose:
                    print(f" [☠] YNOR TERMINATED: {result['reason']} (mu = {self.state.mu:.2f})")
                break
                
            if result["decision"] == "WARN":
                if verbose:
                    print(f" [!] DRIFT WARN: {result['reason']} (Applying adaptive pressure...)")

        return outputs
