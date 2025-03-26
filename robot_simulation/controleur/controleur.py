import time
from robot_simulation.controleur.strategie import AvancerDroit, Tourner
from robot_simulation.modele.environnement import Environnement
from robot_simulation.controleur.strategie import StrategieCarre


class Controleur:
    def __init__(self, robot, mode=None, master=None):
        """Initialise le contrôleur pour gérer les stratégies du robot et l'environnement.
        
        :param robot: L'objet robot qui sera contrôlé par le contrôleur.
        :param mode: Le mode d'affichage (par défaut, il est None).
        :param master: La fenêtre principale tkinter (utilisée dans le mode graphique).
        """
        
        self.robot = robot
        self.environnement = Environnement(robot=self.robot,width=500, height=500, obstacle_count=15)  # Associer l'environnement au robot
        self.mode = mode  # Ajouter un mode, avec une valeur par défaut None
        self.queue_strategies = []  # Liste des stratégies à exécuter
        self.strategie_courante = None  # La stratégie en cours
        self.master = master
    
    def run(self, duration=30):
        """Démarrer la simulation.
        :param duration: Durée de la simulation (en secondes, non utilisée ici directement).
        """
        # Si on est en mode graphique, on initialise l'affichage avec la classe AffichageGraphique"""
        if self.mode == "graphique" and self.master:
            from robot_simulation.affichage.affichage_graphique import AffichageGraphique
            self.affichage = AffichageGraphique(self.master, self.robot,self)
        
        # Utilisation de la stratégie carré au lieu de faire_carre()
        self.strategie_courante = StrategieCarre(self.robot)
        self.ajouter_strategie(self.strategie_courante)   # Ajout de la stratégie à la queue
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
            self.strategie_courante.step()  # Exécution de la stratégie actuelle

            if self.strategie_courante.stop():  # Vérifie si la stratégie est terminée
                self.environnement.mettre_a_jour(dt=1)  # Mise à jour de l'environnement après l'étape

        

        if self.mode == "graphique" and self.master:
            self.master.after(100, self.step)  # Met à jour toutes les 100ms
        else:
            time.sleep(0.1)
            self.step()
    

    
    def ajouter_strategie(self, strategie):
        """Ajoute une stratégie à la file d'attente."""
        self.queue_strategies.append(strategie)
    
    def stop(self):
        """Arrête la simulation proprement."""
        self.running = False