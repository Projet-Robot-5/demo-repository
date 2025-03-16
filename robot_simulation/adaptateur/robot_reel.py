import time

class RobotReel:
    def __init__(self, robot):
        """Initialisation du robot réel en utilisant les API de contrôle matériel."""
        self.robot = robot
        self.initialiser_materiel()

    def initialiser_materiel(self):
        """Initialise les moteurs et les capteurs du robot réel."""
        print("Initialisation du matériel réel...")