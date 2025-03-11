from itertools import count
import math
import random

class Environnement:
    def __init__(self,robot, width=500, height=500, obstacle_count=15):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)
        self.robot = robot

    def generate_obstacles(self, count):
        """Génère des obstacles aléatoires dans l'environnement."""
        obstacles = []
        for _ in range(count):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            obstacles.append((x, y))
        return obstacles
    
    def mettre_a_jour(self, dt=1):
        """Met à jour la position et l'orientation du robot."""
        self.robot.move(dt)

    def set_vitesse_roues(self, vitesse_gauche, vitesse_droite):
        """Modifie la vitesse des roues du robot."""
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)

    

    