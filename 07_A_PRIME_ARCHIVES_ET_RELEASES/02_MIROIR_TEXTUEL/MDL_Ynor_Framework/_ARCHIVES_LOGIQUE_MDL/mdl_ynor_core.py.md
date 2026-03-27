# MIROIR TEXTUEL - mdl_ynor_core.py

Source : MDL_Ynor_Framework\_ARCHIVES_LOGIQUE_MDL\mdl_ynor_core.py
Taille : 5013 octets
SHA256 : 8e17143fd89d887c57bc9df53d841a7fa5407d430a3381288263f31106d5d6ce

```text
﻿# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
from scipy.integrate import solve_ivp
import logging

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
        
        # Marges et éléments avancés
        self.mu_theoretical = None
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
        """
        Équation d'évolution d'état : S_dot = E(S) - D(S) + M(S, t) + w(t)
        
        Args:
            t (float): temps courant
            S (numpy.ndarray): vecteur d'état courant
            
        Returns:
            numpy.ndarray: dérivée de l'état (S_dot)
        """
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
        S_dot = self.dynamics(0, S)  # Sans tenir compte du temps exact
        energy_deriv = np.dot(S, S_dot)
        forcing = self.w(0)
        perturb_power = np.dot(S, forcing)
        S_norm_sq = np.sum(S**2)
        
        if S_norm_sq == 0:
            logging.warning("Indéfini au repos parfait")
            return 0.0
            
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

    def audit_compliance(self, S):
        J_E = self.jacobian_E(S)
        J_D = self.jacobian_D(S)
        compliance_metric = np.linalg.norm(J_E - J_D)
        return compliance_metric

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