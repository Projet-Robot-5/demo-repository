import time

class Controleur:
    def __init__(self, robot, mode=None, master=None):
        self.robot = robot
        self.mode = mode  # Ajouter un mode, avec une valeur par défaut None
        self.queue_strategies = []  # Liste des stratégies à exécuter
        self.strategie_courante = None  # La stratégie en cours
        self.master = master
    def run(self, duration=30):
        """Démarrer la simulation."""
        if self.mode == "graphique" and self.master:
            from robot_simulation.affichage_graphique import AffichageGraphique
            self.affichage = AffichageGraphique(self.master, self.robot)
        
        self.faire_carre()  # Commencer le mouvement en carré
        self.step()
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
class AvancerDroit:
    def __init__(self, robot, distance):
        self.robot = robot
        self.distance = distance
        self.distance_parcourue = 0
    
    def start(self):
        """Démarre la stratégie d'avance."""
        self.distance_parcourue = 0
        self.robot.set_wheel_speed(10, 10)  # Vitesse constante pour avancer
        print("Début de l'avance droite")

    def step(self):
        """Fait avancer le robot d'une petite étape."""
        self.robot.move(dt=1)  # Le robot avance d'une petite unité
        self.distance_parcourue += 10  # On ajuste la distance parcourue
        print(f"Avance droite: {self.distance_parcourue}/{self.distance}")

    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        return self.distance_parcourue >= self.distance
    
class Tourner:
    def __init__(self, robot, angle):
        self.robot = robot
        self.angle = angle
        self.angle_tourne = 0

    def start(self):
        """Démarre la rotation."""
        self.angle_tourne = 0
        self.robot.set_wheel_speed(5, -5)  # Roues opposées pour tourner sur place
        print("Début de la rotation")
    def step(self):
        """Effectue la rotation par petites étapes."""
        self.robot.move(dt=0.1)  # Le robot tourne
        self.angle_tourne += 5  # Rotation de 5° à chaque étape (ajustable)
        print(f"Rotation: {self.angle_tourne}/{self.angle}")
    def stop(self):
        """Retourne vrai si la rotation est terminée."""
        return self.angle_tourne >= self.angle



