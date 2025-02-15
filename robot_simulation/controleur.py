import time

class Controleur:
    def __init__(self, robot, mode=None, master=None):
        self.robot = robot
        self.mode = mode  # Ajouter un mode, avec une valeur par défaut None
        self.queue_strategies = []  # Liste des stratégies à exécuter
        self.strategie_courante = None  # La stratégie en cours
        self.master = master
