import math
from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait

class AdaptateurRobotReel(AdaptateurAbstrait):
    def __init__(self, robot):
        super().__init__(robot)
        self.wheel_radius = 3.5  # Rayon des roues en cm
        self.last_left_ticks = 0
        self.last_right_ticks = 0
        self.x = 0  # Position initiale
        self.y = 0
        self.orientation = 0

    def update_position(self):
        """Met à jour la position à partir des encodeurs"""
        left_ticks = self.robot.get_motor_position("MOTOR_LEFT")
        right_ticks = self.robot.get_motor_position("MOTOR_RIGHT")
        
        # Calcul du déplacement des roues
        left_dist = (left_ticks - self.last_left_ticks) * self.wheel_radius * math.pi / 180
        right_dist = (right_ticks - self.last_right_ticks) * self.wheel_radius * math.pi / 180
        
        # Mise à jour de la position et orientation
        distance = (left_dist + right_dist) / 2
        angle_change = (right_dist - left_dist) / self.robot.wheel_distance
        
        self.x += distance * math.cos(math.radians(self.orientation))
        self.y += distance * math.sin(math.radians(self.orientation))
        self.orientation = (self.orientation + math.degrees(angle_change)) % 360
        
        self.last_left_ticks = left_ticks
        self.last_right_ticks = right_ticks

    def get_distance_parcourue(self):
        self.update_position()
        return math.sqrt(self.x**2 + self.y**2)  # Distance depuis l'origine

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

    def set_motor_dps(self, port, dps):
        self.robot.set_motor_dps(port, dps)

    def offset_motor_encoder(self, port, offset):
        self.robot.offset_motor_encoder(port, offset)

    def servo_rotate(self, port, angle):
        self.robot.servo_rotate(port, angle)
