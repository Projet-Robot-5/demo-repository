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
