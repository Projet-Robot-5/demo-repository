import tkinter as tk
import math
from .simulation import Simulation
import threading
import time
from robot_simulation.controleur import Controleur

class AffichageGraphique:
    def __init__(self, master, robot):
        """Initialise l'affichage graphique de la simulation."""
        self.master = master
        self.robot = robot
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()

        self.simulation = Simulation()
        self.controleur = Controleur(self.simulation.robot)  # Contrôleur qui gère les mouvements
        self.controleur.faire_carre(100)  # Démarrer le carré
        self.running = True  # Indicateur pour contrôler l'exécution du thread
        self.update_affichage()

        self.thread = threading.Thread(target=self.update_affichage_thread)
        self.thread.daemon = True  # Le thread se ferme automatiquement quand la fenêtre se ferme
        self.thread.start()

        # Gérer la fermeture de la fenêtre pour arrêter proprement le thread
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Assurez-vous que self.on_close est appelé ici

    def show(self):
        """Cette méthode va démarrer le mainloop de Tkinter pour l'affichage."""
        self.master.mainloop()
    
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
            self.update_affichage()  # met à jour les éléments
            self.controleur.step()  # Exécuter les stratégies en arrière-plan
            self.simulation.update_all()
            self.master.after(50, self.update_affichage)  # Mise à jour toutes les 50ms
            time.sleep(0.05)  # pour réduire la charge CPU et laisser de l'espace pour les autres tâches

    def on_close(self):
        """Ferme la fenêtre et arrête proprement le thread."""
        self.running = False
        self.thread.join(timeout=1)  # Attendre que le thread se termine proprement
        self.master.destroy()  # Ferme la fenêtre Tkinter proprement
