import time
import tkinter as tk
import threading
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.environnement import Environnement

def mode_graphique():
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))
    controleur.environnement = Environnement(width=500, height=500)
    
    root = tk.Tk()
    root.title("Simulation Robot")
    
    affichage = AffichageGraphique(root, adaptateur, controleur)
    affichage.pack(fill=tk.BOTH, expand=True)
    
    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    mode_graphique()
