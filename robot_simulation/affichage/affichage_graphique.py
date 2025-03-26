import tkinter as tk
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieCarre

class AffichageGraphique:
    def __init__(self, master, adaptateur, controleur):
        self.controleur = controleur
        self.master = master
        self.adaptateur = adaptateur
        
        # Création de la figure 3D
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.trajet = []  # Liste pour stocker la trajectoire du robot
        self.running = True  # Indicateur pour contrôler la boucle d'affichage

        # Démarrer la stratégie du carré
        self.controleur.strategie_courante = StrategieCarre(self.adaptateur)
        self.controleur.ajouter_strategie(self.controleur.strategie_courante)

        # Lancer la mise à jour graphique
        self.update_affichage()

    def update_affichage(self):
        if not self.running:
            return

        self.ax.clear()  # Efface le graphique précédent
        self.ax.set_xlim(-100, 100)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(0, 50)  # Ajout d'une dimension Z
        
        # Récupérer la position actuelle du robot
        x, y = self.adaptateur.get_position()
        z = 10  # Position en hauteur (ex: constante ou avec une variation)
        orientation = self.adaptateur.get_orientation()
        
        # Ajouter la nouvelle position à la trajectoire
        if len(self.trajet) > 0:
            prev_x, prev_y, prev_z = self.trajet[-1]
            self.ax.plot([prev_x, x], [prev_y, y], [prev_z, z], 'black')

        self.trajet.append((x, y, z))

        # Dessiner les obstacles
        for obs in self.controleur.environnement.obstacles:
            self.ax.scatter(obs[0], obs[1], 5, c='red', marker='o')

        # Dessiner le robot
        self.ax.scatter(x, y, z, c='blue', marker='o')
        
        # Dessiner la direction du robot
        angle_rad = math.radians(orientation)
        dir_x = x + 10 * math.cos(angle_rad)
        dir_y = y + 10 * math.sin(angle_rad)
        dir_z = z  # Conserver la même hauteur
        self.ax.plot([x, dir_x], [y, dir_y], [z, dir_z], 'green')

        # Rafraîchir l'affichage
        plt.pause(0.05)

        if not self.controleur.queue_strategies and not self.controleur.strategie_courante:
            self.running = False
            plt.close()
            return

        self.master.after(50, self.update_affichage)

    def on_close(self):
        self.running = False
        plt.close()
        self.master.destroy()