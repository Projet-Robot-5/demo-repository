import random
import numpy as np


class Environnement:
    def __init__(self, width=500, height=500, obstacle_count=15):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)

    def generate_obstacles(self, count):
        """Génère des obstacles aléatoires dans l'environnement."""
        return [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(count)]

    def detect_obstacle(self, x, y):
        """Vérifie si un obstacle est dans une certaine proximité du robot."""
        for obs in self.obstacles:
            if np.linalg.norm(np.array([x, y]) - np.array(obs)) < 15:  # Distance de détection
                return True
        return False