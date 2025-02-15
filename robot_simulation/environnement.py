from itertools import count
import math
import random

class Environnement:
    def __init__(self, width=500, height=500, obstacle_count=15):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)

    def generate_obstacles(self, count):
        """Génère des obstacles aléatoires dans l'environnement."""
        obstacles = []
        for _ in range(count):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            obstacles.append((x, y))
        return obstacles

    def detect_obstacle(self, robot):
        """Détecte si le robot est trop près d'un obstacle en prenant en compte sa taille. """
        robot_radius = robot.taille / 2  # Rayon du robot
        for obs in self.obstacles:
            distance = math.sqrt((robot.x - obs[0]) ** 2 + (robot.y - obs[1]) ** 2)
            if distance < robot_radius + 10:  # Prend en compte la taille du robot
                return True
        return False
