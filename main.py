import threading
import sys
import time
import tkinter as tk
import importlib.util

from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieCarre
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.simulation import Simulation
def mode_terminal():
    print("Mode terminal activé")
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    
    # Configuration de la stratégie
    controleur.set_strategie(StrategieCarre(adaptateur))
    
    try:
        while True:
            controleur.update()
            x, y = adaptateur.get_position()
            print(f"Position actuelle: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")

def mode_graphique():
    # Initialisation des composants
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    
    # Configuration de la stratégie
    controleur.set_strategie(StrategieCarre(adaptateur))
    
    # Thread pour le contrôleur
    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()
    
    # Interface graphique dans le thread principal
    root = tk.Tk()
    root.title("Simulation Robot")
    
    # Configuration de l'affichage
    affichage = AffichageGraphique(root, adaptateur, controleur)
    root.protocol("WM_DELETE_WINDOW", lambda: [
        setattr(controleur, 'running', False),
        ctrl_thread.join(timeout=0.1),
        root.destroy()
    ])
    
    root.mainloop()

def main():
    if "--no-gui" in sys.argv:
        mode_terminal()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()