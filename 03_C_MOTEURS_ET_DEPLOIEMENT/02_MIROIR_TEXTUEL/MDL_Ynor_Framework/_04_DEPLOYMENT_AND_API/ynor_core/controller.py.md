# MIROIR TEXTUEL - controller.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\ynor_core\controller.py
Taille : 1395 octets
SHA256 : 427db8998625577d8ac1a3bfe9fb1566add591b5f49938727795418a05738d2a

```text
"""
YNOR CORE CONTROLLER - INDUSTRIAL GRADE
---------------------------------------
Dynamic decision and governance policies for LLM execution flow.
"""

class YnorController:
    def __init__(self, mode: str = "strict", threshold: float = 0.0):
        """
        Policy Modes:
        - strict: Stop as soon as mu <= threshold
        - conservative: Warn when mu < threshold + offset, stop later
        - balanced: Dynamically adjust temperature before stopping
        """
        self.mode = mode
        self.threshold = threshold

    def decide(self, state, last_d_mu: float = 0.0) -> dict:
        """Central Governance Logic"""
        mu = state.mu
        
        # STOP RULE 1: The Zero-Boundary (Surface Critique Σ)
        if mu <= self.threshold:
            return {
                "decision": "STOP",
                "reason": "VIABILITY_EXHAUSTED",
                "mu": mu
            }
            
        # STOP RULE 2: Persistant Drift (Entropy runaway)
        # Even if Mu is positive, a sharp collapse in D_mu signals trouble
        if last_d_mu < -0.5:
            return {
                "decision": "WARN",
                "reason": "CRITICAL_DRIFT",
                "mu": mu,
                "adjustment": {"temperature": 0.2, "max_tokens": 100}
            }
            
        return {
            "decision": "CONTINUE",
            "mu": mu
        }

```