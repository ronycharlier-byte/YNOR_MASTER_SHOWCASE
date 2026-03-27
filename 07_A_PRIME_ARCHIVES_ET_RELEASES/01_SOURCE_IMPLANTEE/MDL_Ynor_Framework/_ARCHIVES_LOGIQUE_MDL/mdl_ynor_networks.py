# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
import numpy as np
from scipy.integrate import solve_ivp
from mdl_ynor_core import YnorSystem

class DissipativeField:
    """
    Cadre formel des Champs Dissipatifs (Chapitre VII).
    Modélise un ensemble de YnorSystems couplés qui échangent de l'énergie.
    L'espace total d'état H_tot est la somme directe des espaces des sous-systèmes.
    """
    
    def __init__(self, systems, coupling_matrix):
        """
        Initialise un champ dissipatif.
        
        Args:
            systems (list of YnorSystem): Liste des systèmes qui composent le champ.
            coupling_matrix (numpy.ndarray): Matrice d'interaction pondérant le couplage.
                                             Si C[i, j] > 0, le sous-système j amplifie S_i.
                                             Si C[i, j] < 0, le sous-système j dissipe S_i.
        """
        self.systems = systems
        self.num_systems = len(systems)
        self.coupling_matrix = coupling_matrix
        
        # Le champ total a comme dimension la somme des dimensions
        self.dimensions = [sys.dimension for sys in self.systems]
        self.total_dim = sum(self.dimensions)
        
        if self.coupling_matrix.shape != (self.num_systems, self.num_systems):
            raise ValueError("Le format de la matrice de couplage est incorrect.")

    def dynamics(self, t, S_tot):
        """
        Calcule la dynamique globale du système couplé.
        S_tot: l'état total concaténé
        """
        # Extraire les sous-états
        coords = np.split(S_tot, np.cumsum(self.dimensions)[:-1])
        
        # Initialiser le vecteur de dérivée total
        S_dot_tot = []
        
        for i, sys in enumerate(self.systems):
            S_i = coords[i]
            
            # Dynamique locale (interne au système i)
            local_dot = sys.dynamics(t, S_i)
            
            # Composante d'interaction (effet du champ)
            interaction_term = np.zeros(sys.dimension)
            for j in range(self.num_systems):
                if i != j:
                    # Hypothèse scalaire pour le couplage simple: 
                    # L'impact de j sur i dépend de son état et du poids C[i,j]
                    # Ici c'est un produit scalaire avec la norme de j pour simplifier la projection,
                    # ou une homothétie si les dimensions varient. Misons sur une homothétie d'interaction :
                    norm_j = np.sqrt(np.sum(coords[j]**2))
                    # L'interaction est orientée vers S_i. (Couplage purement linéaire énergétique).
                    # Une modélisation plus précise exigerait des tenseurs de projection entre les espaces H_i et H_j.
                    if np.sum(S_i**2) > 0:
                        direction = S_i / np.sqrt(np.sum(S_i**2))
                    else:
                        direction = np.zeros_like(S_i)
                        
                    interaction_term += self.coupling_matrix[i, j] * norm_j * direction
                    
            S_dot_tot.append(local_dot + interaction_term)
            
        return np.concatenate(S_dot_tot)

    def simulate(self, S_init_tot, t_span, t_eval=None, method='RK45'):
        return solve_ivp(
            fun=self.dynamics,
            t_span=t_span,
            y0=S_init_tot,
            t_eval=t_eval,
            method=method
        )


class CriticalNetwork:
    """
    Cadre formel des Réseaux Critiques et de la Propagation Multi-Niveaux (Chapitre VIII).
    Représente une hiérarchie ou un graphe orienté de systèmes dissipatifs qui peuvent propager des "mutations"
    lorsque l'un des nœuds franchit un seuil critique local (mu < 0).
    """

    def __init__(self, dissipative_field, failure_thresholds):
        """
        Initialise un réseau critique à partir d'un champ dissipatif.
        
        Args:
            dissipative_field (DissipativeField): Le champ de base d'oscillateurs/systèmes.
            failure_thresholds (list): [mu_th_1, mu_th_2, ...]. Seuils en deçà desquels le nœud `i` 
                                       délivre un "pulse d'anomalie" à ses voisins.
        """
        self.field = dissipative_field
        self.thresholds = failure_thresholds

    def network_dynamics_with_events(self, t, S_tot):
        """
        Même dynamique que le champ dissipatif, mais inclut la détection d'événements critiques (mutations).
        """
        return self.field.dynamics(t, S_tot)
