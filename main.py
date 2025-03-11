import sys
import time
import tkinter as tk
import importlib.util

# Import des modules réorganisés
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.modele.robot import Robot
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.modele.simulation import Simulation

# Vérifier si affichage_graphique.py existe
affichage_graphique_spec = importlib.util.find_spec("robot_simulation.affichage.affichage_graphique")
GUI_AVAILABLE = affichage_graphique_spec is not None


def mode_terminal():
    """Mode terminal sans interface graphique."""
    print("Mode terminal activé (sans interface graphique).")

    while True:
        simulation = Simulation()
        robot = Robot(x=100, y=100, vitesse_gauche=5, vitesse_droite=5)
        simulation.robot = robot
        controleur = Controleur(robot, mode="terminal")

        controleur.run(duration=10)  # Lance la simulation pendant 10 sec

        while True:
            if not simulation.updateModele():
                choix = input("CRASH ! Le robot a percuté un obstacle.\nVoulez-vous recommencer ? (o/n) : ").strip().lower()
                if choix == 'o':
                    break  # On sort de cette boucle et recommence la simulation
                else:
                    return  # On quitte complètement le mode terminal


def mode_graphique():
    """Mode graphique avec Tkinter, et passe au mode terminal si on ferme la fenêtre."""
    root = tk.Tk()
    root.title("Simulation de Robot")

   # Initialisation du robot
    robot = Robot(x=250, y=250)  # Créer le robot directement

    # Création du contrôleur et de l'affichage
    controleur = Controleur(robot, mode="graphique", master=root)
    affichage = AffichageGraphique(root, robot)

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