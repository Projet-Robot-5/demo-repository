import time
import tkinter as tk
from affichage_graphique import AffichageGraphique
from simulation import Simulation

class Controleur:
    """Gère la simulation en mode graphique et en mode terminal."""
    
    def __init__(self, mode="terminal"):
        """Initialise le contrôleur avec une instance de simulation."""
        self.simulation = Simulation()
        self.mode = mode
        self.root = None 
    def detect_wall_collision(self):
        """Détecte si le robot est trop près d'un mur."""
        margin = 20 #définir la marge de sécurité pour eviter les collisions avec les murs
        return (
            self.robot.x < margin or self.robot.x > self.environnement.width - margin or self.robot.y < margin or self.robot.y > self.environnement.height - margin )
    def update(self):
        """Met à jour le modèle de simulation (robot + environnement)."""
        #verifie d'abord si le robot est en collision avec un obstacle ou un mur
        if not self.simulation.updateModele(): #Apller la methode updateModele de simulation
            return False
        if self.detect_wall_collision():
            print("Collision avec un mur!")
            return False
        return True # Si aucune collision, la simulation continue
        
    def lancer_simulation_sans_AG(self):
        """Exécuter la simulation en mode terminal (sans interface graphique)."""
        print("Mode terminal activé.")
        while True:
            if not self.update():
                choix = input("Simulation terminée. Recommencer ? (o/n) : ")
                if choix.lower() == 'o':
                    self.simulation = Simulation()  # Réinitialiser la simulation
                else:
                    break
            time.sleep(0.1)

    def lancer_simulation_avec_AG(self):
        """Lancer l'affichage graphique de la simulation."""
        self.root = tk.Tk()
        self.root.title("Simulation de Robot")
        affichage = AffichageGraphique(self.root, self.simulation)  # On passe la simulation existante

        def on_close():
            """Si on ferme la fenêtre graphique, on passe en mode terminal."""
            print("\nFermeture de l'interface graphique. Passage en mode terminal...\n")
            self.root.destroy()
            self.lancer_simulation_sans_AG()

        self.root.protocol("WM_DELETE_WINDOW", on_close)  # Capture la fermeture de la fenêtre
        self.root.mainloop()
