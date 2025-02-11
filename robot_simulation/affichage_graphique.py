import random
import math
import tkinter as tk
import numpy as np
from robot import Robot
from environnement import Environnement

class AffichageGraphique:
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

            # Représentation graphique du robot
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

            # Gestion des touches pour la version graphique
            self.master.bind("<KeyPress>", self.on_key_press)
            self.master.bind("<KeyRelease>", self.on_key_release)
        
        self.update()

    def draw_obstacles(self):
        """Dessine les obstacles sur la carte"""
        for obs in self.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")
    def on_key_press(self, event):
        """Ajoute la touche pressée à la liste"""
        self.pressed_keys.add(event.keysym)
    def on_key_release(self, event):
        """Retire la touche relâchée de la liste"""
        self.pressed_keys.discard(event.keysym)
    def detect_wall_collision(self):
        """Détecte si le robot est trop près d'un mur"""
        margin = 20  # Distance minimale avant de considérer une collision
        if self.robot.x < margin or self.robot.x > self.environnement.width - margin:
            return True
        if self.robot.y < margin or self.robot.y > self.environnement.height - margin:
            return True
        return False
    def update_movement(self):
        """Met à jour les vitesses des roues et fait avancer le robot en suivant un carré"""
        speed = 10  # Vitesse de base
        left_speed, right_speed = self.robot.vitesse_gauche, self.robot.vitesse_droite

        if self.current_distance < self.distance_per_side:
            # Avancer tout droit sur le côté actuel
            left_speed = right_speed = speed
            self.current_distance += speed * 0.1  # Mise à jour de la distance parcourue
        else:
            # Après avoir parcouru un côté, on tourne de 90°
            left_speed = right_speed = 0  # Arrêter les roues avant de tourner
            self.turning = True  # Indiquer que le robot va tourner
            self.step_count += 1  # Un côté est terminé
            self.current_distance = 0  # Réinitialiser la distance parcourue pour le prochain côté

        # Appliquer les vitesses des roues au robot
        self.robot.set_wheel_speed(left_speed, right_speed)
    def update(self):
        """Met à jour la position du robot et l'état de la simulation"""
        self.update_movement()

        # Vérifier les collisions avec les obstacles
        if self.environnement.detect_obstacle(self.robot):
            print("CRASH ! Le robot a percuté un obstacle.")  # Affichage du crash
            return  # Pas d’arrêt du robot, il continue de foncer


        # Vérifier les collisions avec les murs
        if self.detect_wall_collision():
            self.robot.set_wheel_speed(0, 0)  # Le robot s'arrête définitivement
            print("Collision avec un mur! Le robot s'est arrêté.")
            return  # Sort de la boucle sans mettre à jour la position

        # Si le robot a terminé un côté, il doit tourner de 90° (après avoir parcouru la distance)
        if self.turning:
            self.robot.orientation += 90  # Tourner de 90° à droite
            self.turning = False  # Réinitialiser l'indicateur de rotation

        # Déplacer le robot en fonction de la vitesse des roues
        self.robot.move(dt=0.1)

        # Mise à jour de l'affichage graphique (si disponible)
        if hasattr(self, 'canvas'):
            self.update_robot_graphics()

        # Afficher la position du robot dans le terminal
        print(f"Position du robot: ({self.robot.x:.2f}, {self.robot.y:.2f})")

        # Mise à jour de la simulation
        self.master.after(50, self.update) if hasattr(self, 'master') else None
    def update_robot_graphics(self):
        """Met à jour la représentation graphique du robot avec rotation"""
        angle_rad = math.radians(self.robot.orientation)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # Calcul des nouvelles coordonnées du robot après rotation
        coords = [
            (self.robot.x - 10 * cos_angle - 15 * sin_angle, self.robot.y - 15 * cos_angle + 10 * sin_angle),  # coin supérieur gauche
            (self.robot.x + 10 * cos_angle - 15 * sin_angle, self.robot.y - 15 * cos_angle - 10 * sin_angle),  # coin supérieur droit
            (self.robot.x + 10 * cos_angle + 15 * sin_angle, self.robot.y + 15 * cos_angle - 10 * sin_angle),  # coin inférieur droit
            (self.robot.x - 10 * cos_angle + 15 * sin_angle, self.robot.y + 15 * cos_angle + 10 * sin_angle)   # coin inférieur gauche
        ]

        self.canvas.coords(self.robot_body, *coords[0], *coords[1], *coords[2], *coords[3])

        # Mise à jour des roues
        wheel_coords = [
            (self.robot.x - 15 * cos_angle - 5 * sin_angle, self.robot.y - 5 * cos_angle + 5 * sin_angle),  # roue gauche
            (self.robot.x - 10 * cos_angle - 5 * sin_angle, self.robot.y + 5 * cos_angle + 5 * sin_angle),  # roue gauche
            (self.robot.x + 10 * cos_angle + 5 * sin_angle, self.robot.y - 5 * cos_angle - 5 * sin_angle),  # roue droite
            (self.robot.x + 15 * cos_angle + 5 * sin_angle, self.robot.y + 5 * cos_angle - 5 * sin_angle)   # roue droite
       ]

        self.canvas.coords(self.left_wheel, *wheel_coords[0], *wheel_coords[1])
        self.canvas.coords(self.right_wheel, *wheel_coords[2], *wheel_coords[3])

    
