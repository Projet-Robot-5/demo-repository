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
    def _init_(self, robot, angle):
        self.robot = robot
        self.angle = angle  # Angle total à tourner
        self.angle_tourne = 0  # Angle déjà tourné
        self.actif = False
    def start(self):
        """Démarre la rotation."""
        self.angle_tourne = 0
        self.robot.set_wheel_speed(-4, 4)  # Rotation à gauche
        self.actif = True
        print(f"Début de la rotation de {self.angle} degrés")
    def step(self):
        """Effectue la rotation par petites étapes."""
        if not self.actif:
            return

        # Faire avancer le robot pendant un petit pas de temps
        self.robot.move(dt=1)

        # Mettre à jour l'angle tourné
        self.angle_tourne += 45  # Supposons que chaque étape tourne de 5 degrés

        # Mettre à jour l'orientation du robot
        self.robot.orientation = (self.robot.orientation + 45) % 360

        # Ajuster l'orientation pour qu'elle soit toujours proche d'un multiple de 90
        if self.angle_tourne % 90 == 0:
            self.robot.orientation = round(self.robot.orientation / 90) * 90
            self.robot.orientation %= 360  # Garantir que l'orientation est entre 0 et 360

        print(f"Rotation: {self.angle_tourne}/{self.angle} | Orientation: {self.robot.orientation}")