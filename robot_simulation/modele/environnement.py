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
