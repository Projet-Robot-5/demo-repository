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

    
    def run(self, duration=30):
        """Lance la simulation pendant une durée donnée."""
        start_time = time.time()
        while time.time() - start_time < duration:
            self.updateModele()
            time.sleep(0.1)


        # Si on utilise une interface graphique, on continue l'update
        if self.master:
            self.master.after(50, self.update_all)  # Répète l'update toutes les 50ms

