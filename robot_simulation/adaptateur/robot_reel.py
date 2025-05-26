import time

class RobotReel:
    def __init__(self, robot):
        self.robot = robot
        self.initialiser_materiel()
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
        self.dernier_temps = time.time()
        self.distance_restante = 1000
        self.x = 0
        self.y = 0
        self.orientation = 0

    def initialiser_materiel(self):
        print("Initialisation du matériel réel...")

    def set_motor_dps(self, moteur_gauche_dps, moteur_droite_dps):
        self.vitesse_gauche = moteur_gauche_dps
        self.vitesse_droite = moteur_droite_dps
        print(f"Commande moteur - Gauche: {moteur_gauche_dps} DPS, Droite: {moteur_droite_dps} DPS")

    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        conversion_dps = 20
        moteur_gauche_dps = vitesse_gauche * conversion_dps
        moteur_droite_dps = vitesse_droite * conversion_dps
        self.set_motor_dps(moteur_gauche_dps, moteur_droite_dps)

    def move(self, dt=0.1):
        print("Déplacement en cours...")
        time.sleep(dt)

    def stop(self):
        print("Arrêt du robot réel.")
        self.set_motor_dps(0, 0)

    def get_sensor_data(self):
        return {"distance_obstacle": 50}

    def get_distance_devant(self):
        try:
            donnees = self.get_sensor_data()
            distance_cm = donnees.get("distance_obstacle", -1)
            return round(distance_cm, 2)
        except Exception as e:
            print(f"[ERREUR capteur IR] {e}")
            return -1

    def tourner(self, angle):
        print(f"Rotation de {angle} degrés...")
        vitesse_rotation = 100
        temps_rotation = abs(angle) / vitesse_rotation
        direction = 1 if angle > 0 else -1
        self.set_motor_dps(direction * vitesse_rotation, -direction * vitesse_rotation)
        time.sleep(temps_rotation)
        self.stop()
        # Mettre à jour orientation ici si possible

    def avancer(self, distance):
        print(f"Avancement de {distance} cm...")
        vitesse_translation = 200
        temps_translation = abs(distance) / 10
        self.set_motor_dps(vitesse_translation, vitesse_translation)
        time.sleep(temps_translation)
        self.stop()
        # Mettre à jour position ici si possible

    def get_distance_parcourue(self):
        maintenant = time.time()
        temps_ecoule = maintenant - self.dernier_temps
        self.dernier_temps = maintenant
        vitesse_moyenne_dps = (self.vitesse_gauche + self.vitesse_droite) / 2
        conversion_cm_par_dps = 0.05
        vitesse_cm_s = vitesse_moyenne_dps * conversion_cm_par_dps
        return vitesse_cm_s * temps_ecoule
