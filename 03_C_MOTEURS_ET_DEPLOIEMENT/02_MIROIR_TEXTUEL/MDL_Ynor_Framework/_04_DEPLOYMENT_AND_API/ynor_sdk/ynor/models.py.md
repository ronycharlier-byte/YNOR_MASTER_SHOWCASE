# MIROIR TEXTUEL - models.py

Source : MDL_Ynor_Framework\_04_DEPLOYMENT_AND_API\ynor_sdk\ynor\models.py
Taille : 240 octets
SHA256 : 03df64da0a32a2b7fad6076bb0f6ce72990c4e2ea1858b68bdd49afd86fc5488

```text
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

```