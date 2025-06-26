import time
import math
class AvancerDroit:
    def __init__(self, adaptateur, distance, vitesse=40):
        self.adaptateur = adaptateur
        self.distance = distance
        self.vitesse = vitesse
        self.depart = None
        self.actif = False

    def start(self):
        """Démarre la stratégie d'avance en enregistrant la distance initiale."""
        self.depart = self.adaptateur.get_distance_parcourue()
        self.actif = True
        print("Début de l'avance droite")

    def step(self):
        """Commande le robot pour avancer tant que la distance n’est pas atteinte."""
        if not self.actif:
            return
        self.adaptateur.avancer(self.vitesse)
        print(f"Distance parcourue depuis le départ : {self.adaptateur.get_distance_parcourue() - self.depart:.2f}/{self.distance}")

    def stop(self):
        """Arrête le robot si la distance est atteinte."""
        if (self.adaptateur.get_distance_parcourue() - self.depart) >= self.distance:
            self.actif = False
            self.adaptateur.stop()
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
    def __init__(self, adaptateur, distance, vitesse=60):
        self.adaptateur = adaptateur
        self.distance = distance
        self.vitesse = -abs(vitesse)
        self.depart = None
        self.actif = False

    def start(self):
        self.depart = self.adaptateur.get_distance_parcourue()
        self.actif = True
        print("Début du recul")

    def step(self):
        if not self.actif:
            return
        self.adaptateur.reculer(abs(self.vitesse))
        print(f"Distance reculée : {self.adaptateur.get_distance_parcourue() - self.depart:.2f}/{self.distance}")

    def stop(self):
        if (self.adaptateur.get_distance_parcourue() - self.depart) >= self.distance:
            self.actif = False
            self.adaptateur.stop()
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

class TriangleEquilateral:
    def __init__(self, adaptateur, longueur=100, angle=(60):
        self.adaptateur = adaptateur
        #self.angle=60
        self.actions = []
    
    for adapateur in range(3):   
        self.actions.append(AvancerDroit(adaptateur, longueur_cote))
        self.actions.apend(Tourner(adaptateur, angle))
    self.strategie = StrategieSequencielle(self.action)

    def start(self):
        self.strategie.start()

    def step(self):
        self.strategie.step()

    def stop(self):
        return step.strategie.stop()

    