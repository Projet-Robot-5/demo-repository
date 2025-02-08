# environnement.py
import math
import random
import numpy as np
import tkinter as tk
import time


import random

class Environnement:
    def __init__(self, width=500, height=500, obstacle_count=10):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)

    def generate_obstacles(self, count):
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
                return True
        return False
