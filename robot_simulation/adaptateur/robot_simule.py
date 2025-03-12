# Importation des modules nécessaires
import math  # Utilisé pour les fonctions mathématiques, comme les calculs d'angle et de position
import time  # Utilisé pour gérer le temps (par exemple, mesurer le temps écoulé)

# Définition de la classe RobotSimule
class RobotSimule:
    
    def __init__(self, robot, x, y, direction_x, direction_y, environnement):
        """
        Constructeur de la classe RobotSimule.

        Paramètres :
        robot : objet de type Robot, représentant le robot réel ou simulé
        x, y : coordonnées initiales du robot dans l'environnement
        direction_x, direction_y : direction du robot dans l'environnement
        environnement : environnement dans lequel le robot évolue

        Attributs :
        angle_parcouru : initialisé à 0, représente l'angle de rotation du robot
        distance_parcouru : initialisé à 0, représente la distance totale parcourue
        temps_passe : le temps écoulé depuis le début de la simulation
        rayon_roue : rayon des roues du robot (10 unités par défaut)
        largeur : largeur entre les roues du robot (20 unités par défaut)
        """
        self.robot = robot  # Objet Robot réel ou simulé
        self.x = x  # Position x du robot
        self.y = y  # Position y du robot
        self.direction_x = direction_x  # Direction dans l'axe X
        self.direction_y = direction_y  # Direction dans l'axe Y
        self.environnement = environnement  # Environnement du robot

        self.angle_parcouru = 0  # Initialisation de l'angle parcouru (0° au départ)
        self.distance_parcouru = 0  # Initialisation de la distance parcourue (0 unité)
        self.temps_passe = time.time()  # Temps actuel à l'initialisation
        self.rayon_roue = 10  # Rayon des roues (par défaut à 10 unités)
        self.largeur = 20  # Largeur entre les roues du robot (par défaut à 20 unités)

    def set_vitesse(self, vitesse_gauche, vitesse_droite):
        """
        Définit les vitesses des roues gauche et droite du robot.

        Paramètres :
        vitesse_gauche : vitesse de la roue gauche
        vitesse_droite : vitesse de la roue droite
        """
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)

    def update_temps_passe(self):
        """
        Met à jour le temps écoulé depuis la dernière mise à jour.

        Retour :
        temps_passe : le temps écoulé depuis la dernière mise à jour (en secondes)
        """
        temps_actuel = time.time()  # Temps actuel
        temps_passe = temps_actuel - self.temps_passe  # Temps écoulé
        self.temps_passe = temps_actuel  # Mise à jour du temps de référence
        return temps_passe

    def update_position(self):
        """
        Met à jour la position du robot en fonction des vitesses des roues.

        Calculs :
        - Vitesse moyenne des roues (moyenne des vitesses gauche et droite)
        - Calcul de la nouvelle position (x, y) en fonction de l'angle parcouru
        - Calcul de la rotation du robot en fonction des vitesses des roues
        """
        vitesse_moyenne = (self.robot.vitesse_gauche + self.robot.vitesse_droite) / 2
        angle_rad = math.radians(self.angle_parcouru)  # Conversion de l'angle en radians

        # Calcul de la nouvelle position
        self.x += vitesse_moyenne * math.cos(angle_rad) * 0.1  # 0.1 est le pas de temps (100ms)
        self.y += vitesse_moyenne * math.sin(angle_rad) * 0.1

        # Si les roues ne tournent pas à la même vitesse, le robot tourne
        if self.robot.vitesse_gauche != self.robot.vitesse_droite:
            rotation_vitesse = (self.robot.vitesse_droite - self.robot.vitesse_gauche) / self.largeur
            self.angle_parcouru += math.degrees(rotation_vitesse * 0.1)  # Mise à jour de l'angle en fonction de la vitesse de rotation
            self.angle_parcouru = self.angle_parcouru % 360  # Normalisation de l'angle entre 0° et 360°

    def calcul_rotation(self, distance_gauche, distance_droite):
        """
        Calcule l'angle de rotation du robot en fonction de la distance parcourue par chaque roue.

        Paramètres :
        distance_gauche : distance parcourue par la roue gauche
        distance_droite : distance parcourue par la roue droite

        Retour :
        L'angle de rotation du robot (en degrés)
        """
        difference_distance = distance_droite - distance_gauche
        angle_rotation_rad = difference_distance / self.largeur  # Calcul de l'angle en radians
        return math.degrees(angle_rotation_rad)  # Conversion en degrés

    def get_distance(self):
        """
        Retourne la distance totale parcourue par le robot.

        Retour :
        La distance parcourue (en unités)
        """
        return self.distance_parcouru

    def get_position(self):
        """
        Retourne la position actuelle du robot (coordonnées x, y).

        Retour :
        Tuple contenant les coordonnées (x, y)
        """
        return self.x, self.y

    def reset(self):
        """
        Réinitialise la position et l'orientation du robot.

        Remarque :
        Si le robot réel a une méthode de réinitialisation, elle est appelée ici.
        """
        self.x = 0  # Réinitialisation de la position x
        self.y = 0  # Réinitialisation de la position y
        self.angle_parcouru = 0  # Réinitialisation de l'angle
        self.distance_parcouru = 0  # Réinitialisation de la distance parcourue
        self.robot.reset()  # Si le robot réel a une méthode de réinitialisation, elle est appelée ici

    def detection_obstacle(self):
        """
        Détecte la présence d'obstacles dans l'environnement.

        Retour :
        La distance à l'obstacle (cette méthode devrait être définie dans la classe Robot)
        """
        return self.robot.get_distance()  # Cette méthode doit être définie dans la classe `Robot` ou une classe héritée

    def afficher_info(self):
        """
        Affiche les informations de position et d'orientation du robot.

        Affiche :
        - La position actuelle du robot
        - L'angle d'orientation du robot
        """
        print(f"Position du robot : ({self.x}, {self.y}), Orientation : {self.angle_parcouru}°")
