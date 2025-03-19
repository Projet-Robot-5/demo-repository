import time
class AvancerDroit:
    def __init__(self, robot, distance):
        self.robot = robot
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False
    def start(self):
        """Démarre la stratégie d'avance."""
        self.distance_parcourue = 0
        self.robot.set_wheel_speed(12, 12)
        self.actif = True
        print("Début de l'avance droite")
    def step(self):
        """Fait avancer le robot d'une petite étape."""
        if not self.actif:
            return
        self.robot.move(dt=1)
        self.distance_parcourue += 12
        print(f"Avance droite: {self.distance_parcourue}/{self.distance}")
        print(f"Position: ({self.robot.x}, {self.robot.y})")
        print(f"Orientation: {self.robot.orientation}")
    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)
        return not self.actif  

class Tourner:
    def __init__(self, robot, angle):
        self.robot = robot
        self.angle = angle  # Angle total à tourner
        self.angle_tourne = 0  # Angle déjà tourné
        self.actif = False
    def start(self):
        """Démarre la rotation."""
        self.angle_tourne = 0
        self.robot.set_wheel_speed(-4, 4)  # Rotation à gauche
        self.actif = True
        print(f"Début de la rotation de {self.angle} degrés")
    def step(self):
        """Effectue la rotation par petites étapes."""
        if not self.actif:
            return

        # Faire avancer le robot pendant un petit pas de temps
        self.robot.move(dt=1)

        # Mettre à jour l'angle tourné
        self.angle_tourne += 10  # Supposons que chaque étape tourne de 5 degrés

        # Mettre à jour l'orientation du robot
        self.robot.orientation = (self.robot.orientation + 10) % 360

        # Ajuster l'orientation pour qu'elle soit toujours proche d'un multiple de 90
        if self.angle_tourne % 90 == 0:
            self.robot.orientation = round(self.robot.orientation / 90) * 90
            self.robot.orientation %= 360  # Garantir que l'orientation est entre 0 et 360

        print(f"Rotation: {self.angle_tourne}/{self.angle} | Orientation: {self.robot.orientation}")
    def stop(self):
        """Retourne vrai si la rotation est terminée."""
        if self.angle_tourne >= self.angle:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)  # Arrêter les roues

            # Correction finale de l'orientation pour s'assurer qu'elle est un multiple de 90
            self.robot.orientation = round(self.robot.orientation / 90) * 90
            self.robot.orientation %= 360  # Garantir que l'orientation est entre 0 et 360

            print(f"Rotation terminée. Orientation finale: {self.robot.orientation}")
        return not self.actif
class Reculer:
    def __init__(self, robot, distance):
        self.robot = robot
        self.distance = distance
        self.distance_parcourue = 0
        self.actif = False

    def start(self):
        """Démarre la stratégie de recul."""
        self.distance_parcourue = 0
        self.robot.set_wheel_speed(-12, -12)  # Vitesse négative pour reculer
        self.actif = True
        print("Début du recul")
    
    def step(self):
        """Fait reculer le robot d'une petite étape."""
        if not self.actif:
            return
        self.robot.move(dt=1)
        self.distance_parcourue += 12
        print(f"Recul: {self.distance_parcourue}/{self.distance}")
        print(f"Position: ({self.robot.x}, {self.robot.y})")
        print(f"Orientation: {self.robot.orientation}")

    def stop(self):
        """Retourne vrai si la distance est atteinte."""
        if self.distance_parcourue >= self.distance:
            self.actif = False
            self.robot.set_wheel_speed(0, 0)  # Arrêter le robot
        return not self.actif
class StrategieCarre:
    def __init__(self, robot):
        """Fait avancer le robot en carré."""
        self.actions = [
            AvancerDroit(robot, 100), Tourner(robot, 90),
            AvancerDroit(robot, 100), Tourner(robot, 90),
            AvancerDroit(robot, 100), Tourner(robot, 90),
            AvancerDroit(robot, 100), Tourner(robot, 90)
        ]
        self.index = 0
    
    def start(self):
        self.actions[self.index].start()
    
    def step(self):
        """Exécute l'action en cours et passe à la 
        suivante si nécessaire."""
        if self.index < len(self.actions):
            self.actions[self.index].step()
            if self.actions[self.index].stop():
                self.index += 1
                if self.index < len(self.actions):
                    self.actions[self.index].start()
    
    def stop(self):
        """Retourne True si toutes 
        les actions sont terminées."""
        return self.index >= len(self.actions)

class StrategieBoucle:
    def __init__(self, robot, n):
        """Répète la stratégie du carré n fois."""
        self.n = n
        self.count = 0
        self.carre = StrategieCarre(robot)
    
    def start(self):
        self.carre.start()
    
    def step(self):
        """Exécute les actions et redémarre si nécessaire."""
        if self.count < self.n:
            self.carre.step()
            if self.carre.stop():
                self.count += 1
                if self.count < self.n:
                    self.carre = StrategieCarre(self.carre.actions[0].robot)
                    self.carre.start()
    
    def stop(self):
        return self.count >= self.n
class StrategieConditionnelle:
    def __init__(self, robot):
        """Recule si un obstacle est détecté."""
        
        self.robot = robot
        self.reculer = Reculer(robot, 50)
    
    def start(self):
        """Vérifie la présence d'un obstacle et recule si nécessaire."""
        if self.robot.detect_obstacle():
            print("Obstacle détecté ! Recul en cours...")
            self.reculer.start()
    
    def step(self):
        """Continue le recul si actif."""
        if self.reculer.actif:
            self.reculer.step()
    
    def stop(self):
        return not self.reculer.actif