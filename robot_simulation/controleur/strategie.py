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
    
    
class StrategieSequencielle:
    def __init__(self, actions):
        """
        Stratégie séquentielle qui exécute une liste d'actions dans l'ordre donné.
        
        :param actions: Liste d'actions (objets de type stratégie comme AvancerDroit, Tourner, etc.)
        """
        self.actions = actions  # Liste des actions à exécuter
        self.index = 0  # Indice de l'action courante

    def start(self):
        """Démarre la première action de la séquence."""
        if self.actions:
            print("Démarrage de la stratégie séquentielle.")
            self.actions[self.index].start()

    def step(self):
        """Exécute l'action en cours et passe à la suivante si nécessaire."""
        if self.index < len(self.actions):
            self.actions[self.index].step()
            if self.actions[self.index].stop():
                print(f"Action {self.index + 1} terminée.")
                self.index += 1
                if self.index < len(self.actions):
                    print(f"Passage à l'action {self.index + 1}.")
                    self.actions[self.index].start()

    def stop(self):
        """Retourne True si toutes les actions de la séquence sont terminées."""
        if self.index >= len(self.actions):
            print("Stratégie séquentielle terminée.")
            return True
        return False  

    
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
# robot_simulation/controleur/strategie.py

class StrategieBoucle:
    def __init__(self, actions, nb_iterations=None):
        """
        Initialise la stratégie de boucle.
        
        :param actions: Liste des actions à exécuter dans la boucle
        :param nb_iterations: Nombre d'itérations avant d'arrêter (None pour une boucle infinie)
        """
        self.actions = actions
        self.nb_iterations = nb_iterations
        self.iteration = 0

    def start(self):
        """
        Démarre l'exécution des actions en boucle.
        """
        print("Démarrage de la boucle.")
        self.iteration = 0

    def step(self):
        """
        Exécute une étape de la boucle.
        Si nb_iterations est défini, cela arrêtera après le nombre spécifié.
        """
        if self.nb_iterations is not None and self.iteration >= self.nb_iterations:
            print("Fin des itérations.")
            return
        
        # Répéter les actions à chaque itération
        for action in self.actions:
            action.start()  # Lance chaque action de la liste
            
            # Une fois l'action terminée, on passe à la suivante
            action.step()
            action.stop()

        # Incrémenter l'itération
        self.iteration += 1

    def stop(self):
        """
        Arrête la boucle si nécessaire.
        """
        print("Arrêt de la boucle.")
        for action in self.actions:
            action.stop()
