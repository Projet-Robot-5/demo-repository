from itertools import count
import math
import random

class Environnement:
    def __init__(self, width=500, height=500, obstacle_count=15):
        """
        Initialise l'environnement dans lequel le robot évolue.
        :param width: Largeur de l'environnement (par défaut 500).
        :param height: Hauteur de l'environnement (par défaut 500).
        :param obstacle_count: Nombre d'obstacles à générer (par défaut 15).
        """
        self.width = width  # Largeur de l'environnement
        self.height = height  # Hauteur de l'environnement
        self.obstacles = self.generate_obstacles(obstacle_count)  # Génère les obstacles

    def generate_obstacles(self, count):
        """
        Génère des obstacles aléatoires dans l'environnement.
        
        :param count: Nombre d'obstacles à générer.
        :return: Liste des positions des obstacles sous forme de tuples (x, y).
        """
        margin = 50  # Marge pour éviter les bords
        return [
            (random.randint(margin, self.width - margin),
             random.randint(margin, self.height - margin))
            for _ in range(count)
        ]
    
    def detect_collision(self, robot):
        """Détecte les collisions entre le robot et les obstacles en utilisant la distance.
            Args:robot (Robot): Instance du robot à vérifier
            Returns:bool: True si collision détectée, False sinon
        """
        robot_x, robot_y = robot.get_position()
        robot_radius = robot.taille
        
        for (obs_x, obs_y) in self.obstacles:
            distance = math.sqrt((robot_x - obs_x)**2 + (robot_y - obs_y)**2)
            if distance < robot_radius:
                return True
        return False