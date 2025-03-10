import time

class AvancerDroit:
    def __init__(self, robot, distance):
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

    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)
        return not self.actif  

class Tourner:
    def __init__(self, robot, angle):
        self.robot = robot
        self.angle = angle
        self.angle_tourne = 0
        self.actif = False

    def start(self):
        """Démarre la rotation."""
        self.angle_tourne = 0
        self.robot.set_wheel_speed(-12, 12)
        self.actif = True
        print("Début de la rotation")

    def step(self):
        """Effectue la rotation par petites étapes."""
        if not self.actif:
            return
        self.robot.move(dt=1)
        self.angle_tourne += 10  # Ajustement pour forcer un 90° précis
        self.robot.orientation = (self.robot.orientation + 10) % 360
        print(f"Rotation: {self.angle_tourne}/{self.angle} | Orientation: {self.robot.orientation}")
    
    def stop(self):
        """Retourne vrai si la rotation est terminée."""
        if self.angle_tourne >= self.angle:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)
            self.robot.orientation = (self.robot.orientation // 90) * 90  # Correction orientation
        return not self.actif
