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
        self.robot.wheel_distance = 40  # Distance entre les deux roues

    def update_position(self, dt):
        """
        Met à jour la position et orientation du robot en fonction de la vitesse des roues
        et cumule la distance parcourue.
        """
        v_g = self.robot.vitesse_gauche
        v_d = self.robot.vitesse_droite

        # Calcul des vitesses linéaire et angulaire
        v = (v_g + v_d) / 2  # vitesse linéaire moyenne
        omega = (v_d - v_g) / self.robot.wheel_distance  # vitesse angulaire rad/s

        # Mise à jour de la position
        angle_rad = math.radians(self.robot.orientation)
        dx = v * math.cos(angle_rad) * dt
        dy = v * math.sin(angle_rad) * dt

        self.robot.x += dx
        self.robot.y += dy

        # Mise à jour de l'orientation
        delta_angle = math.degrees(omega * dt)
        self.robot.orientation = (self.robot.orientation + delta_angle) % 360

        # Mise à jour de la distance parcourue (absolue)
        distance_step = math.sqrt(dx**2 + dy**2)
        self.distance_parcourue += distance_step

        print(f"[update_position] dt={dt:.3f}s, dx={dx:.2f}, dy={dy:.2f}, dθ={delta_angle:.2f}°, "
            f"x={self.robot.x:.2f}, y={self.robot.y:.2f}, θ={self.robot.orientation:.2f}°, "
            f"distance_total={self.distance_parcourue:.2f}")


    def get_distance_parcourue(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        self.update_position(dt)

        return self.distance_parcourue

    def avancer(self, vitesse):
        print(f"[avancer] vitesse={vitesse}")
        self.robot.set_wheel_speed(vitesse, vitesse)

    def tourner(self, angle_degres, vitesse_dps):
        # Convertir en différence de vitesse des roues
        vitesse_diff = (vitesse_dps * math.pi/180) * self.robot.wheel_distance / 2
        if angle_degres > 0:  # Gauche
            self.robot.set_wheel_speed(-vitesse_diff, vitesse_diff)
        else:  # Droite
            self.robot.set_wheel_speed(vitesse_diff, -vitesse_diff)

    def reculer(self, vitesse):
        self.robot.set_wheel_speed(-vitesse, -vitesse)

    def stop(self):
        """Arrête le robot."""
        self.robot.set_wheel_speed(0, 0)

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