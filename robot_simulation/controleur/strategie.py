import time
class AvancerDroit:
    def __init__(self, adaptateur, distance):
        """
        Initialise la stratégie pour faire avancer le robot.
        
        :param adaptateur: L'adaptateur du robot (simulé ou réel).
        :param distance: La distance à parcourir.
        """
        self.adaptateur = adaptateur
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False

    def start(self):
        """Démarre la stratégie d'avance."""
        self.distance_parcourue = 0
        self.actif = True
        print("Début de l'avance droite")

    def step(self):
        """Fait avancer le robot d'une petite étape."""
        if not self.actif:
            return

        # Fait avancer le robot d'une petite distance
        self.adaptateur.avancer(12)  # Avancer de 12 unités
        self.distance_parcourue += 12

        # Mise à jour de la position et de la distance parcourue
        position = self.adaptateur.get_position()
        print(f"Avance droite: {self.distance_parcourue}/{self.distance}")
        print(f"Position: {position}")

    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.adaptateur.stop()  # Arrêter le robot
        return not self.actif 

class Tourner:
    def __init__(self, adaptateur, angle):
        """
        Initialise la stratégie pour faire tourner le robot.
        
        :param adaptateur: L'adaptateur du robot (simulé ou réel).
        :param angle: L'angle à tourner (en degrés).
        """
        self.adaptateur = adaptateur
        self.angle = angle
        self.angle_tourne = 0
        self.actif = False

    def start(self):
        """Démarre la rotation."""
        self.angle_tourne = 0
        self.actif = True
        print(f"Début de la rotation de {self.angle} degrés")

    def step(self):
        """Effectue la rotation par petites étapes."""
        if not self.actif:
            return

        # Fait tourner le robot d'un petit angle
        self.adaptateur.tourner(10)  # Tourner de 10 degrés
        self.angle_tourne += 10

        # Mise à jour de l'orientation
        orientation = self.adaptateur.get_orientation()
        print(f"Rotation: {self.angle_tourne}/{self.angle} | Orientation: {orientation}")

    def stop(self):
        """Retourne vrai si la rotation est terminée."""
        if self.angle_tourne >= self.angle:
            self.actif = False
            self.adaptateur.stop()  # Arrêter le robot
        return not self.actif
    
class Reculer:
    def __init__(self, adaptateur, distance):
        """
        Initialise la stratégie pour faire reculer le robot.
        
        :param adaptateur: L'adaptateur du robot (simulé ou réel).
        :param distance: La distance à reculer.
        """
        self.adaptateur = adaptateur
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False

    def start(self):
        """Démarre la stratégie de recul."""
        self.distance_parcourue = 0
        self.actif = True
        print("Début du recul")

    def step(self):
        """Fait reculer le robot d'une petite étape."""
        if not self.actif:
            return

        # Fait reculer le robot d'une petite distance
        self.adaptateur.reculer(12)  # Reculer de 12 unités
        self.distance_parcourue += 12

        # Mise à jour de la position et de la distance parcourue
        position = self.adaptateur.get_position()
        print(f"Recul: {self.distance_parcourue}/{self.distance}")
        print(f"Position: {position}")

    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.adaptateur.stop()  # Arrêter le robot
        return not self.actif
    
class StrategieCarre:
    def __init__(self, adaptateur):
        """Fait avancer le robot en carré."""
        self.actions = [
            AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
            AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
            AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
            AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
        ]
        self.index = 0
    
    def start(self):
        self.actions[self.index].start()
    
    def step(self):
        """Exécute l'action en cours et passe à la suivante si nécessaire."""
        if self.index < len(self.actions):
            self.actions[self.index].step()
            if self.actions[self.index].stop():
                self.index += 1
                if self.index < len(self.actions):
                    self.actions[self.index].start()
    
    def stop(self):
        """Retourne True si toutes les actions sont terminées."""
        return self.index >= len(self.actions)
    
class StrategieBoucle:
    def __init__(self, adaptateur, n):
        """Répète la stratégie du carré n fois."""
        self.n = n
        self.count = 0
        self.carre = StrategieCarre(adaptateur)
    
    def start(self):
        self.carre.start()
    
    def step(self):
        """Exécute les actions et redémarre si nécessaire."""
        if self.count < self.n:
            self.carre.step()
            if self.carre.stop():
                self.count += 1
                if self.count < self.n:
                    self.carre = StrategieCarre(self.carre.actions[0].adaptateur)
                    self.carre.start()
    
    def stop(self):
        return self.count >= self.n
    
class StrategieConditionnelle:
    def __init__(self, adaptateur):
        """Recule si un obstacle est détecté."""
        self.adaptateur = adaptateur
        self.reculer = Reculer(adaptateur, 50)
    
    def start(self):
        """Vérifie la présence d'un obstacle et recule si nécessaire."""
        if self.adaptateur.detect_obstacle():
            print("Obstacle détecté ! Recul en cours...")
            self.reculer.start()
    
    def step(self):
        """Continue le recul si actif."""
        if self.reculer.actif:
            self.reculer.step()
    
    def stop(self):
        return not self.reculer.actif