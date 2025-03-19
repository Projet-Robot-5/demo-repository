from itertools import count
import math
import random

class Environnement:
    def __init__(self, robot, width=500, height=500, obstacle_count=15):
        """
        Initialise l'environnement dans lequel le robot évolue.
        
        :param robot: Le robot à placer dans l'environnement.
        :param width: Largeur de l'environnement (par défaut 500).
        :param height: Hauteur de l'environnement (par défaut 500).
        :param obstacle_count: Nombre d'obstacles à générer (par défaut 15).
        """
        self.width = width  # Largeur de l'environnement
        self.height = height  # Hauteur de l'environnement
        self.obstacles = self.generate_obstacles(obstacle_count)  # Génère les obstacles
        self.robot = robot  # Le robot qui interagira avec l'environnement

    def generate_obstacles(self, count):
        """
        Génère des obstacles aléatoires dans l'environnement.
        
        :param count: Nombre d'obstacles à générer.
        :return: Liste des positions des obstacles sous forme de tuples (x, y).
        """
        obstacles = []  # Liste pour stocker les positions des obstacles
        for _ in range(count):
            x = random.randint(50, self.width - 50)  # Position x aléatoire dans l'environnement
            y = random.randint(50, self.height - 50)  # Position y aléatoire dans l'environnement
            obstacles.append((x, y))  # Ajouter l'obstacle à la liste
        return obstacles  # Retourne la liste des obstacles générés
    
    def mettre_a_jour(self, dt=1):
        """
        Met à jour la position et l'orientation du robot à chaque itération de simulation.
        
        :param dt: Temps écoulé (par défaut 1 unité de temps).
        """
        self.robot.move(dt)  # Déplace le robot en fonction du temps écoulé
    
    def set_vitesse_roues(self, vitesse_gauche, vitesse_droite):
        """
        Modifie la vitesse des roues du robot pour le contrôle du mouvement.
        
        :param vitesse_gauche: Vitesse de la roue gauche du robot.
        :param vitesse_droite: Vitesse de la roue droite du robot.
        """
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)  # Modifie la vitesse des roues


    