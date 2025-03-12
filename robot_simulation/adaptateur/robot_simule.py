import math
import time

class RobotSimule:

    def __init__(self, robot, x, y, direction_x, direction_y, environnement):
        self.robot = robot  # Robot réel ou simulé
        self.x = x  # Position x du robot
        self.y = y  # Position y du robot
        self.direction_x = direction_x  # Direction dans l'axe X
        self.direction_y = direction_y  # Direction dans l'axe Y
        self.environnement = environnement  # Environnement dans lequel le robot évolue

        self.angle_parcouru = 0  # Angle du robot, initialisé à 0
        self.distance_parcouru = 0  # Distance parcourue par le robot, initialisée à 0
        self.temps_passe = time.time()  # Temps initial
        self.rayon_roue = 10  # Rayon des roues (par exemple, 10 unités)
        self.largeur = 20  # Largeur entre les roues du robot, exemple : 20 unités

    def set_vitesse(self, vitesse_gauche, vitesse_droite):
        """Définit les vitesses des roues gauche et droite du robot."""
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)

    def update_temps_passe(self):
        """Mise à jour du temps passé depuis la dernière mise à jour."""
        temps_actuel = time.time()
        temps_passe = temps_actuel - self.temps_passe
        self.temps_passe = temps_actuel
        return temps_passe

    def update_position(self):
        """Mise à jour de la position du robot en fonction des vitesses des roues."""
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        angle_rad = math.radians(self.angle_parcouru)

        # Calcul de la position du robot
        self.x += vitesse_moyenne * math.cos(angle_rad) * 0.1  # dt=0.1 pour 100ms
        self.y += vitesse_moyenne * math.sin(angle_rad) * 0.1

        # Calcul de la rotation en fonction des vitesses des roues
        if self.robot.vitesse_gauche != self.robot.vitesse_droite:
            rotation_vitesse = (self.robot.vitesse_droite - self.robot.vitesse_gauche) / self.largeur
            self.angle_parcouru += math.degrees(rotation_vitesse * 0.1)  # Mise à jour en fonction de dt
            self.angle_parcouru = self.angle_parcouru % 360  # Normalisation de l'angle entre 0 et 360

    def calcul_rotation(self, distance_gauche, distance_droite):
        """Calcule l'angle de rotation du robot en fonction de la distance parcourue par chaque roue."""
        difference_distance = distance_droite - distance_gauche
        angle_rotation_rad = difference_distance / self.largeur
        return math.degrees(angle_rotation_rad)

    def get_distance(self):
        """Retourne la distance totale parcourue par le robot."""
        return self.distance_parcouru

    def get_position(self):
        """Retourne la position actuelle du robot."""
        return self.x, self.y

    def reset(self):
        """Réinitialise la position et l'orientation du robot."""
        self.x = 0
        self.y = 0
        self.angle_parcouru = 0
        self.distance_parcouru = 0
        self.robot.reset()  # Si le robot réel a une méthode de reset, l'appeler ici

    def detection_obstacle(self):
        """Détecte la présence d'obstacles dans l'environnement."""
        return self.robot.get_distance()  # Cette méthode doit être définie dans la classe `Robot` ou une classe héritée

    def afficher_info(self):
        """Affiche les informations de position et d'orientation du robot."""
        print(f"Position du robot : ({self.x}, {self.y}), Orientation : {self.angle_parcouru}°")
