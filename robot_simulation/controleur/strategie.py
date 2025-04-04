import time
import math

class Strategie:
    def __init__(self, adaptateur):
        self.adaptateur = adaptateur

    def step(self, dt):
        raise NotImplementedError

    def stop(self):
        self.adaptateur.set_wheel_speed(0, 0)


class AvancerDroit(Strategie):
    def __init__(self, adaptateur, vitesse=50):
        super().__init__(adaptateur)
        self.vitesse = vitesse

    def start(self):
        """Commence l'action d'avancer droit."""
        print(f"Début de l'avancement à une vitesse de {self.vitesse} m/s.")
        self.adaptateur.set_wheel_speed(self.vitesse, self.vitesse)

    def step(self, dt):
        """Continue à avancer selon la vitesse."""
        # L'avancement se fait de manière continue. Si besoin d'ajouter une logique pour l'arrêt, on peut l'ajouter ici.
        # Par exemple, on pourrait avoir un critère de distance ou de durée ici, mais actuellement, on avance indéfiniment.
        return True  # Continuer à avancer

    def stop(self):
        """Arrête l'avancement du robot."""
        self.adaptateur.set_wheel_speed(0, 0)
        print("Avancement arrêté.")


class Tourner(Strategie):
    def __init__(self, adaptateur, vitesse=30):
        super().__init__(adaptateur)
        self.vitesse = vitesse  # La vitesse à laquelle le robot doit tourner
        self.signe = 1  # Direction par défaut pour tourner dans un sens

    def start(self):
        """Commence l'action de tourner avec la vitesse définie."""
        print(f"Début de la rotation avec une vitesse de {self.vitesse}.")
        self.adaptateur.set_wheel_speed(-self.signe * self.vitesse, self.signe * self.vitesse)

    def step(self, dt):
        """Effectue la rotation basée sur la vitesse."""
        # Calcul de la distance parcourue pendant la rotation
        distance_parcourue = self.adaptateur.get_distance_parcourue()

        # Par exemple, pour un certain angle (disons 90°), la rotation devrait être effectuée sur une distance prédéfinie
        distance_cible = 0.5  # Une valeur estimée de distance (à ajuster selon les besoins)

        if distance_parcourue < distance_cible:
            return True  # Continue de tourner
        else:
            self.stop()
            return False  # Arrêt de la rotation

class Reculer(Strategie):
    def __init__(self, adaptateur, vitesse=50):
        super().__init__(adaptateur)
        self.vitesse = vitesse

    def start(self):
        """Commence l'action de reculer."""
        print(f"Recul en cours à une vitesse de {self.vitesse} m/s.")
        self.adaptateur.set_wheel_speed(-self.vitesse, -self.vitesse)

    def step(self, dt):
        """Continue le recul basé sur la vitesse."""
        if self.adaptateur.get_distance_parcourue() < self.adaptateur.distance_cible:
            return True  # Continue de reculer
        else:
            self.stop()
            return False  # Arrêt

    def stop(self):
        """Arrête le recul du robot."""
        self.adaptateur.set_wheel_speed(0, 0)


class StrategieSequencielle:
    def __init__(self, actions):
        self.actions = actions  # Liste des actions à exécuter dans la séquence
        self.index = 0  # Indice pour suivre quelle action est en cours
        self.running = False  # Pour suivre l'état de l'exécution de la stratégie

    def start(self):
        """ Démarre la stratégie en initialisant la première action. """
        if not self.actions:
            return
        self.running = True
        self.actions[self.index].start()

    def step(self, dt):
        """ Passe à l'action suivante dans la séquence. """
        if not self.running or self.index >= len(self.actions):
            return

        current_action = self.actions[self.index]
        if current_action.step(dt):  # Si l'action est terminée
            self.index += 1
            if self.index < len(self.actions):
                self.actions[self.index].start()  # Commence la suivante

    def stop(self):
        """ Arrête la stratégie. """
        self.running = False
        if self.index < len(self.actions):
            self.actions[self.index].stop()





    
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
