import math
from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait

class AdaptateurRobotSimule(AdaptateurAbstrait):
    def __init__(self, robot,rayon_roue):
        super().__init__(robot) 
        self.distance_parcourue = 0
        self.angle_tourne = 0
        self.temps_ecoule = 0  # Temps écoulé pour les calculs
        self.rayon_roue = rayon_roue  # Rayon des roues
        self.robot.x = 0  # Position initiale du robot (x)
        self.robot.y = 0  # Position initiale du robot (y)
        self.robot.orientation = 0  # Orientation initiale du robot en degrés (0 = orientation vers la droite)
    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        """Ajuste les vitesses des roues du robot simulé."""
        # Logique pour mettre à jour les vitesses des roues
        # Supposons que les vitesses sont en m/s et on les applique aux roues
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)
    def avancer(self, vitesse, dt):
        """
        Fait avancer le robot simulé avec une certaine vitesse.
        
        :param vitesse: Vitesse du robot en m/s
        :param dt: Temps écoulé depuis la dernière mise à jour
        """
        # Calcul de la distance parcourue pendant le temps écoulé
        distance_parcourue = vitesse * dt
        
        # Mise à jour de la position du robot en fonction de sa vitesse et de son orientation
        angle_rad = math.radians(self.robot.orientation)  # Conversion de l'orientation en radians
        dx = distance_parcourue * math.cos(angle_rad)  # Calcul du déplacement en x
        dy = distance_parcourue * math.sin(angle_rad)  # Calcul du déplacement en y
        
        # Mise à jour des coordonnées du robot
        self.robot.x += dx
        self.robot.y += dy
        
        # Mise à jour de la distance totale parcourue
        self.distance_parcourue += distance_parcourue
        
        # Appliquer la vitesse aux roues du robot (simulé)
        self.robot.set_wheel_speed(vitesse, vitesse)

    def reculer(self, vitesse, dt):
        """
        Fait reculer le robot simulé avec une certaine vitesse.
        
        :param vitesse: Vitesse du robot en m/s
        :param dt: Temps écoulé depuis la dernière mise à jour
        """
        # Calcul de la distance parcourue pendant le temps écoulé (en reculant)
        distance_parcourue = vitesse * dt
        
        # Mise à jour de la position du robot en fonction de sa vitesse et de son orientation (en reculant)
        angle_rad = math.radians(self.robot.orientation)  # Conversion de l'orientation en radians
        dx = -distance_parcourue * math.cos(angle_rad)  # Calcul du déplacement en x (négatif pour le recul)
        dy = -distance_parcourue * math.sin(angle_rad)  # Calcul du déplacement en y (négatif pour le recul)
        
        # Mise à jour des coordonnées du robot
        self.robot.x += dx
        self.robot.y += dy
        
        # Mise à jour de la distance totale parcourue (négative pour le recul)
        self.distance_parcourue -= distance_parcourue
        
        # Appliquer la vitesse aux roues du robot (simulé)
        self.robot.set_wheel_speed(-vitesse, -vitesse)

    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        return self.distance_parcourue
    def tourner(self, angle):
        """
        Fait tourner le robot simulé d'un certain angle.
        """
        if angle > 0:
            self.robot.set_wheel_speed(-4, 4)  # Rotation à gauche
        else:
            self.robot.set_wheel_speed(4, -4)  # Rotation à droite

        # Mise à jour de l'orientation du robot
        self.robot.orientation = (self.robot.orientation + angle) % 360
        self.angle_tourne += angle

    
    def stop(self):
        """Arrête le robot."""
        self.robot.set_wheel_speed(0, 0)

    

    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        return self.angle_tourne

    def get_distance_devant(self, obstacles):
        """
        Retourne la distance à l'obstacle devant en appelant le robot simulé.
        """
        return self.robot.get_distance_devant(obstacles)

    def detect_obstacle(self):
        """Retourne vrai si un obstacle est détecté."""
        return self.robot.detect_obstacle()

    def set_led(self, led, r, g, b):
        self.robot.set_led(led, r, g, b)

    def set_motor_dps(self, port, dps):
        self.robot.set_motor_speed(port, dps)

    def offset_motor_encoder(self, port, offset):
        self.robot.set_motor_offset(port, offset)

    def servo_rotate(self, port, angle):
        self.robot.rotate_servo(port, angle)
    def get_orientation(self):
        """Retourne l'orientation actuelle du robot."""
        return self.robot.orientation

    def get_position(self):
        """Retourne la position actuelle du robot sous forme de tuple (x, y)."""
        return (self.robot.x, self.robot.y)