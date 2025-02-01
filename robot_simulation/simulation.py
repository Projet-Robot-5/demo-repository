import tkinter as tk
from .robot import Robot
from .environnement import Environnement
import math

class Simulation:
    def __init__(self, master):
        self.master = master
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot()

        self.pressed_keys = set()

        # Création de la fenêtre graphique
        self.canvas = tk.Canvas(self.master, width=self.environnement.width, height=self.environnement.height, bg="white")
        self.canvas.pack()

        # Dessiner les obstacles
        self.draw_obstacles()

        # Représentation du robot avec un corps (polygon) et deux roues
        self.robot_body = self.canvas.create_polygon(
            self.robot.x - 10, self.robot.y - 15, 
            self.robot.x + 10, self.robot.y - 15,
            self.robot.x + 10, self.robot.y + 15,
            self.robot.x - 10, self.robot.y + 15, 
            fill="blue", outline="black"
        )

        self.left_wheel = self.canvas.create_rectangle(self.robot.x - 15, self.robot.y - 5, self.robot.x - 10, self.robot.y + 5, fill="black")
        self.right_wheel = self.canvas.create_rectangle(self.robot.x + 10, self.robot.y - 5, self.robot.x + 15, self.robot.y + 5, fill="black")

        # Gestion des touches
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        self.update()
