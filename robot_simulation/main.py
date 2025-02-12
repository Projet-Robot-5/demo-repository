import sys
import time
import tkinter as tk 
from affichage_graphique import AffichageGraphique
from simulation import Simulation

# Vérifier si affichage_graphique.py existe
try:
    from affichage_graphique import AffichageGraphique
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def main():
    """Initialiser et démarrer la simulation."""

    # Mode terminal si --no-gui est passé en argument ou si GUI non disponible
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
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
        return

        # Mode GUI
    racine = tk.Tk()
    racine.title("Simulation de Robot")
    simulation = AffichageGraphique(racine)
    racine.mainloop()


if __name__ == "__main__":
    main()