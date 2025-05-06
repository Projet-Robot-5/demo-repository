import math
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
        if hasattr(self.adaptateur, 'robot'):
            position = (self.adaptateur.robot.x, self.adaptateur.robot.y)
        else:
            position = (0, 0)  # Valeur par défaut
        
        print(f"Avance droite: {self.distance_parcourue}/{self.distance}")
        print(f"Position estimée: {position}")

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
        if hasattr(self.adaptateur, 'robot'):
            orientation = self.adaptateur.robot.orientation
        else:
            orientation = 0  # Valeur par défaut
            
        print(f"Rotation: {self.angle_tourne}/{self.angle} | Orientation estimée: {orientation}")
        
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
    
class DetecterBalise:
    def __init__(self, adaptateur):
        self.adaptateur = adaptateur
        self.actif = False
        self.balise_trouvee = False
        
    def start(self):
        self.actif = True
        self.balise_trouvee = False
        print("Recherche balise...")
        
    def step(self):
        if not self.actif:
            return
            
        if hasattr(self.adaptateur.robot, 'environnement'):
            balises = getattr(self.adaptateur.robot.environnement, 'balises', [])
            if balises:
                self.adaptateur.robot.balise_cible = balises[0]
                self.balise_trouvee = True

    def stop(self):
        self.actif = False
        return self.balise_trouvee  # True si balise trouvée, False sinon


class TournerVersBalise:
    def __init__(self, adaptateur):
        self.adaptateur = adaptateur
        self.actif = False
        
    def start(self):
        self.actif = True
        print("Alignement sur balise...")
        
    def step(self):
        if not self.actif:
            return
            
        robot = self.adaptateur.robot
        if hasattr(robot, 'balise_cible'):
            bx, by = robot.balise_cible
            dx, dy = bx - robot.x, by - robot.y
            angle_cible = math.degrees(math.atan2(dy, dx))
            angle_diff = (angle_cible - robot.orientation) % 360
            
            if angle_diff > 180:
                angle_diff -= 360
                
            if abs(angle_diff) > 5:  # Seuil de précision
                self.adaptateur.tourner(angle_diff * 0.3)
            else:
                self.actif = False

    def stop(self):
        return not self.actif  # True quand alignement terminé


class AvancerVersBalise:
    def __init__(self, adaptateur):
        self.adaptateur = adaptateur
        self.actif = False
        
    def start(self):
        self.actif = True
        print("Approche balise...")
        
    def step(self):
        if not self.actif:
            return
            
        robot = self.adaptateur.robot
        if hasattr(robot, 'balise_cible'):
            bx, by = robot.balise_cible
            distance = math.sqrt((bx-robot.x)**2 + (by-robot.y)**2)
            
            if distance > 20:  # Distance d'arrêt
                self.adaptateur.avancer(min(100, distance * 0.5))
            else:
                self.actif = False

    def stop(self):
        return not self.actif  # True quand distance atteinte
    
