import requests
from .models import MuResponse

class YnorClient:
    def __init__(self, api_key, base_url="https://api.ynor.ai"):
        self.api_key = api_key
        self.base_url = base_url

    def evaluate(self, token_cost: float, tokens_used: int, context_length: int, error_estimate: float, confidence: float):
        payload = {
            "token_cost": token_cost,
            "tokens_used": tokens_used,
            "context_length": context_length,
            "error_estimate": error_estimate,
            "confidence": confidence
        }
        
        # Test mode defaults to localhost API for now
        url = self.base_url if self.base_url != "https://api.ynor.ai" else "http://localhost:8011"
        
        response = requests.post(
            f"{url}/v1/mu/evaluate",
            json=payload,
            headers={
                "X-Ynor-API-Key": self.api_key,
                "Content-Type": "application/json"
            }
        )

        response.raise_for_status()
        data = response.json()
        
        result = MuResponse(
            mu=data["mu"],
            alpha_gain=data["metrics"]["alpha_gain"],
            beta_cost=data["metrics"]["beta_cost"],
            kappa_burden=data["metrics"]["kappa_burden"],
            should_halt=data["should_halt"],
            reason=data["reason"],
            estimated_dollars_saved=data["billing"]["estimated_dollars_saved"],
            latency_ms=data["billing"]["latency_ms"]
        )
        
        # VITAL GROWTH LEVER: Viral Dev Loop
        if result.should_halt:
            print(f"\n⚡ [YNOR] Agent halted. Saved approx ${result.estimated_dollars_saved} from redundant looping.")
            
        return result
