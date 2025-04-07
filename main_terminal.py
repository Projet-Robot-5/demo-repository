import sys
import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.controleur.strategie import StrategieBoucle
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.modele.robot import Robot

def mode_terminal():
    print("Mode terminal activé")
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    actions1 = [
        AvancerDroit(adaptateur, 800),]
        
    actions2 = [ Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur, 360),Tourner(adaptateur,360),Tourner(adaptateur, 360)
         
    ]
    controleur.set_strategie(StrategieSequencielle(actions1))
    controleur.set_strategie(StrategieBoucle(actions2,10))

    try:
        while True:
            controleur.update()
            if hasattr(adaptateur, 'robot'):
                x, y = adaptateur.robot.x, adaptateur.robot.y
            else:
                x, y = 0, 0
            print(f"Position estimée: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nArrêt du programme")

if __name__ == "__main__":
    mode_terminal()
