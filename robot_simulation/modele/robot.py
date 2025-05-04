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
        self.is_moving = False  # État de mouvement
        self.balise_detectee = False
        self.balise_position = (0, 0)  # (x,y)

    def detecter_balise(self, environnement):
        """Détecte la balise la plus proche"""
        self.balise_detectee = False
        if not hasattr(self, 'environnement') or not hasattr(self.environnement, 'balises'):
            return False
            
        for balise in environnement.balises:
            distance = math.sqrt((self.x - balise[0])**2 + (self.y - balise[1])**2)
            if distance < 50:  # Portée de détection
                self.balise_detectee = True
                self.balise_position = balise
                return True
        return False
    
    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        """Définit les vitesses des roues."""
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.is_moving = (vitesse_gauche != 0 or vitesse_droite != 0)

    def move(self, dt=1):
        """Met à jour la position du robot en fonction des vitesses des roues."""
        if not self.is_moving:
            return

        # Calcul du déplacement linéaire
        vitesse_lineaire = (self.vitesse_gauche + self.vitesse_droite) / 2
        angle_rad = math.radians(self.orientation)

        self.x += vitesse_lineaire * math.cos(angle_rad) * dt
        self.y += vitesse_lineaire * math.sin(angle_rad) * dt

        # Ajout de l'angle de rotation
        if self.vitesse_gauche != self.vitesse_droite:  # Rotation uniquement si vitesses différentes
            rotation_vitesse = (self.vitesse_droite - self.vitesse_gauche) / self.wheel_distance
            delta_orientation = math.degrees(rotation_vitesse * dt) 
            self.orientation += delta_orientation# Conversion en degrés
            self.orientation %= 360

    def stop(self):
        """Arrête immédiatement le robot."""
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
        self.is_moving = False

    def get_position(self):
        """Retourne la position actuelle (x,y)."""
        return (self.x, self.y)

    def get_orientation(self):
        """Retourne l'orientation actuelle en degrés."""
        return self.orientation
    
    def get_distance_devant(self, obstacles):
        """
        Calcule la distance au premier obstacle devant le robot.
        """
        from math import cos, sin, radians, sqrt

        x, y = self.x, self.y
        angle = self.orientation  # En degrés
        dx = cos(radians(angle))
        dy = sin(radians(angle))

        min_distance = float("inf")

        for obs in obstacles:
            ox, oy, ow, oh = obs
            cx = ox + ow / 2
            cy = oy + oh / 2
            distance = sqrt((cx - x)**2 + (cy - y)**2)

            # Vérification si obstacle est dans la direction approximative
            direction_vector = ((cx - x) * dx + (cy - y) * dy)
            if direction_vector > 0:
                min_distance = min(min_distance, distance)

        return min_distance if min_distance != float("inf") else -1

    def get_distance_parcourue(self):
        """
        Calcule la distance entre la position actuelle du robot et l’origine (0, 0).
        :return: distance en cm
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

