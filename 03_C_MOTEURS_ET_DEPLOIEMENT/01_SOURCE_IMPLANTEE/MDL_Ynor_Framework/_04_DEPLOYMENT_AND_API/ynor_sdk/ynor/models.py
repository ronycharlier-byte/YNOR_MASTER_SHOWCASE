from dataclasses import dataclass

@dataclass
class MuResponse:
    mu: float
    alpha_gain: float
    beta_cost: float
    kappa_burden: float
    should_halt: bool
    reason: str
    estimated_dollars_saved: float
    latency_ms: float
