import time
import math
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot

class Simulation:
    def __init__(self, master=None):
        """Initialise la simulation, gère l'environnement et le robot"""
        self.environnement = Environnement(width=500, height=500, obstacle_count=3)
        self.robot = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)
        self.robot_chat = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)
        self.robot_souris = Robot(x=250, y=250, vitesse_gauche=10, vitesse_droite=10)

    def updateModele(self):
       
        # Faire bouger le robot
        self.robot_chat.move()
        self.robot_souris.move()
        # Détecter les collisions
        attrape = self.environnement.chat_attrape_souris(self.robot_chat,self.robot_souris)
        
        if attrape:
            # Gérer la collision (arrêter le robot, etc.)
            self.robot_chat.stop()
            self.robot_souris.stop()
            return False
        
        return True

    def run(self, duration=30):
        """Lance la simulation pendant une durée donnée."""
        start_time = time.time()
        while time.time() - start_time < duration:
           if not self.updateModele():
                print("Collision détectée !")
                break
                time.sleep(0.1)

