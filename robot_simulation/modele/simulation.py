import time
import math
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot

class Simulation:
    def __init__(self, master=None):
        """Initialise la simulation, gère l'environnement et le robot"""
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)
        self.master = master

    def update_all(self):
        """Met à jour l'état du robot et de l'environnement à chaque itération"""
        self.robot.move(dt=0.1)  # Mise à jour de la position du robot
        self.environnement.detect_obstacle(self.robot)  # Vérifie les collisions

        # Détecte si le robot percute un mur
        if self.robot.x < 20 or self.robot.x > self.environnement.width - 20 or \
           self.robot.y < 20 or self.robot.y > self.environnement.height - 20:
            print("Collision avec un mur ! Le robot s'arrête.")
            return

        # Afficher la position du robot en mode console (utile pour le mode terminal)
        print(f"Position du robot: ({self.robot.x:.2f}, {self.robot.y:.2f})")

        return True
    def run(self, duration=30):
        """Lance la simulation pendant une durée donnée."""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.updateModele()
            time.sleep(0.1)


        # Si on utilise une interface graphique, on continue l'update
        if self.master:
            self.master.after(50, self.update_all)  # Répète l'update toutes les 50ms

