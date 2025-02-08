<<<<<<< HEAD
# environnement.py
import math
=======
>>>>>>> b6d08a48ef76f842699f7c59b85bc91a3b3971f6
import random
import numpy as np



import random

class Environnement:
<<<<<<< HEAD
    def __init__(self, width=500, height=500, obstacle_count=10):
=======
    def __init__(self, width=500, height=500, obstacle_count=15):
>>>>>>> b6d08a48ef76f842699f7c59b85bc91a3b3971f6
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)

    def generate_obstacles(self, count):
<<<<<<< HEAD
        obstacles = []
        for _ in range(count):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            obstacles.append((x, y))
        return obstacles

    def detect_obstacle(self, robot):
        """Détecte si le robot est trop près d'un obstacle"""
        for obs in self.obstacles:
            distance = math.sqrt((robot.x - obs[0]) ** 2 + (robot.y - obs[1]) ** 2)
            if distance < 20:  # Seuil de détection
=======
        """Génère des obstacles aléatoires dans l'environnement."""
        return [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(count)]

    def detect_obstacle(self, x, y):
        """Vérifie si un obstacle est dans une certaine proximité du robot."""
        for obs in self.obstacles:
            if np.linalg.norm(np.array([x, y]) - np.array(obs)) < 15:  # Distance de détection
>>>>>>> b6d08a48ef76f842699f7c59b85bc91a3b3971f6
                return True
        return False