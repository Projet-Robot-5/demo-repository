
from abc import ABC, abstractmethod

class AdaptateurAbstrait(ABC):
    def __init__(self, robot):
        """Initialise l'adaptateur avec l'objet robot."""
        self.robot = robot
        self.distance_parcourue = 0
        self.angle_tourne = 0

    @abstractmethod
    def avancer(self, distance):
        """Fait avancer le robot d'une certaine distance."""
        pass

    @abstractmethod
    def tourner(self, angle):
        """Fait tourner le robot d'un certain angle."""
        pass 
    @abstractmethod
    def reculer(self, distance):
        """Fait reculer le robot d'une certaine distance."""
        pass

    @abstractmethod
    def stop(self):
        """Arrête le robot."""
        pass
    @abstractmethod
    def get_position(self):
        """Retourne la position actuelle du robot."""
        pass

    @abstractmethod
    def get_orientation(self):
        """Retourne l'orientation actuelle du robot."""
        pass

    @abstractmethod
    def get_distance_parcourue(self):
        """Retourne la distance totale parcourue."""
        pass