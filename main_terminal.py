import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.robot import Robot

def initialiser_robot():
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
    return robot, adaptateur, controleur

def main():
    print("Mode terminal activé")
    robot, adaptateur, controleur = initialiser_robot()

    try:
        while True:
            controleur.update()
            x, y = adaptateur.robot.x, adaptateur.robot.y
            print(f"Position estimée: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nArrêt du programme")

if __name__ == "__main__":
    main()
