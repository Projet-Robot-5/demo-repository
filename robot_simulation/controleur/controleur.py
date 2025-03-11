import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.modele.environnement import Environnement


class Controleur:
    def __init__(self, simulation, mode=None, master=None):
        self.simulation = simulation  # Stocke l'objet simulation
        self.robot = self.simulation.robot
        self.environnement = Environnement(self.robot)  # Associer l'environnement au robot
        self.mode = mode  # Ajouter un mode, avec une valeur par défaut None
        self.queue_strategies = []  # Liste des stratégies à exécuter
        self.strategie_courante = None  # La stratégie en cours
        self.master = master
    
    def run(self, duration=30):
        """Démarrer la simulation."""
        if self.mode == "graphique" and self.master:
            from robot_simulation.affichage.affichage_graphique import AffichageGraphique
            self.affichage = AffichageGraphique(self.master, self.simulation)
        
        self.faire_carre()  # Commencer le mouvement en carré
        self.step()
    
    def step(self):
        """Exécute la stratégie actuelle et passe à la suivante si elle est terminée."""
        if self.strategie_courante is None or self.strategie_courante.stop():
            if self.queue_strategies:
                self.strategie_courante = self.queue_strategies.pop(0)
                self.strategie_courante.start()
            else:
                return  # Plus rien à exécuter

        if self.strategie_courante:
            self.strategie_courante.step()
            self.environnement.mettre_a_jour(dt=1)  # Mise à jour du robot via l'environnement

        if self.environnement.detecter_collision():
            print("Simulation arrêtée à cause d'une collision.")
            return

        if self.mode == "graphique" and self.master:
            self.master.after(100, self.step)  # Met à jour toutes les 100ms
        else:
            time.sleep(0.1)
            self.step()
    
    def faire_carre(self, cote=120):
        """Ajoute les stratégies pour faire un carré."""
        for _ in range(4):
            avancer = AvancerDroit(self.robot, cote)
            tourner = Tourner(self.robot, 90)  # Correction pour assurer un carré parfait
            self.ajouter_strategie(avancer)
            self.ajouter_strategie(tourner)
    
    def ajouter_strategie(self, strategie):
        """Ajoute une stratégie à la file d'attente."""
        self.queue_strategies.append(strategie)

