import tkinter as tk  # Importation de la bibliothèque Tkinter pour l'interface graphique
import time  # Pour gérer le temps d'attente entre les mises à jour
import threading  # Pour exécuter des tâches en parallèle (affichage graphique dans un thread)
import math
from robot_simulation.adaptateur.adaptateur_robot_reel import AdaptateurRobotReel
from robot_simulation.controleur.controleur import Controleur  # Importation de la classe Controleur pour gérer les mouvements du robot
from robot_simulation.modele.simulation import Simulation  # Importation de la classe Simulation (non utilisée dans ce code)
from robot_simulation.controleur.strategie import StrategieSequencielle # Importation de la stratégie seq
class AffichageGraphique:
    def __init__(self, master, adaptateur, controleur):
        self.master = master
        self.adaptateur = adaptateur
        self.controleur = controleur
        self.running = True
        self.trajet = []

        # Configuration du canvas
        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.pack()

        # Dessiner les obstacles initiaux
        self.draw_obstacles()

        # Démarrer les mises à jour
        self.update_affichage()

    def draw_obstacles(self):
        """Dessine les obstacles une seule fois au début"""
        if hasattr(self.controleur, 'environnement'):
            for obs in self.controleur.environnement.obstacles:
                self.canvas.create_oval(obs[0]-5, obs[1]-5, obs[0]+5, obs[1]+5, fill="red")

    def update_affichage(self):
        """Met à jour l'affichage à intervalle régulier"""
        if not self.running:
            return

        try:
            # Récupération des données ACTUELLES
            x, y = self.adaptateur.get_position()
            orientation = self.adaptateur.get_orientation()

            # Mise à jour trajectoire
            if len(self.trajet) > 0:
                prev_x, prev_y = self.trajet[-1]
                self.canvas.create_line(prev_x, prev_y, x, y, fill="black", width=2)
            self.trajet.append((x, y))

            # Effacer ancien robot
            self.canvas.delete("robot")

            # Dessiner nouveau robot
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="blue", tags="robot")
            
            # Dessiner direction
            angle_rad = math.radians(orientation)
            dx = x + 20 * math.cos(angle_rad)
            dy = y + 20 * math.sin(angle_rad)
            self.canvas.create_line(x, y, dx, dy, arrow=tk.LAST, fill="green", tags="robot")

            # Planifier prochaine mise à jour
            self.master.after(50, self.update_affichage)

        except Exception as e:
            print(f"Erreur affichage: {e}")
            self.running = False

    def on_close(self):
        """Arrêt propre"""
        self.running = False
        self.master.destroy()

    def update_display(self):
        # Récupération directe des attributs du robot
        robot = self.adaptateur.robot
        x, y = robot.x, robot.y
        orientation = robot.orientation
    
        # Effacer l'ancien robot
        self.canvas.delete("robot")
    
        # Dessiner le robot à la nouvelle position
        size = 20  # Taille du robot
        x1 = x - size
        y1 = y - size
        x2 = x + size
        y2 = y + size
    
        # Carré représentant le robot
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="robot")
    
        # Ligne indiquant l'orientation
        end_x = x + size * 1.5 * math.cos(math.radians(orientation))
        end_y = y + size * 1.5 * math.sin(math.radians(orientation))
        self.canvas.create_line(x, y, end_x, end_y, arrow=tk.LAST, width=3, fill="red", tags="robot")
    
        # Mettre à jour l'affichage des obstacles si nécessaire
        self.draw_environment()
    
        # Planifier la prochaine mise à jour
        self.master.after(50, self.update_display)