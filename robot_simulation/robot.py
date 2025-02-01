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
        """Définit les vitesses des roues"""
        self.wheel_speed_left = left_speed
        self.wheel_speed_right = right_speed

