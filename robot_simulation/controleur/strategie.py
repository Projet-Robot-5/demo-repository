import time
class AvancerDroit:
    def _init_(self, robot, distance):
        self.robot = robot
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False
    def start(self):
        """Démarre la stratégie d'avance."""
        self.distance_parcourue = 0
        self.robot.set_wheel_speed(12, 12)
        self.actif = True
        print("Début de l'avance droite")