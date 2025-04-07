import time
import tkinter as tk
import threading
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.controleur.strategie import StrategieBoucle
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.environnement import Environnement

def mode_graphique():
    robot = Robot(x=250, y=250)
    robot2 = Robot(x=350, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    adaptateur2 = AdaptateurRobotSimule(robot2)
    controleur2 = Controleur(adaptateur2)
 
    
    actions1 = [
        AvancerDroit(adaptateur, 800),StrategieBoucle(Tourner(adaptateur, 360),10)]
        
   
    controleur.set_strategie(StrategieSequencielle(actions1))
    #controleur.set_strategie(StrategieBoucle(actions2,10))
    controleur.environnement = Environnement(width=500, height=500)
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    controleur2.set_strategie(StrategieSequencielle(actions))
    #controleur2.environnement = Environnement(width=500, height=500)
    
    root = tk.Tk()
    root.title("Simulation Robot")
    
    affichage = [AffichageGraphique(root, adaptateur, controleur),AffichageGraphique(root, adaptateur2, controleur2)]
    for affichage in affichage:
        affichage.pack(fill=tk.BOTH, expand=True)
    
    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()
    def run_controleur2():
        while getattr(controleur2, 'running', True):
            controleur2.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur2, daemon=True)
    ctrl_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    mode_graphique()
