import threading
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

# Ajout des fonctions run_simulation, run_controleur et run_affichage qui seront exécutées en parallèle dans les threads.

def run_simulation(simulation):
    """Thread pour mettre à jour le modèle (robot + environnement)"""
    while True:
        simulation.update_modele()
        time.sleep(0.01)  # 10 ms


def run_controleur(controleur):
    """Thread pour mettre à jour le contrôleur (stratégie du robot)"""
    while True:
        controleur.update()
        time.sleep(0.01)


def run_affichage(simulation):
    """Thread pour lancer l'interface graphique"""
    root = tk.Tk()
    root.title("Simulation de Robot")
    gui = AffichageGraphique(root, simulation)
    root.mainloop()


def main():
    """Choix du mode : terminal ou GUI"""
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
        mode_terminal()  # Si le mode graphique n'est pas disponible ou si l'argument --no-gui est passé
    else:
        mode_graphique()  # Sinon, passe au mode graphique


def mode_terminal():
    """Mode terminal sans interface graphique."""
    print("Mode terminal activé (sans interface graphique).")
    while True:
        simulation = Simulation()
        robot = Robot(x=100, y=100, vitesse_gauche=5, vitesse_droite=5)
        simulation.robot = robot
        controleur = Controleur(robot, mode="terminal")
        
        controleur.run(duration=10)  # Lance la simulation pendant 10 sec
        
        # Logique d'interaction utilisateur en cas de collision
        while True:
            if not simulation.updateModele():
                choix = input("CRASH ! Le robot a percuté un obstacle.\nVoulez-vous recommencer ? (o/n) : ").strip().lower()
                if choix == 'o':
                    break
                else:
                    return  # Quitter complètement le mode terminal


def mode_graphique():
    """Mode graphique avec Tkinter."""
    root = tk.Tk()
    root.title("Simulation de Robot")

    # Initialisation du robot et du contrôleur
    robot = Robot(x=250, y=250)
    controleur = Controleur(robot, mode="graphique", master=root)
    
    # Lancer la simulation avec la méthode `run`
    controleur.run()  # Démarrer la simulation pendant 10 sec

    # Lancer la boucle principale de Tkinter
    root.mainloop()


if __name__ == "__main__":
    main()