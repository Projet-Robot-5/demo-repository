import time
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
        self.adaptateur.update_position() 
        self.adaptateur.avancer(self.vitesse)
        print(f"Distance parcourue depuis le départ : {self.adaptateur.get_distance_parcourue() - self.depart:.2f}/{self.distance}")

    def stop(self):
        """Arrête le robot si la distance est atteinte."""
        if (self.adaptateur.get_distance_parcourue() - self.depart) >= self.distance:
            self.actif = False
            self.adaptateur.stop()
        return not self.actif


class Tourner:
    def __init__(self, adaptateur, angle, vitesse_rotation=50):
        self.adaptateur = adaptateur
        self.angle_demande = angle
        self.vitesse_rotation = vitesse_rotation
        self.angle_parcouru = 0
        self.actif = False
        self.direction = 1 if angle > 0 else -1
        self.last_orientation = None  # 🆕 stocker l'angle précédent

    def start(self):
        self.angle_parcouru = 0
        self.actif = True
        print(f"Début rotation: {self.angle_demande}°")
        self.last_orientation = self.adaptateur.get_angle_tourne()  # 🆕
        self.adaptateur.tourner(self.direction * self.angle_demande, self.vitesse_rotation)

    def step(self):
        if not self.actif:
            return

        self.adaptateur.update_position() 
        current_angle = self.adaptateur.get_angle_tourne()  # ✅ lecture correcte
        delta = (current_angle - self.last_orientation) % 360

        if delta > 180:
            delta -= 360

        self.angle_parcouru += abs(delta)
        self.last_orientation = current_angle

        print(f"Rotation: {self.angle_parcouru:.1f}/{abs(self.angle_demande)}°")

    def stop(self):
        if self.angle_parcouru >= abs(self.angle_demande):
            self.adaptateur.stop()
            self.actif = False
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

def faire_carre(adaptateur, longueur=200, angle=90, vitesse=40, vitesse_rotation=50):
    actions = []
    for _ in range(4):
        actions.append(AvancerDroit(adaptateur, longueur, vitesse))
        actions.append(Tourner(adaptateur, angle, vitesse_rotation))
    return StrategieSequencielle(actions)
