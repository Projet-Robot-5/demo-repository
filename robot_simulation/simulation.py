import tkinter as tk
from robot_simulation.robot import Robot
from robot_simulation.environnement import Environnement

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
        racine.bind("<Up>", self.accelerer)
        racine.bind("<Donwn>", self.ralentir)
        racine.bind("<Left>", self.tourner_gauche)
        racine.bind("<Right>", self.tourner_droite)
    def accelerer(self , event):
        """Accélérer les deux roues."""
        self.robot.set_vitesse_roues(10,10)
        self.deplacer_robot()
    def ralentir(self, event):
        """Ralentir les deux roues. """
        self.robot.set_vitesse_roues(-10,-10)
        self.deplacer_robot()
    def deplacer_robot(self, event):
        """Déplacer le robot en évitant les obstacles et les bordures."""
        # Si un obstacle est détecté, tourner
        self.robot.eviter_obstacle(self.obstacles,self.canevas.winfo_width(),self.canevas.winfo_height())

    def tourner_gauche(self, event):
        """Tourner le robot à gauche."""
        self.robot.tourner("gauche")

    def tourner_droite(self, event):
        """Tourner le robot à droite."""
        self.robot.tourner("droite")
