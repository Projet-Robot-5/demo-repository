import tkinter as tk
from .robot import Robot
from .environnement import Environnement
import math

class Simulation:
    def __init__(self, racine):
        """Initialise la simulation, l'environnement et le robot."""
        self.env = Environnement(racine, largeur=500, hauteur=500)  # Pass width and height
        self.canevas = self.env.obtenir_canevas()
        self.robot = Robot(self.canevas)

        # Ajouter des obstacles pour tester
        self.obstacles = [(150, 150), (250, 250), (350, 150)]  # Exemple d'obstacles
        for obs in self.obstacles:
            self.env.dessiner_obstacle(obs[0], obs[1])

        # Lier les touches du clavier pour déplacer et faire tourner le robot
        racine.bind("<Up>", self.deplacer_robot)
        racine.bind("<Left>", self.tourner_gauche)
        racine.bind("<Right>", self.tourner_droite)

    def deplacer_robot(self, event):
        """Déplacer le robot dans la direction qu'il regarde, avec détection d'obstacle et bordure."""
        # Si un obstacle est détecté, tourner
        if self.robot.detecter_obstacle(self.obstacles):
            self.robot.tourner("droite")  # Tourner à droite si obstacle détecté
        elif self.robot.detecter_bordure(self.canevas.winfo_width(), self.canevas.winfo_height()):
            self.robot.tourner("gauche")  # Tourner à gauche si au bord
        else:
            self.robot.avancer(10)  # Avancer si aucune détection

    def tourner_gauche(self, event):
        """Tourner le robot à gauche."""
        self.robot.tourner("gauche")

    def tourner_droite(self, event):
        """Tourner le robot à droite."""
        self.robot.tourner("droite")
