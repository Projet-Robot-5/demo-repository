import time
from robot_simulation import adaptateur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.environnement import Environnement
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
""""""
class Controleur:
    def __init__(self, adptateur):
        """ Initialise le contrôleur pour gérer les stratégies du robot.
        """
        self.adaptateur = adaptateur  # Instanciation de l'adaptateur
        self.queue_strategies = []
        self.strategie_courante = None
        self.running = True  # Variable pour contrôler la boucle

    def update(self):
        """
        Méthode appelée à chaque tick pour appliquer la stratégie courante.
        """
        if not self.running or not self.strategie_courante:
            return False

        # Applique un pas de la stratégie courante
        self.strategie_courante.step()

        # Passe à la stratégie suivante si nécessaire
        if self.strategie_courante.stop():
            if self.queue_strategies:
                self.strategie_courante = self.queue_strategies.pop(0)
                self.strategie_courante.start()
                return True
            else:
                self.running = False
                return False
        return True

    def set_strategie(self, strategie):
        """
        Définit la stratégie à exécuter.
        Args: strategie: Objet stratégie implémentant l'interface de stratégie
        """
        self.strategie_courante = strategie
        self.strategie_courante.start()
        self.running = True

    def ajouter_strategie(self, strategie):
        """Ajoute une stratégie à la file d'attente."""
        self.queue_strategies.append(strategie)

    def stop(self):
        """Arrête la simulation proprement."""
        self.running = False
        if self.strategie_courante:
            self.strategie_courante.stop()
