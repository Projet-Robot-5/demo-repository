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
    def step(self):
        """Fait avancer le robot d'une petite étape."""
        if not self.actif:
            return
        self.robot.move(dt=1)
        self.distance_parcourue += 12
        print(f"Avance droite: {self.distance_parcourue}/{self.distance}")
        print(f"Position: ({self.robot.x}, {self.robot.y})")
        print(f"Orientation: {self.robot.orientation}")
    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)
        return not self.actif  

class Tourner: