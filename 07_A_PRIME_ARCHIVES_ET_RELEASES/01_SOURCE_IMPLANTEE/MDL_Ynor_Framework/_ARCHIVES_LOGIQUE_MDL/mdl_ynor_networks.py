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
    Modlise un ensemble de YnorSystems coupls qui changent de l'nergie.
    L'espace total d'tat H_tot est la somme directe des espaces des sous-systmes.
    """
    
    def __init__(self, systems, coupling_matrix):
        """
        Initialise un champ dissipatif.
        
        Args:
            systems (list of YnorSystem): Liste des systmes qui composent le champ.
            coupling_matrix (numpy.ndarray): Matrice d'interaction pondrant le couplage.
                                             Si C[i, j] > 0, le sous-systme j amplifie S_i.
                                             Si C[i, j] < 0, le sous-systme j dissipe S_i.
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
        Calcule la dynamique globale du systme coupl.
        S_tot: l'tat total concatn
        """
        # Extraire les sous-tats
        coords = np.split(S_tot, np.cumsum(self.dimensions)[:-1])
        
        # Initialiser le vecteur de drive total
        S_dot_tot = []
        
        for i, sys in enumerate(self.systems):
            S_i = coords[i]
            
            # Dynamique locale (interne au systme i)
            local_dot = sys.dynamics(t, S_i)
            
            # Composante d'interaction (effet du champ)
            interaction_term = np.zeros(sys.dimension)
            for j in range(self.num_systems):
                if i != j:
                    # Hypothse scalaire pour le couplage simple: 
                    # L'impact de j sur i dpend de son tat et du poids C[i,j]
                    # Ici c'est un produit scalaire avec la norme de j pour simplifier la projection,
                    # ou une homothtie si les dimensions varient. Misons sur une homothtie d'interaction :
                    norm_j = np.sqrt(np.sum(coords[j]**2))
                    # L'interaction est oriente vers S_i. (Couplage purement linaire nergtique).
                    # Une modlisation plus prcise exigerait des tenseurs de projection entre les espaces H_i et H_j.
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
    Cadre formel des Rseaux Critiques et de la Propagation Multi-Niveaux (Chapitre VIII).
    Reprsente une hirarchie ou un graphe orient de systmes dissipatifs qui peuvent propager des "mutations"
    lorsque l'un des nuds franchit un seuil critique local (mu < 0).
    """

    def __init__(self, dissipative_field, failure_thresholds):
        """
        Initialise un rseau critique  partir d'un champ dissipatif.
        
        Args:
            dissipative_field (DissipativeField): Le champ de base d'oscillateurs/systmes.
            failure_thresholds (list): [mu_th_1, mu_th_2, ...]. Seuils en de desquels le nud `i` 
                                       dlivre un "pulse d'anomalie"  ses voisins.
        """
        self.field = dissipative_field
        self.thresholds = failure_thresholds

    def network_dynamics_with_events(self, t, S_tot):
        """
        Mme dynamique que le champ dissipatif, mais inclut la dtection d'vnements critiques (mutations).
        """
        return self.field.dynamics(t, S_tot)



