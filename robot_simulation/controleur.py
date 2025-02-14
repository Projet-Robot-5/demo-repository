import tkinter as tk
from affichage_graphique import AffichageGraphique
from simulation import Simulation

class Controleur:
    """Gère la simulation en mode graphique et en mode terminal."""
    
    def __init__(self):
        """Initialise le contrôleur avec une instance de simulation."""
        self.simulation = Simulation()

    def lancer_simulation_sans_AG(self):
        """Exécuter la simulation en mode terminal (sans interface graphique)."""
        self.simulation.run()

    def lancer_simulation_avec_AG(self):
        """Lancer l'affichage graphique de la simulation."""
        racine = tk.Tk()
        racine.title("Simulation de Robot")
        affichage = AffichageGraphique(racine, self.simulation)  # On passe la simulation existante
        racine.mainloop()
