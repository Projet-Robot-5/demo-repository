class AdaptateurRobotReel:
    def __init__(self, robot):
        """
        Initialise l'adaptateur pour le robot réel.
        
        :param robot: L'objet robot réel.
        """
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné

    def avancer(self, distance):
        """
        Fait avancer le robot réel d'une certaine distance.
        
        :param distance: La distance à parcourir.
        """
        self.robot.set_speed(12, 12)  # Vitesse constante pour avancer
        self.distance_parcourue += distance  # Mise à jour de la distance parcourue

    def tourner(self, angle):
        """
        Fait tourner le robot réel d'un certain angle.
        
        :param angle: L'angle à tourner (en degrés).
        """
        if angle > 0:
            self.robot.set_speed(-4, 4)  # Rotation à gauche
        else:
            self.robot.set_speed(4, -4)  # Rotation à droite
        self.angle_tourne += angle  # Mise à jour de l'angle tourné

    def reculer(self, distance):
        """
        Fait reculer le robot réel d'une certaine distance.
        
        :param distance: La distance à reculer.
        """
        self.robot.set_speed(-12, -12)  # Vitesse négative pour reculer
        self.distance_parcourue += distance  # Mise à jour de la distance parcourue

    def stop(self):
        """Arrête le robot."""
        self.robot.set_speed(0, 0)

    def get_position(self):
        """Retourne la position actuelle du robot."""
        return self.robot.get_position()

    def get_orientation(self):
        """Retourne l'orientation actuelle du robot."""
        return self.robot.get_orientation()

    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        return self.distance_parcourue

    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        return self.angle_tourne

    def detect_obstacle(self):
        """
        Détecte un obstacle pour le robot réel.
        
        :return: True si un obstacle est détecté, False sinon.
        """
        return self.robot.detect_obstacle()