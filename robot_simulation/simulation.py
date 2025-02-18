import time
import math
from .robot import Robot
from .environnement import Environnement
from .environnement import Environnement
from .robot import Robot

class Simulation:
    def __init__(self):
        """Initialise l'environnement et le robot."""
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)
        if not hasattr(self, "robot") or not hasattr(self, "environnement"):
            raise ValueError("Erreur d'initialisation: robot ou environnement manquant.")
        self.step_count = 0
        self.distance_per_side = 100
        self.current_distance = 0
        self.turning = False
    def detect_wall_collision(self):
        """Détecte si le robot est trop près d'un mur."""
        margin = 20 #définir la marge de sécurité pour eviter les collisions avec les murs
        return (
            self.robot.x < margin or self.robot.x > self.environnement.width - margin or self.robot.y < margin or self.robot.y > self.environnement.height - margin )
        
        

    def updateModele(self):
        """Met à jour l'état du robotet de l'environnement, sans logique de mouvement."""
        if self.environnement.detect_obstacle(self.robot):
            print("CRASH ! Le robot a percuté un obstacle.")
            return False
        if self.detect_wall_collision():
            print("Collision avec un mur")
            return  False
        print(f"Position du robot: ({self.robot.x:.2f}, {self.robot.y:.2f})")
        return True