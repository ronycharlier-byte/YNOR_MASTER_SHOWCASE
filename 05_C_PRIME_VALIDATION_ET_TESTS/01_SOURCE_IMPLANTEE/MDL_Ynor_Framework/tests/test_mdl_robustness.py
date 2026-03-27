# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# MDL YNOR - STRESS TEST & ROBUSTNESS (pytest)
# =============================================================================
import pytest
import numpy as np
from _04_DEPLOYMENT_AND_API.ynor_core.engine import YnorSystem

def test_mu_calculation_valid_state():
    """Vérifier la marge mu pour un état simple."""
    dim = 2
    E = lambda S: 0.5 * S
    D = lambda S: 2.0 * S
    sys = YnorSystem(dim, E, D)
    S = np.array([10.0, 10.0])
    mu = sys.measure_dissipative_margin(S)
    assert mu == 1.5

def test_extreme_amplication():
    """Test de survie avec amplification massive (mu < 0)."""
    dim = 2
    E = lambda S: 5.0 * S  # Beta élevé
    D = lambda S: 1.0 * S  # Alpha faible
    sys = YnorSystem(dim, E, D)
    S = np.array([1.0, 1.0])
    mu = sys.measure_dissipative_margin(S)
    assert mu == -4.0  # Le système doit retourner une valeur négative cohérente

def test_zero_state_robustness():
    """Vérifier la stabilité face à un état nul (limite)."""
    dim = 2
    E = lambda S: 0.5 * S
    D = lambda S: 2.0 * S
    sys = YnorSystem(dim, E, D)
    S = np.zeros(2)
    # Dans certains cas de division par zéro, mu doit lever une alerte ou être géré.
    try:
        mu = sys.measure_dissipative_margin(S)
        assert isinstance(mu, (float, int))
    except ZeroDivisionError:
        pytest.fail("MDL Ynor ne doit pas échouer sur un état nul (Division par zéro non gérée).")

def test_non_linear_robustness():
    """Test avec opérateurs non linéaires complexes."""
    dim = 2
    E = lambda S: np.sin(S) * 0.5
    D = lambda S: np.exp(S) * 0.1
    sys = YnorSystem(dim, E, D)
    S = np.array([1.0, 1.0])
    mu = sys.measure_dissipative_margin(S)
    assert mu != 0  # Doit retourner une marge réelle calculée sur le jacobien local

def test_high_dimension_performance():
    """Vérifier la scalabilité sur 100 dimensions."""
    dim = 100
    E = lambda S: 0.8 * S
    D = lambda S: 1.2 * S
    sys = YnorSystem(dim, E, D)
    S = np.random.rand(dim)
    mu = sys.measure_dissipative_margin(S)
    assert np.isclose(mu, 0.4)
