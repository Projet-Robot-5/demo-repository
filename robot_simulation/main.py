import sys
import time
import tkinter as tk
from .controleur import Controleur

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
    controleur = Controleur(mode="terminal")
    controleur.run(duration = 10) #lancer la simulation pendant 10 sec

    while True:
        if not controleur.simulation.update_all():
            choix = input("Voulez-vous recommencer ? (o/n) : ")
            if choix.lower() == 'o':
                controleur.simulation = Controleur()
            else:
                break
        time.sleep(0.1)
        
def mode_graphique():
    """Mode graphique avec Tkinter, et passe au mode terminal si on ferme la fenêtre."""
    root = tk.Tk()
    root.title("Simulation de Robot")
    controleur = Controleur(mode="graphique", master=root)

    def on_close():
        """Si on ferme la fenêtre, on passe en mode terminal."""
        print("\nFermeture de l'interface graphique. Passage en mode terminal...\n")
        root.destroy()
        mode_terminal()

    root.protocol("WM_DELETE_WINDOW", on_close)  # Capture la fermeture de la fenêtre
    controleur.run(duration=10) #lancer la simulation pendant 10 sec
    root.mainloop()

def main():
    """Choix du mode : terminal ou GUI"""
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
        mode_terminal()
    else:
        mode_graphique()
if __name__ == "__main__":
    main()

