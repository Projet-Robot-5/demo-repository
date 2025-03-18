class AdaptateurRobotSimule:
    def __init__(self, robot):
        """Initialise l'adaptateur pour le robot simulé."""
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné