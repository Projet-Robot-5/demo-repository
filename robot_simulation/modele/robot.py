import math

class Robot:
    def __init__(self, x, y, vitesse_gauche=10, vitesse_droite=10, orientation=0, taille = 20):
        self.x = x
        self.y = y
        self.orientation = 0  # En degrés
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

        # Ajout de l'angle de rotation
        if self.vitesse_gauche != self.vitesse_droite:  # Rotation uniquement si vitesses différentes
            rotation_vitesse = (self.vitesse_droite - self.vitesse_gauche) / self.wheel_distance
            delta_orientation = math.degrees(rotation_vitesse * dt) 
            self.orientation += delta_orientation# Conversion en degrés
            self.orientation %= 360