class SuivreBalise:
    def __init__(self, adaptateur, environnement):  # Accepte maintenant environnement
        self.adaptateur = adaptateur
        self.environnement = environnement
        self.actif = False

    def start(self):
        self.actif = True
        print("Démarrage suivi de balise")

    def step(self):
        if not self.actif:
            return
            
        robot = self.adaptateur.robot
        balises = getattr(self.environnement, 'balises', [])
        
        if balises:
            bx, by = balises[0]  # Prend la première balise
            dx, dy = bx - robot.x, by - robot.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 20:  # Distance d'arrêt
                angle_cible = math.degrees(math.atan2(dy, dx))
                angle_diff = (angle_cible - robot.orientation + 180) % 360 - 180
                
                if abs(angle_diff) > 10:  # Seuil de rotation
                    self.adaptateur.tourner(angle_diff * 0.8)
                else:
                    self.adaptateur.avancer(min(40, distance * 0.5))
            else:
                self.adaptateur.stop()
        else:
            print("Recherche balise...")
            self.adaptateur.tourner(30)  # Rotation de recherche

    def stop(self):
        self.actif = False
        self.adaptateur.stop()
        return True
    
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
    def __init__(self, strategie1, strategie2, condition):
        """
        Initialise la stratégie conditionnelle avec deux stratégies et une condition.
        :param strategie1: La première stratégie à exécuter si la condition est vraie.
        :param strategie2: La deuxième stratégie à exécuter si la condition est fausse.
        :param condition: La condition (fonction ou booléenne) pour choisir la stratégie à exécuter.
        """
        self.strategie1 = strategie1  # Première stratégie
        self.strategie2 = strategie2  # Deuxième stratégie
        self.condition = condition  # La condition qui détermine quelle stratégie exécuter
    
    def start(self):
        """Vérifie la condition et exécute la stratégie appropriée."""
        if self.condition():
            print("Condition vraie, exécution de la stratégie 1...")
            self.strategie1.start()  # Exécute la stratégie 1
        else:
            print("Condition fausse, exécution de la stratégie 2...")
            self.strategie2.start()  # Exécute la stratégie 2
    
    def step(self):
        """Exécute la prochaine étape de la stratégie active."""
        if self.condition():
            if hasattr(self.strategie1, 'step'):
                self.strategie1.step()  # Exécuter la méthode step de la stratégie 1
        else:
            if hasattr(self.strategie2, 'step'):
                self.strategie2.step()  # Exécuter la méthode step de la stratégie 2
    
    def stop(self):
        """Arrête la stratégie active."""
        if self.condition():
            return self.strategie1.stop()  # Arrêter la stratégie 1 si la condition est vraie
        else:
            return self.strategie2.stop()  # Arrêter la stratégie 2 si la condition est fausse
        
class ApprocheMur:
    """
    Classe représentant une stratégie pour approcher un mur rapidement sans le toucher.

    Attributs:
        robot (Robot): L'objet robot à contrôler.
        environnement (Environnement): L'environnement contenant les obstacles.
        ecartAvecMur (float): Distance minimale à garder avec le mur.
    """

    def __init__(self, robot, environnement, ecartAvecMur):
        self.robot = robot
        self.environnement = environnement
        self.ecartAvecMur = ecartAvecMur
        self.detected_obstacle = False
        self.arret = False

    def start(self):
        """Initialise le contrôleur."""
        self.robot.set_wheel_speed(100, 100)
        self.detected_obstacle = False
        self.arret = False

    def step(self):
        """Exécute une étape de la stratégie."""
        dist = self.robot.get_distance_devant(self.environnement.obstacles)
        print("Distance à l'obstacle le plus proche :", dist)
        if dist != -1 and dist <= self.ecartAvecMur:
            # Si obstacle détecté et à moins de ecartAvecMur, on s'arrête
            self.robot.stop()
            self.arret = True
        else:
            # Sinon, on continue à avancer vite
            self.robot.set_wheel_speed(100, 100)

    def stop(self):
        """Vérifie si la stratégie doit s'arrêter."""
        return self.arret




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

class StrategieContournement:
    """
    Stratégie autonome pour contourner un obstacle détecté devant le robot.
    Le robot tourne progressivement jusqu'à ce qu'il n'y ait plus d'obstacle en face.
    """

    def __init__(self, adaptateur, environnement, seuil_detection=30):
        """
        Initialise la stratégie de contournement.

        :param adaptateur: Adaptateur (simulé ou réel) du robot.
        :param environnement: Environnement contenant les obstacles.
        :param seuil_detection: Distance seuil pour détecter un obstacle (en cm).
        """
        self.adaptateur = adaptateur
        self.environnement = environnement
        self.seuil_detection = seuil_detection
        self.actif = False

    def start(self):
        self.actif = True
        print("Stratégie de contournement d’obstacle démarrée.")

    def step(self):
        if not self.actif:
            return

        # Mesure la distance devant
        distance = self.adaptateur.get_distance_devant(self.environnement.obstacles)
        print(f"[Contournement] Distance détectée : {distance} cm")

        if 0 <= distance <= self.seuil_detection:
            # Tourne légèrement vers la droite pour chercher un passage libre
            self.adaptateur.tourner(10)
        else:
            # Obstacle évité, on peut continuer
            self.actif = False

    def stop(self):
        return not self.actif
