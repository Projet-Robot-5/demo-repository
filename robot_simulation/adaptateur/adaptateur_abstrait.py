
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
    @abstractmethod
    def get_angle_tourne(self):
        """Retourne l'angle total tourné."""
        pass

    @abstractmethod
    def detect_obstacle(self):
        """Détecte un obstacle et retourne True si détecté, False sinon."""
        pass

    @abstractmethod
    def set_led(self, led, r, g, b):
        """Active ou désactive les LEDs du robot avec une couleur spécifiée."""
        pass 
    @abstractmethod
    def set_motor_dps(self, port, dps):
        """Régle la vitesse du moteur à une valeur donnée."""
        pass

    @abstractmethod
    def offset_motor_encoder(self, port, offset):
        """Effectue un offset sur l'encodeur du moteur."""
        pass

    @abstractmethod
    def servo_rotate(self, port, angle):
        """Fait tourner un servo à un angle donné."""
        pass