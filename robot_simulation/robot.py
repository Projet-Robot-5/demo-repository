import math


class Robot:
    def __init__(self, x=250, y=250, orientation=0):
        self.x = x
        self.y = y
        self.orientation = orientation  # En degrés
        self.wheel_speed_left = 0  # Vitesse roue gauche
        self.wheel_speed_right = 0  # Vitesse roue droite
        self.wheel_distance = 30  # Distance entre les roues

    def set_wheel_speed(self, left_speed, right_speed):
        """Définit les vitesses des roues."""
        self.wheel_speed_left = left_speed
        self.wheel_speed_right = right_speed

    def move(self, dt=0.1):
        """Met à jour la position du robot en fonction des vitesses des roues."""
        v_left = self.wheel_speed_left
        v_right = self.wheel_speed_right
        v = (v_left + v_right) / 2  # Vitesse moyenne
        omega = (v_right - v_left) / self.wheel_distance  # Rotation

        # Mettre à jour l'orientation (convertie en degrés)
        self.orientation += omega * dt * 180 / math.pi

        # Mettre à jour la position
        self.x += v * math.cos(math.radians(self.orientation)) * dt
        self.y += v * math.sin(math.radians(self.orientation)) * dt