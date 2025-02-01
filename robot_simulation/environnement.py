# environnement.py
import random
import numpy as np
import tkinter as tk
import time

class Environnement:
    def __init__(self, width=100, height=100, obstacle_count=10):
        self.width = width
        self.height = height
        self.obstacles = self.generate_obstacles(obstacle_count)
    
    def generate_obstacles(self, count):
        return [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(count)]
    def detect_obstacle(self, x, y):
        """Vérifie si un obstacle est dans une certaine proximité du robot"""
        for obs in self.obstacles:
            # Distance entre le robot et un obstacle
            if np.linalg.norm(np.array([x, y]) - np.array(obs)) < 15:  # 15 est la distance de détection
                return True
        return False
