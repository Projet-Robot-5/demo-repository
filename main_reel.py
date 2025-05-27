import time
from gopigo3 import GoPiGo3
from robot_simulation.adaptateur.adaptateur_robot_reel import AdaptateurRobotReel
from robot_simulation.controleur.strategie import faire_carre
def main():
    robot = GoPiGo3()
    adaptateur = AdaptateurRobotReel(robot)

    strategie = faire_carre(adaptateur, longueur=30, angle=90, vitesse=50, vitesse_rotation=50)

    strategie.start()
    while not strategie.stop():
        strategie.step()
        adaptateur.update_position()
        time.sleep(0.05)

if __name__ == "__main__":
    main()
