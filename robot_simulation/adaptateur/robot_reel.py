import time

class RobotReel:
    def __init__(self, robot):
        """Initialisation du robot réel en utilisant les API de contrôle matériel."""
        self.robot = robot
        self.initialiser_materiel()
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
        self.dernier_temps = time.time()
        self.distance_restante = 1000  # Distance estimée au mur en mm/cm


    def initialiser_materiel(self):
        """Initialise les moteurs et les capteurs du robot réel."""
        print("Initialisation du matériel réel...")

    def set_motor_dps(self, moteur_gauche_dps, moteur_droite_dps):
        """Contrôle les moteurs en définissant leur vitesse en degrés par seconde (DPS)."""
        self.vitesse_gauche = moteur_gauche_dps  # Enregistre la vitesse gauche pour le suivi de distance
        self.vitesse_droite = moteur_droite_dps  # Enregistre la vitesse droite pour le suivi de distance
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

    def stop(self):
        """Arrête le robot en mettant les moteurs à 0."""
        print("Arrêt du robot réel.")
        self.set_motor_dps(0, 0)

    def get_sensor_data(self):
        """Récupère les données des capteurs (ex: distance, obstacles, etc.)."""
        # Exemple de récupération de données capteurs
        return {"distance_obstacle": 50}  # Ex: renvoie une distance de 50 cm

    
    def get_distance_devant(self):
        # Récupère l'heure actuelle
        maintenant = time.time()

        # Calcule le temps écoulé depuis le dernier appel
        temps_ecoule = maintenant - self.dernier_temps

        # Met à jour le dernier temps enregistré
        self.dernier_temps = maintenant

        # Calcule la vitesse moyenne des deux roues
        vitesse_moyenne = (self.vitesse_gauche + self.vitesse_droite) / 2  # en DPS

        # Conversion fictive de DPS vers cm/s (à adapter selon le matériel réel)
        conversion_cm_par_dps = 0.05
        vitesse_cm_s = vitesse_moyenne * conversion_cm_par_dps

        # Distance parcourue pendant le temps écoulé
        distance_parcourue = vitesse_cm_s * temps_ecoule

        # Mise à jour de la distance restante simulée devant le robot
        self.distance_restante -= distance_parcourue

        # Retourne la distance actuelle devant (jamais négative)
        return max(self.distance_restante, 0)

    
    def tourner(self, angle):
        """Fait tourner le robot d'un certain angle en degrés."""
        print(f"Rotation de {angle} degrés...")
        vitesse_rotation = 100  # Exemple de vitesse de rotation en DPS
        temps_rotation = abs(angle) / vitesse_rotation
        direction = 1 if angle > 0 else -1
        self.set_motor_dps(direction * vitesse_rotation, -direction * vitesse_rotation)
        time.sleep(temps_rotation)
        self.stop()

    def avancer(self, distance):
        """Fait avancer le robot d'une certaine distance en cm."""
        print(f"Avancement de {distance} cm...")
        vitesse_translation = 200  # Exemple de vitesse de translation en DPS
        temps_translation = abs(distance) / 10  # Supposons 10 cm/s
        self.set_motor_dps(vitesse_translation, vitesse_translation)
        time.sleep(temps_translation)
        self.stop()

