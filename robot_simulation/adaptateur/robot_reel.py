import time

class RobotReel:
    def __init__(self, robot):
        """Initialisation du robot réel en utilisant les API de contrôle matériel."""
        self.robot = robot
        self.initialiser_materiel()

    def initialiser_materiel(self):
        """Initialise les moteurs et les capteurs du robot réel."""
        print("Initialisation du matériel réel...")

    def set_motor_dps(self, moteur_gauche_dps, moteur_droite_dps):
        """Contrôle les moteurs en définissant leur vitesse en degrés par seconde (DPS)."""
        print(f"Commande moteur - Gauche: {moteur_gauche_dps} DPS, Droite: {moteur_droite_dps} DPS")
        # Ici, on enverrait la commande aux moteurs via une bibliothèque matérielle

    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        """Convertit une vitesse linéaire en commande moteur et envoie aux moteurs."""
        # Supposons une conversion simplifiée entre vitesse linéaire et DPS
        conversion_dps = 20  # Exemple : 1 unité de vitesse correspond à 20 DPS
        moteur_gauche_dps = vitesse_gauche * conversion_dps
        moteur_droite_dps = vitesse_droite * conversion_dps
        self.set_motor_dps(moteur_gauche_dps, moteur_droite_dps)

    def move(self, dt=0.1):
        """Fait avancer le robot pendant dt secondes."""
        print("Déplacement en cours...")
        time.sleep(dt)  # Simulation du mouvement