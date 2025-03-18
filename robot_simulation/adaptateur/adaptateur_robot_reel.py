class AdaptateurRobotReel:
    def __init__(self, robot):
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné
