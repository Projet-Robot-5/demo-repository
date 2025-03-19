class AdaptateurRobotSimule:
    def __init__(self, robot):
        """Initialise l'adaptateur pour le robot simulé."""
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné

    def avancer(self, distance):
        vitesse = distance / 10  # Exemple de conversion
        self.robot.set_wheel_speed(vitesse, vitesse)
        self.distance_parcourue += distance

    def tourner(self, angle):
        if angle > 0:
            self.robot.set_wheel_speed(-4, 4)  # Rotation à gauche
        else:
            self.robot.set_wheel_speed(4, -4)  # Rotation à droite
        self.angle_tourne += angle
    
    def reculer(self, distance):
        vitesse = distance / 10
        self.robot.set_wheel_speed(-vitesse, -vitesse)
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
