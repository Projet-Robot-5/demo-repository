from robot_simulation.adaptateur.adaptateur_abstrait import AdaptateurAbstrait

class AdaptateurRobotReel(AdaptateurAbstrait):
    def __init__(self, robot):
        super().__init__(robot)
        self.distance_parcourue = 0
        self.angle_tourne = 0
        self.temps_ecoule = 0  # Temps écoulé pour les calculs
        self.angle_tourne = 0
        self.temps_ecoule = 0  # Temps écoulé pour les calculs
        self.rayon_roue = rayon_roue

    def avancer(self, vitesse):
        """Fait avancer le robot réel avec une certaine vitesse."""
        self.robot.set_motor_dps("MOTOR_LEFT", vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", vitesse)
        self.temps_ecoule += 1  # Chaque appel représente un cycle de temps
        distance_parcourue_roue = vitesse * self.temps_ecoule  # Distance parcourue par les roues
        self.distance_parcourue += distance_parcourue_roue

    def reculer(self, vitesse):
        """Fait reculer le robot réel avec une certaine vitesse."""
        self.robot.set_motor_dps("MOTOR_LEFT", -vitesse)
        self.robot.set_motor_dps("MOTOR_RIGHT", -vitesse)
        self.temps_ecoule += 1
        distance_parcourue_roue = vitesse * self.temps_ecoule
        self.distance_parcourue -= distance_parcourue_roue

    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        return self.distance_parcourue 
    def stop(self):
        """Arrête le robot."""
        self.robot.set_motor_dps("MOTOR_LEFT", 0)
        self.robot.set_motor_dps("MOTOR_RIGHT", 0)

    

    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        return self.angle_tourne

    def detect_obstacle(self):
        """Retourne vrai si un obstacle est détecté."""
        return self.robot.get_distance() < 20

    def set_led(self, led, r, g, b):
        self.robot.set_led(led, r, g, b)

    def set_motor_dps(self, port, dps):
        self.robot.set_motor_dps(port, dps)

    def offset_motor_encoder(self, port, offset):
        self.robot.offset_motor_encoder(port, offset)

    def servo_rotate(self, port, angle):
        self.robot.servo_rotate(port, angle)

