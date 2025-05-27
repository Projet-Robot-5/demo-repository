import math
from gopigo3 import GoPiGo3
from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait

class AdaptateurRobotReel(AdaptateurAbstrait):
    def __init__(self, robot: GoPiGo3):
        super().__init__(robot)
        self.robot.MOTOR_LEFT = robot.MOTOR_LEFT
        self.robot.MOTOR_RIGHT = robot.MOTOR_RIGHT
        self.wheel_radius = 3.5  # cm
        self.robot.wheel_distance = 14.2 
        self.last_left_ticks = 0
        self.last_right_ticks = 0
        self.x = 0
        self.y = 0
        self.orientation = 0
        self.distance_parcourue_totale = 0


    def update_position(self):
        left_ticks = self.robot.get_motor_encoder(self.robot.MOTOR_LEFT)
        right_ticks = self.robot.get_motor_encoder(self.robot.MOTOR_RIGHT)

        left_dist = (left_ticks - self.last_left_ticks) * self.wheel_radius * math.pi / 180
        right_dist = (right_ticks - self.last_right_ticks) * self.wheel_radius * math.pi / 180
        distance = (left_dist + right_dist) / 2

        dx = distance * math.cos(math.radians(self.orientation))
        dy = distance * math.sin(math.radians(self.orientation))

        self.x += dx
        self.y += dy

        delta_theta = (right_dist - left_dist) / self.robot.wheel_distance
        self.orientation = (self.orientation + math.degrees(delta_theta)) % 360

        self.distance_parcourue_totale += abs(distance)
        self.last_left_ticks = left_ticks
        self.last_right_ticks = right_ticks



    
    def avancer(self, vitesse=50):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, vitesse)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, vitesse)

    def reculer(self, vitesse=50):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, -vitesse)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, -vitesse)

    def tourner(self, angle_degres, vitesse_dps=50):
        angle_rad = math.radians(abs(angle_degres))
        arc_length = angle_rad * (self.robot.wheel_distance / 2)
        ticks = (arc_length / (self.wheel_radius * math.pi)) * 360  # en degrés moteurs

        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, 0)
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, 0)

        direction = 1 if angle_degres > 0 else -1

        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, -direction * vitesse_dps)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, direction * vitesse_dps)

        while True:
            left = abs(self.robot.get_motor_encoder(self.robot.MOTOR_LEFT))
            right = abs(self.robot.get_motor_encoder(self.robot.MOTOR_RIGHT))
            if (left + right) / 2 >= ticks:
                break
            time.sleep(0.01)

        self.stop()


    def stop(self):
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, 0)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, 0)

    def get_distance_parcourue(self):
        return self.distance_parcourue_totale

    def get_angle_tourne(self):
        return self.orientation
    

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
