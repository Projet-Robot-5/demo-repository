
import math  # Utilisé pour les fonctions mathématiques, comme les calculs d'angle et de position
import time  # Utilisé pour gérer le temps (par exemple, mesurer le temps écoulé)

# Définition de la classe RobotSimule
class RobotSimule:
    
    def __init__(self, robot):
        """
        Constructeur de la classe RobotSimule.

        Paramètres :
        - robot : instance du robot simulé
        """
        self.robot = robot  # Objet Robot réel ou simulé
        self.angle_parcouru = 0  # Initialisation de l'angle parcouru (0° au départ)
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
        temps_passe = temps_actuel - self.robot.temps_passe  # Temps écoulé
        self.robot.temps_passe = temps_actuel  # Mise à jour du temps de référence
        return temps_passe


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
        return self.robot.distance_parcouru

    def get_position(self):
        """
        Retourne la position actuelle du robot (coordonnées x, y).

        Retour :
        Tuple contenant les coordonnées (x, y)
        """
        return self.robot.x, self.robot.y

    def reset(self):
        """Réinitialise le robot."""
        self.robot.reset()
        
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
