import tkinter as tk  # Importation de la bibliothèque Tkinter pour l'interface graphique
import time  # Pour gérer le temps d'attente entre les mises à jour
import threading  # Pour exécuter des tâches en parallèle (affichage graphique dans un thread)
import math
from tkinter import ttk
from robot_simulation.adaptateur.adaptateur_robot_reel import AdaptateurRobotReel
from robot_simulation.controleur.controleur import Controleur  # Importation de la classe Controleur pour gérer les mouvements du robot
from robot_simulation.modele.simulation import Simulation  # Importation de la classe Simulation (non utilisée dans ce code)
from robot_simulation.controleur.strategie import StrategieSequencielle # Importation de la stratégie seq
class AffichageGraphique(ttk.Frame):
    def __init__(self, master, adaptateur, controleur, environnement):
        super().__init__(master)
        self.adaptateur = adaptateur
        self.controleur = controleur
        self.trajectoire = []  # Pour stocker le parcours
        self.environnement = environnement
        
        # Configuration du canvas
        self.canvas = tk.Canvas(self, width=500, height=500, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Paramètres visuels
        self.robot_color = 'blue'
        self.obstacle_color = 'red'
        self.trajectoire_color = 'gray'
        self.robot_size = 10
        self.obstacle_size = 8
        self.line_width = 2

        # Dessin initial
        self.draw_environment()
        self.update_affichage()

    def draw_environment(self):
        """Dessin des obstacles ET des balises"""
        self.canvas.delete("environment")
        
        # Obstacles
        for obs in self.environnement.obstacles:
            x, y = obs
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='red', tags="obstacle")
        
        # Balises
        for balise in getattr(self.environnement, 'balises', []):
            x, y = balise
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='green', tags="balise")

    def draw_robot(self):
        """Dessine le robot et sa trajectoire"""
        self.canvas.delete("robot")
        try:
            x, y = self.adaptateur.robot.x, self.adaptateur.robot.y
            angle = self.adaptateur.robot.orientation
            
            # Ajouter le point actuel à la trajectoire
            self.trajectoire.append((x, y))
            
            # Dessiner la trajectoire
            if len(self.trajectoire) > 1:
                self.canvas.create_line(
                    self.trajectoire,
                    fill=self.trajectoire_color,
                    width=self.line_width,
                    smooth=True,
                    tags="trajectoire"
                )
            
            # Dessiner le robot
            self.canvas.create_oval(
                x-self.robot_size, y-self.robot_size,
                x+self.robot_size, y+self.robot_size,
                fill=self.robot_color,
                outline='darkblue',
                width=2,
                tags="robot"
            )
            
            # Dessiner la direction
            end_x = x + self.robot_size * 2 * math.cos(math.radians(angle))
            end_y = y + self.robot_size * 2 * math.sin(math.radians(angle))
            self.canvas.create_line(
                x, y, end_x, end_y,
                arrow=tk.LAST,
                width=3,
                fill='yellow',
                tags="robot"
            )
            
        except AttributeError:
            print("Erreur: Impossible d'accéder à la position du robot")

    def update_affichage(self):
        """Mise à jour périodique"""
        self.draw_robot()
        self.after(50, self.update_affichage)  # 20 FPS