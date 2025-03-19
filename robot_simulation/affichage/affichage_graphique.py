import tkinter as tk
import math
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieCarre

class AffichageGraphique:
    def __init__(self, master, adaptateur, controleur):
        """
        Initialise l'affichage graphique de la simulation.

        :param master: La fenêtre principale tkinter.
        :param adaptateur: L'adaptateur du robot (simulé ou réel).
        :param controleur: Le contrôleur de la simulation.
        """
        self.controleur = controleur
        self.master = master
        self.adaptateur = adaptateur
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()
        self.trajet = []  # Liste pour stocker la trajectoire du robot
        self.running = True  # Indicateur pour contrôler la boucle d'affichage

        # Démarrer la stratégie du carré
        self.controleur.strategie_courante = StrategieCarre(self.adaptateur)
        self.controleur.ajouter_strategie(self.controleur.strategie_courante)

        # Lancer la mise à jour graphique
        self.update_affichage()

    def update_affichage(self):
        """Met à jour l'affichage graphique du robot en traçant sa trajectoire."""
        if not self.running:
            return  # Arrêter la mise à jour si la simulation est terminée

        # Effacer le robot précédent
        self.canvas.delete("robot")  # Supprime uniquement le robot, pas la trajectoire

        # Récupérer la position actuelle du robot
        x, y = self.adaptateur.get_position()
        orientation = self.adaptateur.get_orientation()

        # Ajouter la nouvelle position à la trajectoire
        if len(self.trajet) > 0:
            prev_x, prev_y = self.trajet[-1]
            self.canvas.create_line(prev_x, prev_y, x, y, fill="black", width=2)  # Tracer la trajectoire

        self.trajet.append((x, y))  # Ajouter la nouvelle position à la trajectoire

        # Dessiner les obstacles
        for obs in self.controleur.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")

        # Dessiner le robot à sa nouvelle position
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="robot")

        # Dessiner la direction du robot
        angle_rad = math.radians(orientation)
        dir_x = x + 20 * math.cos(angle_rad)
        dir_y = y + 20 * math.sin(angle_rad)
        self.canvas.create_line(x, y, dir_x, dir_y, fill="green", arrow=tk.LAST, tags="robot")

        # Dessiner les roues du robot avec rotation et flèches
        wheel_distance = 15  # Distance entre les roues
        wheel_size = 5  # Taille des roues
        left_wheel_x = x - wheel_distance * math.sin(angle_rad)
        left_wheel_y = y + wheel_distance * math.cos(angle_rad)
        right_wheel_x = x + wheel_distance * math.sin(angle_rad)
        right_wheel_y = y - wheel_distance * math.cos(angle_rad)

        # Calculer l'angle des roues en fonction de l'orientation du robot
        wheel_angle = orientation  # Utiliser l'orientation du robot pour les roues

        # Dessiner les roues avec rotation et flèches
        self.draw_rotated_wheel_with_arrow(left_wheel_x, left_wheel_y, wheel_size, wheel_angle)
        self.draw_rotated_wheel_with_arrow(right_wheel_x, right_wheel_y, wheel_size, wheel_angle)

        # Vérifier si toutes les stratégies sont terminées
        if not self.controleur.queue_strategies and not self.controleur.strategie_courante:
            self.running = False  # Arrêter la simulation si toutes les stratégies sont terminées
            self.master.after(1000, self.master.destroy)  # Fermer la fenêtre après un délai
            return

        # Continuer la mise à jour après 50ms
        self.master.after(50, self.update_affichage)

    def draw_rotated_wheel_with_arrow(self, x, y, size, angle):
        """Dessine une roue avec un angle de rotation donné et une flèche indiquant la direction."""
        angle_rad = math.radians(angle)
        cos, sin = math.cos(angle_rad), math.sin(angle_rad)

        # Calculer les coins de la roue tournée
        top_left = (x - size * cos - size * sin, y - size * sin + size * cos)
        bottom_right = (x + size * cos - size * sin, y + size * sin + size * cos)

        self.canvas.create_oval(top_left[0], top_left[1], bottom_right[0], bottom_right[1], fill="gray", tags="robot")

        # Dessiner une flèche indiquant la direction de la roue
        arrow_length = 10
        arrow_x = x + arrow_length * cos
        arrow_y = y + arrow_length * sin
        self.canvas.create_line(x, y, arrow_x, arrow_y, fill="red", arrow=tk.LAST, tags="robot")

    def on_close(self):
        """Ferme la fenêtre et arrête proprement l'exécution."""
        self.running = False
        self.master.destroy()
