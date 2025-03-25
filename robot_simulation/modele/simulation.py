import time
import math
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot

class Simulation:
    def __init__(self, master=None):
        """Initialise la simulation, gère l'environnement et le robot"""
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)

    def updateModele(self):
        """
        Met à jour le modèle de simulation à chaque tick:
        1. Fait bouger le robot
        2. Détecte les collisions
        3. Met à jour l'environnement si nécessaire
        Retourne False si collision détectée, True sinon
        """
        # Faire bouger le robot
        self.robot.move()
        
        # Détecter les collisions
        collision = self.environnement.detect_collision(self.robot)
        
        if collision:
            # Gérer la collision (arrêter le robot, etc.)
            self.robot.stop()
            return False
        
        # Mettre à jour l'environnement si nécessaire
        self.environnement.update(self.robot)
        
        return True

    def run(self, duration=30):
        """Lance la simulation pendant une durée donnée."""
        start_time = time.time()
        while time.time() - start_time < duration:
           if not self.updateModele():
                print("Collision détectée !")
                break
                time.sleep(0.1)

