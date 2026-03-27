"""
YNOR CORE METRICS - INDUSTRIAL GRADE
------------------------------------
Precision measurement of:
- Alpha: Information Density / Semantic Value
- Beta: Token Cost / Vernacular Efficiency
- Kappa: Context Inertia / Memory Payload
"""
import re
from functools import lru_cache

try:
    import tiktoken
except ImportError:
    tiktoken = None

_STRUCTURE_PATTERN = re.compile(r"[.,;!?( )]")


@lru_cache(maxsize=16)
def _get_encoding(model: str):
    if not tiktoken:
        return None
    return tiktoken.encoding_for_model(model)

def get_token_count(text: str, model: str = "gpt-4o") -> int:
    """Accurate token count using tiktoken (OpenAI standard)"""
    if tiktoken:
        try:
            encoding = _get_encoding(model)
            return len(encoding.encode(text))
        except Exception:
            return int(len(text.split()) * 1.3)  # Fallback approximation
    return int(len(text.split()) * 1.3)  # General fallback

def measure_alpha(output: str) -> float:
    """
    Measure Alpha (Value):
    Calculated as a factor of information diversity and pattern discovery.
    High Alpha = High density of non-redundant, structured information.
    """
    words = output.lower().split()
    if not words:
        return 0.0
        
    unique_words = set(words)
    diversity_index = len(unique_words) / len(words)
    
    # Semantic depth proxy (punctuation/structure ratio)
    structure_density = (len(_STRUCTURE_PATTERN.findall(output)) + 1) / (len(words) + 1)
    
    # Industrial Scaling (Alpha > 1.0 is considered highly valuable)
    return diversity_index * structure_density * 5.0

def measure_beta(output: str, model: str = "gpt-4o", token_count: int | None = None) -> float:
    """
    Measure Beta (Cost):
    Directly proportional to the number of tokens used.
    """
    tokens = token_count if token_count is not None else get_token_count(output, model=model)
    # 0.01 per token as a standardized cost unit in Ynor Mu space
    return tokens * 0.01

def measure_kappa(
    context: str | None = None,
    model: str = "gpt-4o",
    token_count: int | None = None,
) -> float:
    """
    Measure Kappa (Memory Payload):
    The friction introduced by the total context window size.
    """
    context_tokens = token_count if token_count is not None else get_token_count(context or "", model=model)
    # Kappa increases exponentially with context size to model performance degradation
    return (context_tokens / 1000.0) ** 1.1
