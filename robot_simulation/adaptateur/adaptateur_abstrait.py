
from abc import ABC, abstractmethod

class AdaptateurAbstrait(ABC):
    def __init__(self, robot):
        """Initialise l'adaptateur avec l'objet robot."""
        self.robot = robot
        self.distance_parcourue = 0
        self.angle_tourne = 0

    