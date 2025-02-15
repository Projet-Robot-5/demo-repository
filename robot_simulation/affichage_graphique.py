

import tkinter as tk
import math
from .simulation import Simulation
import threading
import time


class AffichageGraphique:
    def __init__(self, master):
        """Initialise l'affichage graphique de la simulation."""
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()

        self.simulation = Simulation()
        self.running = True # Indicateur pour controler l'execution du thread
        self.update_affichage()

        self.thread = threading.Thread(target=self.update_affichage_thread)
        self.thread.daemon = True #Le thread se ferme automatiquement quand la fenetre se ferme
        self.thread.start()
    
    
    def update_affichage(self):
        """Met à jour l'affichage graphique du robot sans interférer avec la simulation."""
        
        self.canvas.delete("all")

        # Dessiner les obstacles
        for obs in self.simulation.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")

        # Dessiner le robot
        x, y = self.simulation.robot.x, self.simulation.robot.y
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")
    
    def update_affichage_thread(self):
        """Mise à jour graphique dans un thread séparé"""
        while self.running:
            self.update_affichage() # met à jour les elements 
            self.master.after(50) # Met à jour toutes les 50ms
            time.sleep(0.05) # pour reduire la charge CPU et laisser de l'espace pour les autres taches

        


if __name__ == "__main__":
    root = tk.Tk()
    app = AffichageGraphique(root)
    root.mainloop()
