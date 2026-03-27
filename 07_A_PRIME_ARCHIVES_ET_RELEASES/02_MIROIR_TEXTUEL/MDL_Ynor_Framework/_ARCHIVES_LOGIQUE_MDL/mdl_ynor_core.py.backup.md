# MIROIR TEXTUEL - mdl_ynor_core.py.backup

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\mdl_ynor_core.py.backup
Taille : 4334 octets
SHA256 : ad7553f3bb4f9660c1fe1c4db8ec01065e0a8f04a4574134d6133dd902de0697

```text
import numpy as np
from scipy.integrate import solve_ivp
import warnings

class YnorSystem:
    """
    Cadre formel de base du noyau MDL Ynor (Chapitre I).
    Représente un système dynamique dissipatif défini dans un espace de Hilbert réel.
    """

    def __init__(self, dimension, amplification_op, dissipation_op,
                 memory_op=None, forcing_op=None):
        """
        Initialise un système MDL Ynor minimal.
        
        Args:
            dimension (int): Dimension de l'espace d'état H.
            amplification_op (callable): E(S), opérateur d'amplification (retourne un vecteur de même dimension que S).
            dissipation_op (callable): D(S), opérateur de dissipation (retourne un vecteur de même dimension que S).
            memory_op (callable, optional): M(S, t, history), opérateur de mémoire/inertie.
            forcing_op (callable, optional): w(t), forçage externe ou perturbation adimissible.
        """
        self.dimension = dimension
        self.E = amplification_op
        self.D = dissipation_op
        
        # Par défaut, pas de mémoire
        self.M = memory_op if memory_op else lambda S, t: np.zeros(self.dimension)
        # Par défaut, pas de forçage
        self.w = forcing_op if forcing_op else lambda t: np.zeros(self.dimension)
        
        # Marge dissipative effective théorique calculable à posteriori
        self.mu_theoretical = None 

    def dynamics(self, t, S):
        """
        Équation d'évolution d'état : S_dot = E(S) - D(S) + M(S_t) + w(t)
        
        Args:
            t (float): temps courant
            S (numpy.ndarray): vecteur d'état courant
            
        Returns:
            numpy.ndarray: dérivée de l'état (S_dot)
        """
        # Pour simplifier l'historique dans cette première itération (scipy solve_ivp n'a pas 
        # directement accès à l'historique complet sans solveur DDE dédié),
        # nous appelons M avec l'état courant. Dans des impl. avancées, la "mémoire retardée"
        # demandera un `scipy.integrate.ode` avec intégrale arrière.
        S_dot = self.E(S) - self.D(S) + self.M(S, t) + self.w(t)
        return S_dot

    def energy(self, S):
        """
        Fonctionnelle d'énergie minimale (E_0(S) = 1/2 * |S|^2)
        """
        return 0.5 * np.sum(S**2)

    def measure_dissipative_margin(self, S):
        """
        Estime localement la marge dissipative "mu = alpha - beta - kappa"
        en évaluant le bilan instantané de la variation d'énergie.
        
        Si d(1/2|S|^2)/dt <= -mu * |S|^2 + <S,w>, on peut isoler une estimation
        dynamique de mu. Un mu > 0 signe une stabilité (régime viable).
        """
        S_dot = self. dynamics(0, S) # Sans tenir compte du temps exact
        # <S, \dot{S}>
        energy_deriv = np.dot(S, S_dot)
        
        # On calcule <S, w> (perturbation)
        forcing = self.w(0)
        perturb_power = np.dot(S, forcing)
        
        S_norm_sq = np.sum(S**2)
        
        if S_norm_sq == 0:
            return 0.0 # Indéfini au repos parfait
            
        # mu = ( <S,w> - dE/dt ) / |S|^2
        mu_estimated = (perturb_power - energy_deriv) / S_norm_sq
        return mu_estimated

    def simulate(self, S_init, t_span, t_eval=None, method='RK45'):
        """
        Simule la trajectoire du système sur l'intervalle donné.
        
        Args:
            S_init (numpy.ndarray): état initial de dimension `dimension`.
            t_span (tuple): (t_start, t_end).
            t_eval (numpy.ndarray, optional): points de temps où évaluer la solution.
            
        Returns:
            scipy.integrate._ivp.ivp.OdeResult: résultat de la simulation.
        """
        if len(S_init) != self.dimension:
            raise ValueError(f"S_init doit être de dimension {self.dimension}")
            
        res = solve_ivp(
            fun=self.dynamics,
            t_span=t_span,
            y0=S_init,
            t_eval=t_eval,
            method=method
        )
        return res

def check_viability_regime(mu):
    """
    Identifie le régime de viabilité du système (Théorème 1).
    """
    if mu > 0.01:
        return "STABLE"
    elif abs(mu) <= 0.01:
        return "CRITICAL"
    else:
        return "INSTABLE"

```