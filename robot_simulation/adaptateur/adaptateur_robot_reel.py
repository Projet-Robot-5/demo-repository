class AdaptateurRobotReel:
    def __init__(self, robot):
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné
    
    def avancer(self, distance):
        vitesse = distance / 10
        self.robot.set_motor_dps("MOTOR_LEFT", vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", vitesse)
        self.distance_parcourue += distance

    def tourner(self, angle):
        if angle > 0:
            self.robot.set_motor_dps("MOTOR_LEFT", -4)  # Rotation à gauche
            self.robot.set_motor_dps("MOTOR_RIGHT", 4)
        else:
            self.robot.set_motor_dps("MOTOR_LEFT", 4)  # Rotation à droite
            self.robot.set_motor_dps("MOTOR_RIGHT", -4)
        self.angle_tourne += angle

    def reculer(self, distance):
        vitesse = distance / 10
        self.robot.set_motor_dps("MOTOR_LEFT", -vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", -vitesse)
        self.distance_parcourue += distance

    def stop(self):
        """Arrête le robot."""
        self.robot.set_motor_dps("MOTOR_LEFT", 0)
        self.robot.set_motor_dps("MOTOR_RIGHT", 0)

    def get_position(self):
        """Retourne la position actuelle du robot."""
        return self.robot.get_motor_position("MOTOR_LEFT"), self.robot.get_motor_position("MOTOR_RIGHT")

    def get_orientation(self):
        """Retourne l'orientation actuelle du robot."""
        return self.angle_tourne

    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        return self.distance_parcourue

    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        return self.angle_tourne

    def detect_obstacle(self):
        return self.robot.get_distance() < 20

    def set_led(self, led, r, g, b):
        self.robot.set_led(led, r, g, b)
