import math



class Robot:
    def __init__(self, x, y, vitesse_gauche=10, vitesse_droite=10):
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

        # Mettre à jour la position
        self.x += v * math.cos(math.radians(self.orientation)) * dt
        self.y += v * math.sin(math.radians(self.orientation)) * dt

