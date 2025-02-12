import sys
import time
import tkinter as tk
from .affichage_graphique import AffichageGraphique
from .simulation import Simulation

# Vérifier si affichage_graphique.py existe
try:
    from .affichage_graphique import AffichageGraphique
    GUI_AVAILABLE = True
except ImportError as e:
    print("Erreur import GUI :", e)
    GUI_AVAILABLE = False
def mode_terminal():
    """Mode terminal sans interface graphique."""
    print("Mode terminal activé (sans interface graphique).")
    simulation = Simulation()

    while True:
        if not simulation.update_all():
            choix = input("Voulez-vous recommencer ? (o/n) : ")
            if choix.lower() == 'o':
                simulation = Simulation()  # Réinitialiser la simulation
            else:
                break
        time.sleep(0.1)
