import tkinter as tk
import math
from robot import Robot
from environnement import Environnement


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

        self.left_wheel = self.canvas.create_rectangle(
            self.robot.x - 15, self.robot.y - 5,
            self.robot.x - 10, self.robot.y + 5,
            fill="black"
        )
        self.right_wheel = self.canvas.create_rectangle(
            self.robot.x + 10, self.robot.y - 5,
            self.robot.x + 15, self.robot.y + 5,
            fill="black"
        )

        # Gestion des touches
        self.master.bind("<KeyPress>", self.on_key_press)
        self.master.bind("<KeyRelease>", self.on_key_release)

        self.update()

    def draw_obstacles(self):
        """Affiche les obstacles sur la carte."""
        for obs in self.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")

    def on_key_press(self, event):
        """Ajoute la touche pressée à la liste."""
        self.pressed_keys.add(event.keysym)

    def on_key_release(self, event):
        """Retire la touche relâchée de la liste."""
        self.pressed_keys.discard(event.keysym)

    def detect_wall_collision(self, x, y):
        """Vérifie si le robot est trop près des bords de la fenêtre."""
        margin = 20  # Distance minimale avant de considérer une collision
        if x < margin or x > self.environnement.width - margin:
            return True
        if y < margin or y > self.environnement.height - margin:
            return True
        return False

    def update_movement(self):
        """Met à jour la vitesse des roues en fonction des touches pressées."""
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

    def update(self):
        """Met à jour la position du robot et gère les collisions."""
        self.update_movement()

        # Détecter les obstacles et réagir
        if self.environnement.detect_obstacle(self.robot.x, self.robot.y):
            # Si un obstacle est détecté, le robot recule puis tourne
            self.robot.set_wheel_speed(-20, -20)  # Recule
            self.robot.move(dt=0.1)
            self.robot.set_wheel_speed(20, -20)  # Tourne
            self.robot.move(dt=0.1)

        # Détecter les collisions avec les bords de la fenêtre
        if self.detect_wall_collision(self.robot.x, self.robot.y):
            # Si le robot est trop près d'un bord, il recule puis tourne
            self.robot.set_wheel_speed(-20, -20)  # Recule
            self.robot.move(dt=0.1)
            self.robot.set_wheel_speed(20, -20)  # Tourne
            self.robot.move(dt=0.1)

        # Déplacement normal
        self.robot.move(dt=0.1)

        # Mise à jour graphique
        self.update_robot_graphics(self.robot.x, self.robot.y)

        self.master.after(50, self.update)  # Rafraîchir toutes les 50ms

    def update_robot_graphics(self, x, y):
        """Met à jour la représentation graphique du robot avec rotation."""
        angle_rad = math.radians(self.robot.orientation)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # Calcul des nouvelles coordonnées du robot après rotation
        coords = [
            (x - 10 * cos_angle - 15 * sin_angle, y - 15 * cos_angle + 10 * sin_angle),  # coin supérieur gauche
            (x + 10 * cos_angle - 15 * sin_angle, y - 15 * cos_angle - 10 * sin_angle),  # coin supérieur droit
            (x + 10 * cos_angle + 15 * sin_angle, y + 15 * cos_angle - 10 * sin_angle),  # coin inférieur droit
            (x - 10 * cos_angle + 15 * sin_angle, y + 15 * cos_angle + 10 * sin_angle)   # coin inférieur gauche
        ]

        self.canvas.coords(self.robot_body, *coords[0], *coords[1], *coords[2], *coords[3])

        # Mise à jour des roues (en rotation aussi)
        wheel_coords = [
            (x - 15 * cos_angle - 5 * sin_angle, y - 5 * cos_angle + 5 * sin_angle),  # roue gauche
            (x - 10 * cos_angle - 5 * sin_angle, y + 5 * cos_angle + 5 * sin_angle),
            (x + 10 * cos_angle + 5 * sin_angle, y - 5 * cos_angle - 5 * sin_angle),  # roue droite
            (x + 15 * cos_angle + 5 * sin_angle, y + 5 * cos_angle - 5 * sin_angle)
        ]

        self.canvas.coords(self.left_wheel, *wheel_coords[0], *wheel_coords[1])
        self.canvas.coords(self.right_wheel, *wheel_coords[2], *wheel_coords[3])