import math
from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait


class AdaptateurRobotSimule(AdaptateurAbstrait):
    def __init__(self, robot):
        super().__init__(robot)

    def avancer(self, distance):
        """
        Fait avancer le robot simulé d'une certaine distance.
        
        :param distance: La distance à parcourir.
        """
        # Calculer la vitesse en fonction de la distance
        vitesse = distance / 10  # Exemple de conversion
        self.robot.set_wheel_speed(vitesse, vitesse)
        
        # Mettre à jour la position du robot
        angle_rad = math.radians(self.robot.orientation)
        self.robot.x += vitesse * math.cos(angle_rad)
        self.robot.y += vitesse * math.sin(angle_rad)
        
        # Mettre à jour la distance parcourue
        self.distance_parcourue += distance

    def tourner(self, angle):
        """
        Fait tourner le robot simulé d'un certain angle.
        
        :param angle: L'angle à tourner (en degrés).
        """
        if angle > 0:
            self.robot.set_wheel_speed(-4, 4)  # Rotation à gauche
        else:
            self.robot.set_wheel_speed(4, -4)  # Rotation à droite
        
        # Mettre à jour l'orientation du robot
        self.robot.orientation = (self.robot.orientation + angle) % 360
        self.angle_tourne += angle

    def reculer(self, distance):
        """
        Fait reculer le robot simulé d'une certaine distance.
        
        :param distance: La distance à reculer.
        """
        # Calculer la vitesse en fonction de la distance
        vitesse = distance / 10  # Exemple de conversion
        self.robot.set_wheel_speed(-vitesse, -vitesse)
        
        # Mettre à jour la position du robot
        angle_rad = math.radians(self.robot.orientation)
        self.robot.x -= vitesse * math.cos(angle_rad)
        self.robot.y -= vitesse * math.sin(angle_rad)
        
        # Mettre à jour la distance parcourue
        self.distance_parcourue += distance

    def stop(self):
        """Arrête le robot."""
        self.robot.set_wheel_speed(0, 0)

    def get_position(self):
        """Retourne la position actuelle du robot."""
        return self.robot.x, self.robot.y

    def get_orientation(self):
        """Retourne l'orientation actuelle du robot."""
        return self.robot.orientation

    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        return self.distance_parcourue

    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        return self.angle_tourne
    
    def get_distance_devant(self, obstacles):
        """
        Retourne la distance à l'obstacle devant en appelant le robot simulé.
        """
        return self.robot.get_distance_devant(obstacles)

    def detect_obstacle(self):
        return self.robot.detect_obstacle()

    def set_led(self, led, r, g, b):
        self.robot.set_led(led, r, g, b)

    def set_motor_dps(self, port, dps):
        self.robot.set_motor_speed(port, dps)

    def offset_motor_encoder(self, port, offset):
        self.robot.set_motor_offset(port, offset)

    def servo_rotate(self, port, angle):
        self.robot.rotate_servo(port, angle)