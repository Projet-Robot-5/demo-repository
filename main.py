import threading
import sys
import time
import tkinter as tk
import importlib.util

from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.simulation import Simulation
def mode_terminal():
    print("Mode terminal activé")
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    ctrl = Controleur(adaptateur)
    
    def run_ctrl():
        while True:
            ctrl.update()
            time.sleep(0.01)
    
    threading.Thread(target=run_ctrl, daemon=True).start()
    
    try:
        while True: 
            time.sleep(1)
    except KeyboardInterrupt:
        print("Arrêt du programme")

def mode_graphique():
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    ctrl = Controleur(adaptateur)
    
    def run_ctrl():
        while True:
            ctrl.update()
            time.sleep(0.01)
    
    # L'affichage doit être dans le thread principal
    threading.Thread(target=run_ctrl, daemon=True).start()
    
    root = tk.Tk()
    root.title("Simulation Robot")
    AffichageGraphique(root, adaptateur, ctrl)  # Passer adaptateur au lieu de simulation
    root.mainloop()

def main():
    if "--no-gui" in sys.argv:
        mode_terminal()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()