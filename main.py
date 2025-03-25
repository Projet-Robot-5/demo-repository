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

# Vérifie dynamiquement si le module graphique est disponible
affichage_graphique_spec = importlib.util.find_spec("robot_simulation.affichage.affichage_graphique")
GUI_AVAILABLE = affichage_graphique_spec is not None

# --- THREADS DE TRAVAIL ---

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

# --- MODES D’EXÉCUTION ---

def mode_terminal():
    """Mode terminal sans interface graphique."""
    print("Mode terminal activé (sans interface graphique).")
    while True:
        simulation = Simulation()
        controleur = Controleur(simulation.robot, mode="terminal")
        controleur.run(duration=10)  # Simulation pendant 10 secondes

        if not simulation.updateModele():
            choix = input("CRASH ! Le robot a percuté un obstacle.\nVoulez-vous recommencer ? (o/n) : ").strip().lower()
            if choix != 'o':
                break  # Quitte le mode terminal

def mode_graphique():
    """Mode graphique avec threads pour chaque composant."""
    # Initialisation
    simulation = Simulation()
    robot = Robot(x=250, y=250)
    simulation.robot = robot
    controleur = Controleur(robot, mode="graphique", simulation=simulation)

    # Lancer les 3 threads en parallèle
    threading.Thread(target=run_simulation, args=(simulation,), daemon=True).start()
    threading.Thread(target=run_controleur, args=(controleur,), daemon=True).start()
    threading.Thread(target=run_affichage, args=(simulation,), daemon=True).start()

    # Garder le programme actif
    while True:
        time.sleep(1)

# --- POINT D’ENTRÉE PRINCIPAL ---

def main():
    """Choix du mode : terminal ou GUI"""
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
        mode_terminal()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()
