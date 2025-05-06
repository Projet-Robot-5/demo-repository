import math
import time
from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait

class AdaptateurRobotSimule(AdaptateurAbstrait):
    def __init__(self, robot):
        super().__init__(robot)
        self.last_time = time.time()
        self.last_position = (robot.x, robot.y)
        self.last_orientation = robot.orientation
        self.distance_parcourue = 0
        self.angle_tourne = 0

    def update_position(self, dt):
        """Met à jour la position à partir des vitesses"""
        vitesse_lineaire = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        angle_rad = math.radians(self.robot.orientation)
        
        self.robot.x += vitesse_lineaire * math.cos(angle_rad) * dt
        self.robot.y += vitesse_lineaire * math.sin(angle_rad) * dt
        
        if self.robot.vitesse_gauche != self.robot.vitesse_droite:
            rotation_vitesse = (self.robot.vitesse_droite - self.robot.vitesse_gauche) / self.robot.wheel_distance
            self.robot.orientation += math.degrees(rotation_vitesse * dt) % 360

    def get_distance_parcourue(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        self.update_position(dt)
        distance = math.sqrt((self.robot.x - self.last_position[0])**2 + 
                             (self.robot.y - self.last_position[1])**2)
        self.last_position = (self.robot.x, self.robot.y)
        self.distance_parcourue += distance
        return distance

    def avancer(self, distance):
        """
        Fait avancer le robot simulé d'une certaine distance (en cm).
        """
        vitesse = distance / 10  # Conversion simple
        self.robot.set_wheel_speed(vitesse, vitesse)
        print(f"[SIMULE] Avance de {distance} cm à {vitesse:.2f} unités")

    def tourner(self, angle):
        """
        Fait tourner le robot simulé d'un certain angle (en degrés).
        """
        if angle > 0:
            self.robot.set_wheel_speed(-4, 4)
        else:
            self.robot.set_wheel_speed(4, -4)
        self.robot.orientation = (self.robot.orientation + angle) % 360
        self.angle_tourne += angle
        print(f"[SIMULE] Tourne de {angle} degrés")

    def reculer(self, distance):
        """
        Fait reculer le robot simulé d'une certaine distance (en cm).
        """
        vitesse = distance *200
        self.robot.set_wheel_speed(-vitesse, -vitesse)
        print(f"[SIMULE] Recule de {distance} cm à {vitesse:.2f} unités")

    def stop(self):
        """Arrête le robot."""
        self.robot.set_wheel_speed(0, 0)
        print("[SIMULE] Robot arrêté.")

    def get_angle_tourne(self):
        return self.angle_tourne

    def get_distance_devant(self, obstacles):
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
