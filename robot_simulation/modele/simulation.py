import time
import math
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot

class Simulation:
    def __init__(self):
        """Initialise l'environnement et le robot."""
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)
        if not hasattr(self, "robot") or not hasattr(self, "environnement"):
            raise ValueError("Erreur d'initialisation: robot ou environnement manquant.")
        self.obstacles = [(x, y) for (x, y) in self.environnement.obstacles if (x, y) != (self.robot.x, self.robot.y)]
        self.step_count = 0
        self.distance_per_side = 100
        self.current_distance = 0
        self.turning = False
    def detect_wall_collision(self):
        """Détecte si le robot est trop près d'un mur."""

        margin = 20 #définir la marge de sécurité pour eviter les collisions avec les murs
        return (
            self.robot.x < margin or self.robot.x > self.environnement.width - margin or self.robot.y < margin or self.robot.y > self.environnement.height - margin )
        
    def detect_obstacle(self, robot):
        """Détecte si le robot est trop près d'un obstacle en prenant en compte sa taille. """
        for obs in self.environnement.obstacles:
            distance = math.sqrt((self.robot.x - obs[0]) ** 2 + (self.robot.y - obs[1]) ** 2)
            if distance < self.robot.taille / 2 + 10:  # Distance de sécurité
                return True
        return False

    def mettre_a_jour_mouvement(self, dt=0.1):
        """Fait avancer le robot en appelant sa méthode move()."""
        self.robot.move(dt)

    def updateModele(self):
        """Met à jour l'état du robotet de l'environnement, sans logique de mouvement."""
        if self.detect_obstacle(self.robot):
            print("CRASH ! Le robot a percuté un obstacle.")
            return False
        if self.detect_wall_collision():
            print("Collision avec un mur")
            return  False
        self.mettre_a_jour_mouvement()  # Déplacement géré ici
        print(f"Position du robot: ({self.robot.x:.2f}, {self.robot.y:.2f})")
        return True
    def run(self, duration=30):
        """Lance la simulation pendant une durée donnée."""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.updateModele()
            time.sleep(0.1)