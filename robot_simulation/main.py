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
