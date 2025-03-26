import tkinter as tk
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieCarre

class AffichageGraphique:
    def __init__(self, master, adaptateur, controleur):
        """
        Initialise l'affichage graphique 3D de la simulation.
        Args:
            master: Fenêtre Tkinter parente
            adaptateur: Adaptateur du robot pour récupérer les positions
            controleur: Contrôleur pour accéder aux stratégies et environnement
        """
        self.master = master
        self.adaptateur = adaptateur
        self.controleur = controleur
        self.trajet = []  # Stocke les positions (x, y, z)
        self.running = True

        # Configuration de la figure matplotlib
        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim(0, 500)
        self.ax.set_ylim(0, 500)
        self.ax.set_zlim(0, 50)

        # Intégration dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Bouton de fermeture
        btn_quit = tk.Button(master, text="Quitter", command=self.on_close)
        btn_quit.pack(side=tk.BOTTOM)

        # Démarrer les mises à jour
        self.update_affichage()

    def update_affichage(self):
        """Met à jour l'affichage 3D à intervalle régulier."""
        if not self.running:
            return

        try:
            # Récupération des données
            x, y = self.adaptateur.get_position()
            z = 10  # Hauteur fixe pour la visualisation
            orientation = self.adaptateur.get_orientation()
            
            # Mise à jour de la trajectoire
            self.trajet.append((x, y, z))
            
            # Nettoyage et réaffichage
            self.ax.clear()
            self.ax.set_xlim(0, 500)
            self.ax.set_ylim(0, 500)
            self.ax.set_zlim(0, 50)

            # Affichage de la trajectoire
            if len(self.trajet) > 1:
                xs, ys, zs = zip(*self.trajet)
                self.ax.plot(xs, ys, zs, 'b-', linewidth=1)

            # Affichage des obstacles (si existants)
            if hasattr(self.controleur, 'environnement') and hasattr(self.controleur.environnement, 'obstacles'):
                for obs in self.controleur.environnement.obstacles:
                    if len(obs) >= 2:  # Vérifie qu'on a bien x et y
                        self.ax.scatter(obs[0], obs[1], 5, c='r', marker='o')

            # Affichage du robot
            self.ax.scatter(x, y, z, c='blue', s=100, marker='o')
            
            # Affichage de l'orientation
            angle_rad = math.radians(orientation)
            dx = 20 * math.cos(angle_rad)
            dy = 20 * math.sin(angle_rad)
            self.ax.quiver(x, y, z, dx, dy, 0, color='green', arrow_length_ratio=0.1)

            # Rafraîchissement
            self.canvas.draw()

            # Planification de la prochaine mise à jour
            if self.running:
                self.master.after(50, self.update_affichage)

        except Exception as e:
            print(f"Erreur lors de la mise à jour: {e}")
            self.running = False

    def on_close(self):
        """Gère la fermeture propre de l'interface."""
        self.running = False
        plt.close('all')
        self.master.destroy()