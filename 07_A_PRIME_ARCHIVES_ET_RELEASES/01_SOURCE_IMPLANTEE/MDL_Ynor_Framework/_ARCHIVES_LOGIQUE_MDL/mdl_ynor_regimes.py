# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
from mdl_ynor_core import YnorSystem
import numpy as np

class PostCriticalReconstructor:
    """
    Implémente les algorithmes de la reconstruction post-critique (Chapitre VI).
    Un système dont la marge dissipative mu devient négative peut "muter" 
    ses opérateurs internes (E ou D) pour restaurer la viabilité.
    """

    def __init__(self, system, mutation_rate=0.1):
        """
        Args:
            system (YnorSystem): Le système à surveiller et réparer.
            mutation_rate (float): Le taux de variation de l'opérateur de dissipation 
                                   lors d'une restructuration.
        """
        self.system = system
        self.r = mutation_rate
        
        # Sauvegarde des opérateurs d'origine pour trace
        self.original_D = system.D

    def evaluate_and_reconstruct(self, current_S):
        """
        Évalue l'état actuel. Si l'état est instable (mu < 0), 
        applique une mutation structurelle d'urgence pour augmenter la dissipation.
        
        Returns:
            bool: True si une mutation a eu lieu, False sinon.
        """
        mu = self.system.measure_dissipative_margin(current_S)
        
        if mu < 0:
            # L'amplification domine. Il faut augmenter la dissipation.
            # Mutation de l'opérateur scalaire de dissipation.
            # On crée un nouveau closure qui "booste" proportionnellement l'ancien D.
            old_D = self.system.D
            
            # Formule d'adaptation canonique : D_new(S) = (1 + r) * D_old(S)
            new_D = lambda S, D_func=old_D: (1.0 + self.r) * D_func(S)
            
            self.system.D = new_D
            return True
            
        return False
        
    def reset(self):
        """ Restaure le système dans sa configuration structurelle d'origine. """
        self.system.D = self.original_D
