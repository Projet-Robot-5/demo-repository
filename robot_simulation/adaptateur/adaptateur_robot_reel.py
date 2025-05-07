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
        self.distance_parcourue_totale = 0
        self.angle_tourne = 0

    def update_position(self):
        """Met à jour la position et cumule la distance parcourue depuis le dernier appel."""
        left_ticks = self.robot.get_motor_position("MOTOR_LEFT")
        right_ticks = self.robot.get_motor_position("MOTOR_RIGHT")

        # Calcul du déplacement des roues (en cm)
        left_dist = (left_ticks - self.last_left_ticks) * self.wheel_radius * math.pi / 180
        right_dist = (right_ticks - self.last_right_ticks) * self.wheel_radius * math.pi / 180

        # Distance moyenne parcourue par le robot depuis la dernière mise à jour
        distance = (left_dist + right_dist) / 2

        # Mise à jour de la position
        self.x += distance * math.cos(math.radians(self.orientation))
        self.y += distance * math.sin(math.radians(self.orientation))

        # Mise à jour de l'orientation
        angle_change = (right_dist - left_dist) / self.robot.wheel_distance
        self.orientation = (self.orientation + math.degrees(angle_change)) % 360

        # Mise à jour de la distance totale parcourue
        self.distance_parcourue_totale += abs(distance)

        # Mise à jour des ticks pour la prochaine itération
        self.last_left_ticks = left_ticks
        self.last_right_ticks = right_ticks



    
    def avancer(self, vitesse=50):
        """Fait avancer le robot à une certaine vitesse (en degrés/seconde)."""
        self.robot.set_motor_dps("MOTOR_LEFT", vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", vitesse)

    def reculer(self, vitesse=50):
        """Fait reculer le robot à une certaine vitesse (en degrés/seconde)."""
        self.robot.set_motor_dps("MOTOR_LEFT", -vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", -vitesse)

    def tourner(self, angle_degres, vitesse_dps=50):
        """
        Fait tourner le robot d'un angle donné (en degrés) sur place.

        :param angle_degres: l’angle à tourner (positif = gauche, négatif = droite)
        :param vitesse_dps: vitesse des moteurs en degrés par seconde
        """
        angle_rad = math.radians(abs(angle_degres))
        demie_base = self.robot.wheel_distance / 2  # distance du centre au moteur

        # Distance que chaque roue doit parcourir
        arc_length = angle_rad * demie_base

        # Conversion en degrés d’encodeur moteur
        ticks = (arc_length / (self.wheel_radius * math.pi)) * 180

        # Définir les directions
        if angle_degres > 0:  # tourner à gauche
            self.robot.offset_motor_encoder("MOTOR_LEFT", 0)
            self.robot.offset_motor_encoder("MOTOR_RIGHT", 0)
            self.robot.set_motor_limits("MOTOR_LEFT", dps=vitesse_dps)
            self.robot.set_motor_limits("MOTOR_RIGHT", dps=vitesse_dps)
            self.robot.set_motor_position_relative("MOTOR_LEFT", -ticks)
            self.robot.set_motor_position_relative("MOTOR_RIGHT", ticks)
        else:  # tourner à droite
            self.robot.offset_motor_encoder("MOTOR_LEFT", 0)
            self.robot.offset_motor_encoder("MOTOR_RIGHT", 0)
            self.robot.set_motor_limits("MOTOR_LEFT", dps=vitesse_dps)
            self.robot.set_motor_limits("MOTOR_RIGHT", dps=vitesse_dps)
            self.robot.set_motor_position_relative("MOTOR_LEFT", ticks)
            self.robot.set_motor_position_relative("MOTOR_RIGHT", -ticks)

    def stop(self):
        """Arrête le robot."""
        self.robot.set_motor_dps("MOTOR_LEFT", 0)
        self.robot.set_motor_dps("MOTOR_RIGHT", 0)


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
