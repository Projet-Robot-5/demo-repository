import time
from robot_simulation import adaptateur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.environnement import Environnement
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule

class Controleur:
    def __init__(self, adaptateur):
        """
        Initialise le contrôleur pour gérer les stratégies du robot.
        """
        self.adaptateur = adaptateur
        self.queue_strategies = []          # File des stratégies à exécuter
        self.strategie_courante = None      # Stratégie en cours
        self.running = False                # Indique si l'exécution est en cours

    def update(self):
        """
        Méthode appelée à chaque tick pour appliquer la stratégie courante.
        Retourne False si aucune stratégie n’est en cours.
        """
        if not self.running or self.strategie_courante is None:
            return False

        # Met à jour la position physique simulée
        if hasattr(self.adaptateur, "update_position"):
            self.adaptateur.update_position(0.05)

        # Exécute une étape de la stratégie actuelle
        self.strategie_courante.step()

        # Si la stratégie est terminée
        if self.strategie_courante.stop():
            print(f"[CONTROLEUR] Fin stratégie : {type(self.strategie_courante).__name__}")
            # Passer à la stratégie suivante s’il y en a
            if self.queue_strategies:
                self.strategie_courante = self.queue_strategies.pop(0)
                print(f"[CONTROLEUR] Lancement de : {type(self.strategie_courante).__name__}")
                self.strategie_courante.start()
            else:
                print("[CONTROLEUR] Aucune autre stratégie, arrêt.")
                self.running = False
        return True

    def set_strategie(self, strategie):
        """
        Définit la stratégie principale à exécuter.
        :param strategie: objet stratégie (doit avoir start, step, stop)
        """
        self.strategie_courante = strategie
        self.strategie_courante.start()
        self.running = True
        print(f"[CONTROLEUR] Stratégie définie : {type(strategie).__name__}")

    def ajouter_strategie(self, strategie):
        """
        Ajoute une stratégie à la file d'attente (sera exécutée après la courante).
        """
        self.queue_strategies.append(strategie)
        print(f"[CONTROLEUR] Stratégie ajoutée en file : {type(strategie).__name__}")

    def stop(self):
        """
        Arrête toute exécution de stratégie.
        """
        print("[CONTROLEUR] Arrêt manuel du contrôleur.")
        self.running = False
        if self.strategie_courante:
            self.strategie_courante.stop()
