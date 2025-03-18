class AdaptateurRobotReel:
    def __init__(self, robot):
        self.robot = robot
        self.distance_parcourue = 0  # Distance totale parcourue
        self.angle_tourne = 0  # Angle total tourné
    
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
