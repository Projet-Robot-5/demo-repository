import math
import time

class RobotSimule:
    def __init__(self):
        # Position (x,y) en cm et orientation en degrés
        self.x = 0.0
        self.y = 0.0
        self.orientation = 0.0  # 0° = face à l'axe x positif

        # Vitesse des roues (en cm/s)
        self.vitesse_gauche = 0.0
        self.vitesse_droite = 0.0

        self.rayon_roue = 3.0       # rayon roue en cm
        self.largeur = 15.0         # distance entre roues en cm

        self.dernier_temps = time.time()

        # Liste d'obstacles (x,y) en cm
        self.obstacles = [(100, 50), (150, 80), (200, 200)]

    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        """Définit la vitesse des roues en cm/s."""
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite

    def update_position(self):
        """Met à jour la position et orientation du robot en fonction des vitesses et du temps écoulé."""
        maintenant = time.time()
        dt = maintenant - self.dernier_temps
        self.dernier_temps = maintenant

        # Calcul des distances parcourues par chaque roue
        dist_gauche = self.vitesse_gauche * dt
        dist_droite = self.vitesse_droite * dt

        # Calcul du déplacement linéaire moyen et de la rotation
        dist_moyenne = (dist_gauche + dist_droite) / 2.0
        delta_theta_rad = (dist_droite - dist_gauche) / self.largeur  # en radians

        # Mise à jour de l'orientation
        self.orientation += math.degrees(delta_theta_rad)
        self.orientation %= 360  # garder entre 0 et 360°

        # Mise à jour de la position (x, y)
        theta_rad = math.radians(self.orientation)
        self.x += dist_moyenne * math.cos(theta_rad)
        self.y += dist_moyenne * math.sin(theta_rad)

    def get_position(self):
        """Retourne la position actuelle (x, y) du robot."""
        return (self.x, self.y)

    def get_orientation(self):
        """Retourne l'orientation actuelle en degrés."""
        return self.orientation

    def stop(self):
        """Arrête les roues."""
        self.vitesse_gauche = 0
        self.vitesse_droite = 0

    def avancer(self, distance_cm, vitesse=20):
        """Fait avancer le robot d'une distance donnée en cm à une vitesse donnée (cm/s)."""
        self.set_wheel_speed(vitesse, vitesse)
        distance_parcourue = 0
        self.dernier_temps = time.time()

        while distance_parcourue < distance_cm:
            self.update_position()
            time.sleep(0.05)  # petite pause pour la simulation
            distance_parcourue += vitesse * 0.05

        self.stop()

    def tourner(self, angle_deg, vitesse=15):
        """Fait tourner le robot d'un angle donné (en degrés)."""
        direction = 1 if angle_deg > 0 else -1
        self.set_wheel_speed(-direction * vitesse, direction * vitesse)
        angle_tourne = 0
        self.dernier_temps = time.time()

        while abs(angle_tourne) < abs(angle_deg):
            self.update_position()
            time.sleep(0.05)
            angle_tourne += vitesse * 0.05 * (360 / (2 * math.pi * self.largeur))  # approx

        self.stop()

    def get_distance_devant(self):
        """
        Simule la détection de la distance au prochain obstacle devant le robot.
        Retourne la distance en cm, ou -1 si aucun obstacle proche.
        """
        min_distance = -1
        theta_rad = math.radians(self.orientation)
        x_rob = self.x
        y_rob = self.y

        for (x_obs, y_obs) in self.obstacles:
            # Vecteur entre robot et obstacle
            dx = x_obs - x_rob
            dy = y_obs - y_rob

            # Projection sur la direction du robot
            proj = dx * math.cos(theta_rad) + dy * math.sin(theta_rad)

            if proj > 0:  # obstacle devant
                # Distance perpendiculaire à la direction du robot
                perpend = abs(-dx * math.sin(theta_rad) + dy * math.cos(theta_rad))
                seuil = 10  # seuil de détection latérale en cm

                if perpend < seuil:
                    # Distance directe
                    distance = math.sqrt(dx*dx + dy*dy)
                    if min_distance == -1 or distance < min_distance:
                        min_distance = distance

        return min_distance

    def afficher_info(self):
        x, y = self.get_position()
        orientation = self.get_orientation()
        print(f"Position: ({x:.1f}, {y:.1f}), Orientation: {orientation:.1f}°, Distance devant: {self.get_distance_devant():.1f} cm")
