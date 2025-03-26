import threading
import sys
import time
import tkinter as tk
import importlib.util

from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.modele.simulation import Simulation
# Vérifie dynamiquement si le module graphique est disponible
affichage_graphique_spec = importlib.util.find_spec("robot_simulation.affichage.affichage_graphique")
GUI_AVAILABLE = affichage_graphique_spec is not None

def run_simulation(simulation):
    while True:
        simulation.update_modele()
        time.sleep(0.01)

def run_controleur(controleur):
    while True:
        controleur.update()
        time.sleep(0.01)

def run_affichage(simulation):
    root = tk.Tk()
    root.title("Simulation de Robot")
    gui = AffichageGraphique(root, simulation)
    root.mainloop()

def mode_terminal():
    print("Mode terminal activé (sans interface graphique).")
    while True:
        simulation = Simulation()
        controleur = Controleur(simulation.robot, mode="terminal")

        controleur.run(duration=10)

        if not simulation.updateModele():
            choix = input("CRASH ! Le robot a percuté un obstacle.\nVoulez-vous recommencer ? (o/n) : ").strip().lower()
            if choix != 'o':
                break

def mode_graphique():
    simulation = Simulation()
    controleur = Controleur(simulation.robot, mode="graphique")

    threading.Thread(target=run_simulation, args=(simulation,), daemon=True).start()
    threading.Thread(target=run_controleur, args=(controleur,), daemon=True).start()
    threading.Thread(target=run_affichage, args=(simulation,), daemon=True).start()

    while True:
        time.sleep(1)

def main():
    if "--no-gui" in sys.argv or not GUI_AVAILABLE:
        mode_terminal()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()
