import time

class Controleur:
    def __init__(self, robot, mode=None, master=None):
        self.robot = robot
        self.mode = mode  # Ajouter un mode, avec une valeur par défaut None
        self.queue_strategies = []  # Liste des stratégies à exécuter
        self.strategie_courante = None  # La stratégie en cours
        self.master = master
    def run(self, duration=10):
        """Méthode pour lancer la simulation."""
        if self.mode == "graphique":
            from .affichage_graphique import AffichageGraphique
            affichage = AffichageGraphique(self.master, self.robot)
        else:
            # Logique pour le mode terminal
            pass
        
        # Démarre l'exécution des stratégies
        self.faire_carre(100)
        self.step()  # Commence à exécuter les étapes des stratégies
