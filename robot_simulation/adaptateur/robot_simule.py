import math
import time

def __init__(self, robot, x, y, direction_x, direction_y, environnement):
    self.robot = robot  # Robot réel ou simulé
    self.x = x  # Position x du robot
    self.y = y  # Position y du robot
    self.direction_x = direction_x  # Direction dans l'axe X
    self.direction_y = direction_y  # Direction dans l'axe Y
    self.environnement = environnement  # Environnement dans lequel le robot évolue

    self.angle_parcouru = 0  # Angle du robot, initialisé à 0
    self.distance_parcouru = 0  # Distance parcourue par le robot, initialisée à 0
    self.temps_passe = time.time()  # Temps initial
    self.rayon_roue = 10  # Rayon des roues (par exemple, 10 unités)
    self.largeur = 20  # Largeur entre les roues du robot, exemple : 20 unités

def set_vitesse(self, vitesse_gauche, vitesse_droite):
    """Définit les vitesses des roues gauche et droite du robot."""
    self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)

def update_temps_passe(self):
    """Mise à jour du temps passé depuis la dernière mise à jour."""
    temps_actuel = time.time()
    temps_passe = temps_actuel - self.temps_passe
    self.temps_passe = temps_actuel
    return temps_passe
