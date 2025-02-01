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
    def draw_obstacles(self):
        """Affiche les obstacles sur la carte"""
        for obs in self.environnement.obstacles:
            self.canvas.create_oval(obs[0]-5, obs[1]-5, obs[0]+5, obs[1]+5, fill="red")
    def on_key_press(self, event):
        """Ajoute la touche pressée à la liste"""
        self.pressed_keys.add(event.keysym)
    def on_key_release(self, event):
        """Retire la touche relâchée de la liste"""
        self.pressed_keys.discard(event.keysym)

    def update_movement(self):
        """Met à jour la vitesse des roues en fonction des touches pressées"""
        speed = 30  # Vitesse de déplacement
        turn_speed = 5  # Vitesse de rotation
        left_speed, right_speed = 0, 0

        if "Up" in self.pressed_keys:
            left_speed += speed
            right_speed += speed
        if "Down" in self.pressed_keys:
            left_speed -= speed
            right_speed -= speed
        if "Left" in self.pressed_keys:
            self.robot.orientation -= turn_speed  # Tourner à gauche
        if "Right" in self.pressed_keys:
            self.robot.orientation += turn_speed  # Tourner à droite

        self.robot.set_wheel_speed(left_speed, right_speed)



