import tkinter as tk
import time
import threading

from robot_simulation.controleur.controleur import Controleur
from robot_simulation.modele.simulation import Simulation

class AffichageGraphique:
    def __init__(self, master, simulation):
        """Initialise l'affichage graphique de la simulation."""
        self.master = master
        self.simulation = simulation
        self.robot = self.simulation.robot
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()
        # Stocker la trajectoire du robot
        self.trajet = []
        # Créer l'objet controleur
        self.controleur = Controleur(self.simulation)  # Contrôleur qui gère les mouvements
        self.controleur.faire_carre(100)  # Démarrer la simulation du carré
        # Indicateur pour contrôler l'exécution du thread
        self.running = True
        self.update_affichage()
        # Lancer le thread pour la mise à jour graphique
        self.thread = threading.Thread(target=self.update_affichage_thread)
        self.thread.daemon = True  # Le thread se ferme automatiquement lorsque la fenêtre se ferme
        self.thread.start()
        # Gérer la fermeture de la fenêtre pour arrêter proprement le thread
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_affichage(self):
        """Met à jour l'affichage graphique du robot en traçant sa trajectoire."""
        # Déplacer le robot
        self.robot.move(dt=0.1)

        # Ajouter la nouvelle position à la trajectoire
        x, y = self.robot.x, self.robot.y
        if len(self.trajet) > 0:
            prev_x, prev_y = self.trajet[-1]
            self.canvas.create_line(prev_x, prev_y, x, y, fill="black", width=2)  # 🔥 Traçage du chemin

        self.trajet.append((x, y))  # Sauvegarde des positions

        # Effacer uniquement le robot pour éviter d'effacer le chemin
        self.canvas.delete("robot")

        # Dessiner les obstacles
        for obs in self.simulation.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")

        # Dessiner le robot
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="robot")

        # Continuer la mise à jour après 50ms
        self.master.after(50, self.update_affichage)

    def update_affichage_thread(self):
        """Mise à jour graphique dans un thread séparé."""
        while self.running:
            time.sleep(0.05)  # Réduit la charge CPU, ne bloque pas l'interface

    def on_close(self):
        """Ferme la fenêtre et arrête proprement le thread."""
        self.running = False
        self.thread.join(timeout=1)  # Attendre que le thread se termine proprement
        self.master.destroy()
