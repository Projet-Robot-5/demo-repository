import sys
import time
import tkinter as tk
import importlib.util

# Import des modules réorganisés
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.modele.robot import Robot
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.simulateur.simulation import Simulation

# Vérifier si affichage_graphique.py existe
affichage_graphique_spec = importlib.util.find_spec("robot_simulation.affichage.affichage_graphique")
GUI_AVAILABLE = affichage_graphique_spec is not None


def mode_terminal():
    """Mode terminal sans interface graphique."""
    print("Mode terminal activé (sans interface graphique).")
    simulation = Simulation()

    # Créer un robot pour le mode terminal
    robot = Robot(x=100, y=100, vitesse=5)  # Exemple de robot avec position et vitesse initiales
    simulation.robot = robot
    controleur = Controleur(simulation, mode="terminal")
    
    controleur.run(duration=10)  # Lance la simulation pendant 10 sec

    while True:
        if not simulation.update_all():
            choix = input("Voulez-vous recommencer ? (o/n) : ")
            if choix.lower() == 'o':
                controleur.simulation = Simulation()
            else:
                break
        time.sleep(0.1)


def mode_graphique():
    """Mode graphique avec Tkinter, et passe au mode terminal si on ferme la fenêtre."""
    root = tk.Tk()
    root.title("Simulation de Robot")

    # Initialisation de la simulation et du robot
    simulation = Simulation()
    robot = Robot(x=250, y=250)
    simulation.robot = robot

    # Création du contrôleur et de l'affichage
    controleur = Controleur(simulation, mode="graphique", master=root)
    affichage = AffichageGraphique(root, simulation)

    def on_close():
        """Si on ferme la fenêtre, on passe en mode terminal."""
        print("\nFermeture de l'interface graphique. Passage en mode terminal...\n")
        root.destroy()
        mode_terminal()  # Passer au mode terminal

    # Définir le comportement lors de la fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", on_close)

    # Lancer la simulation pendant 10 sec
    controleur.run(duration=10)

    # Démarre la boucle principale de Tkinter
    root.mainloop()


def main():
    """Choix du mode : terminal ou GUI"""
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
        mode_terminal()
    else:
        mode_graphique()


if __name__ == "__main__":
    main()
