import math

class Robot:
    def __init__(self, x, y, vitesse_gauche=10, vitesse_droite=10, orientation=0, taille = 20):
        self.x = x
        self.y = y
        self.orientation = orientation  # En degrés
        self.vitesse_gauche = vitesse_gauche  # Vitesse de la roue gauche
        self.vitesse_droite = vitesse_droite  # Vitesse de la roue droite
        self.wheel_distance = 30  # Distance entre les roues
        self.taille = taille  # Ajout de la taille du robot


    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        """Définit les vitesses des roues."""
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def move(self, dt=1):
        """Met à jour la position du robot en fonction des vitesses des roues."""
        vitesse_moyenne = (self.vitesse_gauche + self.vitesse_droite) / 2
        angle_rad = math.radians(self.orientation)

        # Déplacement basé sur la vitesse moyenne et l'orientation
        self.x += vitesse_moyenne * math.cos(angle_rad) * dt
        self.y += vitesse_moyenne * math.sin(angle_rad) * dt

        # Mise à jour de l'orientation (rotation si les roues ne tournent pas à la même vitesse)
        delta_orientation = (self.vitesse_droite - self.vitesse_gauche) / self.wheel_distance
        self.orientation += math.degrees(delta_orientation) * dt
        self.orientation %= 360  # Garde l'angle entre 0 et 360

    def turn(self, angle):
        """Tourne le robot d'un certain angle (en degrés)."""
        self.orientation = (self.orientation + angle) % 360
