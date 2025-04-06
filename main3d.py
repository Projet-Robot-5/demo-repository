import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_3d import Affichage3D
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.environnement import Environnement

def mode_3d():
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

    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)

    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
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
    mode_3d()
