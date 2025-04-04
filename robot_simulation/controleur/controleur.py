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
        self.last_update_time = time.time()  # Initialiser le temps de mise à jour
    def update(self):
        """Méthode appelée à chaque tick pour appliquer la stratégie courante."""
        if not self.running or not self.strategie_courante:
            return False

        # Calcul du delta temps (dt) entre la mise à jour actuelle et la dernière
        current_time = time.time()
        dt = current_time - self.last_update_time  # Delta temps écoulé

        # Applique un pas de la stratégie courante en passant le dt
        self.strategie_courante.step(dt)

        # Mettre à jour le temps de la dernière mise à jour
        self.last_update_time = current_time

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