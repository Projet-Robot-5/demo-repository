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
    
