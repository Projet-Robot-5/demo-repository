import tkinter as tk
from affichage_graphique import AffichageGraphique
from simulation import Simulation

class Controleur:
    """Gère la simulation en mode graphique et en mode terminal."""
    
    def __init__(self):
        """Initialise le contrôleur avec une instance de simulation."""
        self.simulation = Simulation()
