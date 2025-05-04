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
            self.orientation += delta_orientation  # Conversion en degrés
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
    Calcule la distance en cm au premier obstacle dans un cône devant le robot.
    Les obstacles sont des tuples (x, y) ou (x, y, w, h).
    """
    from math import cos, sin, radians, sqrt, atan2, degrees

    x, y = self.x, self.y
    angle = radians(self.orientation)  # Orientation en radians
    dx = cos(angle)
    dy = sin(angle)

    min_distance = float("inf")
    angle_tolerance = radians(30)  # cône de 60° au total

    for obs in obstacles:
        # Supporte les obstacles sous forme (x, y) ou (x, y, w, h)
        ox, oy = obs[0], obs[1]

        vx = ox - x
        vy = oy - y
        distance = sqrt(vx**2 + vy**2)
        if distance == 0:
            continue  # Ignore le point s’il est à la même position

        # Calcul de l'angle entre le vecteur du robot et le vecteur vers l'obstacle
        angle_to_obstacle = atan2(vy, vx)
        angle_diff = abs((angle_to_obstacle - angle + 3.14159) % (2 * 3.14159) - 3.14159)

        if angle_diff <= angle_tolerance:
            min_distance = min(min_distance, distance)

    # Conversion en centimètres (si 1 pixel = 1 cm)
    return round(min_distance, 2) if min_distance != float("inf") else -1
