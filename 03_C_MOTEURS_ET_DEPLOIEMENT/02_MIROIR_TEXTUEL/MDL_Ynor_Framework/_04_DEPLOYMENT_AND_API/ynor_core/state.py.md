# MIROIR TEXTUEL - state.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\ynor_core\state.py
Taille : 1804 octets
SHA256 : 0f67bdc5b38dba06a51bfd10ffeffa4c603b26c01e8643df9afc582c24fa2857

```text
"""
YNOR CORE STATE - INDUSTRIAL GRADE
----------------------------------
Persistent and analytical state tracking of Mu (μ).
"""
import uuid
from typing import List, Dict
import time

class YnorState:
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.alpha_total = 0.0
        self.beta_total = 0.0
        self.kappa_total = 0.0
        self.history: List[Dict] = []
        self.start_time = time.time()

    def update(self, d_alpha: float, d_beta: float, d_kappa: float, step_metadata: dict = None):
        """Update metrics and record history for dashboard plotting"""
        self.alpha_total += d_alpha
        self.beta_total += d_beta
        self.kappa_total += d_kappa
        
        record = {
            "timestamp": time.time() - self.start_time,
            "d_alpha": d_alpha,
            "d_beta": d_beta,
            "d_kappa": d_kappa,
            "mu": self.mu,
            "alpha": self.alpha_total,
            "beta": self.beta_total,
            "kappa": self.kappa_total
        }
        if step_metadata:
            record.update(step_metadata)
            
        self.history.append(record)

    @property
    def mu(self) -> float:
        """Central Viability Invariant (μ = α - β - κ)"""
        return self.alpha_total - self.beta_total - self.kappa_total

    def get_summary(self) -> dict:
        """Return audit-ready data for industrial reporting"""
        return {
            "session_id": self.session_id,
            "duration": time.time() - self.start_time,
            "final_mu": self.mu,
            "total_alpha": self.alpha_total,
            "total_beta": self.beta_total,
            "total_kappa": self.kappa_total,
            "step_count": len(self.history)
        }

```