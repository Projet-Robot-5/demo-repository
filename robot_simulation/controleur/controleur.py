import time
from robot_simulation.controleur.strategie import StrategieCarre
from robot_simulation.modele.environnement import Environnement
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule

class Controleur:
    def __init__(self, robot, mode=None, master=None):
        """
        Initialise le contrôleur pour gérer les stratégies du robot.

        :param robot: L'objet robot qui sera contrôlé.
        :param mode: Le mode d'affichage ("graphique" ou None).
        :param master: La fenêtre principale tkinter (pour le mode graphique).
        """
        self.adaptateur = AdaptateurRobotSimule(robot)  # Instanciation de l'adaptateur
        self.environnement = Environnement(width=500, height=500, obstacle_count=15)
        self.mode = mode
        self.queue_strategies = []
        self.strategie_courante = None
        self.master = master
        self.running = True  # Variable pour contrôler la boucle

    def run(self):
        """Démarrer la simulation en exécutant les stratégies."""
        if self.mode == "graphique" and self.master:
            from robot_simulation.affichage.affichage_graphique import AffichageGraphique
            self.affichage = AffichageGraphique(self.master, self.adaptateur, self)

        # Démarrer la stratégie du carré
        self.strategie_courante = StrategieCarre(self.adaptateur)
        self.ajouter_strategie(self.strategie_courante)
        self.step()

    def step(self):
        """Exécute la stratégie actuelle et passe à la suivante si elle est terminée."""
        if not self.running:
            return  # Stopper la simulation si demandé
        
        if self.strategie_courante is None or self.strategie_courante.stop():
            if self.queue_strategies:
                self.strategie_courante = self.queue_strategies.pop(0)
                self.strategie_courante.start()
            else:
                print("Toutes les stratégies sont terminées.")
                self.running = False  # Arrêter la simulation après exécution

        if self.strategie_courante:
            self.strategie_courante.step()

        # Met à jour seulement en mode graphique
        if self.mode == "graphique" and self.master:
            self.master.after(100, self.step)
        else:
            time.sleep(0.1)
            self.step()

    def ajouter_strategie(self, strategie):
        """Ajoute une stratégie à la file d'attente."""
        self.queue_strategies.append(strategie)

    def stop(self):
        """Arrête la simulation proprement."""
        self.running = False