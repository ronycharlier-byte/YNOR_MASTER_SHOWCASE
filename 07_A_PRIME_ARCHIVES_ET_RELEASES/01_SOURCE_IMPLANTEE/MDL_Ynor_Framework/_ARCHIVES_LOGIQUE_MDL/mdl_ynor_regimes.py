# =============================================================================
# COPYRIGHT (c) 2026 CHARLIER RONY - TOUS DROITS RESERVES
# Architecte Supreme & Fondateur - Architecture MDL Ynor
# Toute reproduction ou utilisation sans autorisation est strictement interdite.
# =============================================================================
from mdl_ynor_core import YnorSystem
import numpy as np

class PostCriticalReconstructor:
    """
    Implmente les algorithmes de la reconstruction post-critique (Chapitre VI).
    Un systme dont la marge dissipative mu devient ngative peut "muter" 
    ses oprateurs internes (E ou D) pour restaurer la viabilit.
    """

    def __init__(self, system, mutation_rate=0.1):
        """
        Args:
            system (YnorSystem): Le systme  surveiller et rparer.
            mutation_rate (float): Le taux de variation de l'oprateur de dissipation 
                                   lors d'une restructuration.
        """
        self.system = system
        self.r = mutation_rate
        
        # Sauvegarde des oprateurs d'origine pour trace
        self.original_D = system.D

    def evaluate_and_reconstruct(self, current_S):
        """
        value l'tat actuel. Si l'tat est instable (mu < 0), 
        applique une mutation structurelle d'urgence pour augmenter la dissipation.
        
        Returns:
            bool: True si une mutation a eu lieu, False sinon.
        """
        mu = self.system.measure_dissipative_margin(current_S)
        
        if mu < 0:
            # L'amplification domine. Il faut augmenter la dissipation.
            # Mutation de l'oprateur scalaire de dissipation.
            # On cre un nouveau closure qui "booste" proportionnellement l'ancien D.
            old_D = self.system.D
            
            # Formule d'adaptation canonique : D_new(S) = (1 + r) * D_old(S)
            new_D = lambda S, D_func=old_D: (1.0 + self.r) * D_func(S)
            
            self.system.D = new_D
            return True
            
        return False
        
    def reset(self):
        """ Restaure le systme dans sa configuration structurelle d'origine. """
        self.system.D = self.original_D



