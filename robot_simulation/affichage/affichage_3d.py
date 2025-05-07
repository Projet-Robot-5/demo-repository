import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Affichage3D:
    def __init__(self, adaptateur, controleur):
        self.adaptateur = adaptateur
        self.controleur = controleur
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([0, 500])
        self.ax.set_ylim([0, 500])
        self.ax.set_zlim([0, 500])
        self.trajet = []

    def update_affichage(self):
        """Met à jour l'affichage 3D à intervalle régulier"""
        x, y = self.adaptateur.get_position()
        z = 0  # Supposons que le robot se déplace sur un plan 2D
        orientation = self.adaptateur.get_orientation()

        # Mise à jour trajectoire
        if len(self.trajet) > 0:
            prev_x, prev_y, prev_z = self.trajet[-1]
            self.ax.plot([prev_x, x], [prev_y, y], [prev_z, z], color='black')
        self.trajet.append((x, y, z))

        # Effacer ancien robot
        self.ax.cla()

        # Dessiner nouveau robot
        self.ax.scatter(x, y, z, color='blue')

        # Dessiner direction
        angle_rad = np.radians(orientation)
        dx = x + 20 * np.cos(angle_rad)
        dy = y + 20 * np.sin(angle_rad)
        self.ax.quiver(x, y, z, dx-x, dy-y, 0, color='green')

        # Dessiner obstacles
        if hasattr(self.controleur, 'environnement'):
            for obs in self.controleur.environnement.obstacles:
                self.ax.scatter(obs[0], obs[1], 0, color='red')

        plt.draw()
        plt.pause(0.05)

    def on_close(self):
        """Arrêt propre"""
        plt.close(self.fig)