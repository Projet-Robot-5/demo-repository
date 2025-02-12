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
def mode_graphique():
    """Mode graphique avec Tkinter, et passe au mode terminal si on ferme la fenêtre."""
    root = tk.Tk()
    root.title("Simulation de Robot")
    simulation = AffichageGraphique(root)

    def on_close():
        """Si on ferme la fenêtre, on passe en mode terminal."""
        print("\nFermeture de l'interface graphique. Passage en mode terminal...\n")
        root.destroy()
        mode_terminal()

    root.protocol("WM_DELETE_WINDOW", on_close)  # Capture la fermeture de la fenêtre
    root.mainloop()
