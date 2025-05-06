import math
import time

class RobotSimule:
    def __init__(self, robot):
        """
        Constructeur du robot simulé.
        :param robot: Instance de la classe Robot (le modèle réel ou simulé)
        """
        self.robot = robot
        self.rayon_roue = 10
        self.largeur = 20

    def set_vitesse(self, vitesse_gauche, vitesse_droite):
        """
        Définit les vitesses des deux roues.
        """
        self.robot.set_wheel_speed(vitesse_gauche, vitesse_droite)

    def update_temps_passe(self):
        """
        Met à jour le temps écoulé depuis la dernière mise à jour.
        """
        if not hasattr(self.robot, "temps_passe"):
            self.robot.temps_passe = time.time()
        temps_actuel = time.time()
        temps_passe = temps_actuel - self.robot.temps_passe
        self.robot.temps_passe = temps_actuel
        return temps_passe

    def calcul_rotation(self, distance_gauche, distance_droite):
        """
        Calcule l'angle de rotation du robot en degrés.
        """
        delta_distance = distance_droite - distance_gauche
        angle_rad = delta_distance / self.largeur
        return math.degrees(angle_rad)

    def get_distance(self):
        """
        Retourne la distance totale parcourue par le robot.
        """
        return self.robot.get_distance_parcourue()

    def get_position(self):
        """
        Retourne la position actuelle du robot.
        """
        return self.robot.get_position()

    def reset(self):
        """
        Réinitialise le robot (à adapter si nécessaire).
        """
        self.robot.x = 0
        self.robot.y = 0
        self.robot.orientation = 0

    def detection_obstacle(self):
        """
        Renvoie une distance simulée au prochain obstacle.
        """
        if hasattr(self.robot, "get_distance_devant"):
            return self.robot.get_distance_devant(self.robot.environnement.obstacles)
        return -1

    def afficher_info(self):
        """
        Affiche les infos du robot.
        """
        x, y = self.get_position()
        orientation = self.robot.get_orientation()
        print(f"Position du robot : ({x:.1f}, {y:.1f}), Orientation : {orientation:.1f}°")

    def get_distance_devant(self, obstacles):
        """
        Utilise la méthode du robot pour détecter les obstacles devant lui.
        """
        return self.robot.get_distance_devant(obstacles)
