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
        """Détecte si le robot est trop près d'un mur"""
        margin = 20
        return (
            self.robot.x < margin or self.robot.x > self.environnement.width - margin or
            self.robot.y < margin or self.robot.y > self.environnement.height - margin
        )

    def update_movement(self):
        """Met à jour la position du robot en fonction des collisions et des déplacements"""
        speed = 10
        left_speed, right_speed = self.robot.vitesse_gauche, self.robot.vitesse_droite
        print(f"Vitesse roues → Gauche: {left_speed}, Droite: {right_speed}")

        if self.current_distance < self.distance_per_side:
            left_speed = right_speed = speed
            self.current_distance += speed * 0.1
        else:
            left_speed = right_speed = 0  # Stopper temporairement avant de tourner
            self.turning = True
            self.step_count += 1
            self.current_distance = 0

        if self.turning:
            self.robot.orientation += 90  # Tourner de 90°
            self.turning = False

        self.robot.set_wheel_speed(left_speed, right_speed)
        self.robot.move(dt=0.1)

    def update_all(self):
        """Met à jour tous les éléments : robot, environnement et affichage."""
        self.update_movement()

        if self.environnement.detect_obstacle(self.robot):
            print("CRASH ! Le robot a percuté un obstacle.")
            return False  # Arrêter la simulation

        if self.detect_wall_collision():
            print("Collision avec un mur! Le robot s'est arrêté.")
            return False  # Arrêter la simulation

        print(f"Position du robot: ({self.robot.x:.2f}, {self.robot.y:.2f})")
        return True  # Continuer la simulation

    def run(self, duration=10):
        """Fait tourner la simulation pendant `duration` secondes."""
        start_time = time.time()
        while time.time() - start_time < duration:
            if not self.update():
                break  # Arrêter la simulation si crash
            time.sleep(0.1)
