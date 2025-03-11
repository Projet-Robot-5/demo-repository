import time
class AvancerDroit:
    def _init_(self, robot, distance):
        self.robot = robot
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False