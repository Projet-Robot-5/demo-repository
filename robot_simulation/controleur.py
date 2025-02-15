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
    def step(self):
        """Exécute la stratégie actuelle et passe à la suivante si elle est terminée."""
        if self.strategie_courante is None or self.strategie_courante.stop():
            if self.queue_strategies:
                self.strategie_courante = self.queue_strategies.pop(0)
                self.strategie_courante.start()
            else:
                # Si toutes les stratégies sont terminées, recommencer le carré
                self.faire_carre(100)

        if self.strategie_courante:
            self.strategie_courante.step()
    def faire_carre(self, cote=100):
        """Ajoute les stratégies pour faire un carré."""
        for _ in range(4):
            self.ajouter_strategie(AvancerDroit(self.robot, cote))
            self.ajouter_strategie(Tourner(self.robot, 90))
    def ajouter_strategie(self, strategie):
        """Ajoute une stratégie à la file d'attente."""
        self.queue_strategies.append(strategie)

