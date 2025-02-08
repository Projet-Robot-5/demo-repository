import random
import math
import tkinter as tk
import numpy as np
from .robot import Robot
from .environnement import Environnement
import time

class Simulation:
    def __init__(self, master=None):
        # Initialisation de l'environnement et du robot
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)  # Position initiale et vitesses des roues

        self.pressed_keys = set()

        self.step_count = 0  # Nombre de segments parcourus (pour le carré)
        self.distance_per_side = 100  # Distance à parcourir sur chaque côté du carré (par exemple, 100 unités)
        self.current_distance = 0  # Distance parcourue sur le côté actuel

        self.turning = False  # Indicateur si le robot doit tourner (après avoir parcouru un côté)
        
        # Si une interface graphique est demandée
        if master:
            self.master = master
            self.canvas = tk.Canvas(self.master, width=self.environnement.width, height=self.environnement.height, bg="white")
            self.canvas.pack()
            self.draw_obstacles()
