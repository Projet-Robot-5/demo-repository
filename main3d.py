import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_3d import Affichage3D
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.environnement import Environnement
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
    controleur.environnement = Environnement()
    return robot, adaptateur, controleur

def run_controleur(controleur):
    while getattr(controleur, 'running', True):
        controleur.update()
        time.sleep(0.05)

def main():
    robot, adaptateur, controleur = initialiser_robot()

    ctrl_thread = threading.Thread(target=run_controleur, args=(controleur,), daemon=True)
    ctrl_thread.start()

    affichage = Affichage3D(adaptateur, controleur)
    try:
        while getattr(controleur, 'running', True):
            affichage.update_affichage()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nArrêt du programme")
    finally:
        affichage.on_close()

if __name__ == "__main__":
    main()
