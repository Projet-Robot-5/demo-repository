import math
import random

import math

class Robot:
    def __init__(self, x, y, vitesse_gauche=10, vitesse_droite=10):
        self.x = x
        self.y = y
        self.orientation = 0  # Angle en degrés
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def move(self, dt=1):
        """Met à jour la position du robot en fonction de la vitesse des roues"""
        vitesse_moyenne = (self.vitesse_gauche + self.vitesse_droite) / 2
        angle_rad = math.radians(self.orientation)

        # Déplacement basé sur la vitesse moyenne et l'orientation
        self.x += vitesse_moyenne * math.cos(angle_rad) * dt
        self.y += vitesse_moyenne * math.sin(angle_rad) * dt

    def turn(self, angle):
        """Tourne le robot d'un certain angle (en degrés)"""
        self.orientation += angle
        if self.orientation >= 360:
            self.orientation -= 360
        elif self.orientation < 0:
            self.orientation += 360
