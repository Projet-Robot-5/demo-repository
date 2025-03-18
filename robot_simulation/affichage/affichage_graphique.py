import tkinter as tk  # Importation de la bibliothèque Tkinter pour l'interface graphique
import time  # Pour gérer le temps d'attente entre les mises à jour
import threading  # Pour exécuter des tâches en parallèle (affichage graphique dans un thread)

from robot_simulation.controleur.controleur import Controleur  # Importation de la classe Controleur pour gérer les mouvements du robot
from robot_simulation.modele.simulation import Simulation  # Importation de la classe Simulation (non utilisée dans ce code)
from robot_simulation.controleur.strategie import StrategieCarre  # Importation de la stratégie Carre
class AffichageGraphique:
    def __init__(self, master, robot, controleur):
        """Initialise l'affichage graphique de la simulation.
        
        :param master: La fenêtre principale de l'application tkinter.
        :param robot: L'objet robot qui sera contrôlé dans la simulation.
        """
        self.controleur=controleur
        self.master = master  # La fenêtre principale de l'application
        self.robot = robot  # Le robot à contrôler
        # Création d'un canevas pour dessiner l'environnement de simulation
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()

        # Stocker la trajectoire du robot pour dessiner le chemin qu'il a parcouru
        self.trajet = []

        # Créer un objet contrôleur pour gérer les mouvements du robot en mode graphique
        
        #self.controleur = Controleur(self.robot, mode="graphique", master=self.master)  
        #self.controleur.faire_carre(120)  # Démarrer la simulation du robot qui suit une trajectoire carrée
        # Remplacer l'appel à 'faire_carre' par l'ajout de la stratégie de carré
        self.controleur.strategie_courante = StrategieCarre(self.controleur.robot)
        self.controleur.ajouter_strategie(self.controleur.strategie_courante)
        # Indicateur pour contrôler si le thread graphique doit continuer à s'exécuter
        self.running = True

        # Lancer la mise à jour graphique sur l'interface
        self.update_affichage()

        # Lancer un thread séparé pour mettre à jour l'affichage graphique
        self.thread = threading.Thread(target=self.update_affichage_thread)
        self.thread.daemon = True  # Le thread se termine automatiquement lorsque la fenêtre est fermée
        self.thread.start()

        # Gérer la fermeture de la fenêtre pour arrêter proprement le thread
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_affichage(self):
        """Met à jour l'affichage graphique du robot en traçant sa trajectoire."""
        if not self.running:
            return  # Si le thread n'est plus en cours d'exécution, on arrête la mise à jour

        
        # Déplacer le robot dans la simulation
        self.robot.move(dt=0.1)

        # Ajouter la nouvelle position du robot à sa trajectoire
        x, y = self.robot.x, self.robot.y

        # Dessiner la ligne entre la position précédente et la position actuelle du robot
        if len(self.trajet) > 0:
            prev_x, prev_y = self.trajet[-1]
            self.canvas.create_line(prev_x, prev_y, x, y, fill="black", width=2)  # Traçage du chemin du robot

        # Sauvegarder la nouvelle position du robot
        self.trajet.append((x, y))

        # Effacer le robot précédent sur le canevas pour éviter de dessiner plusieurs fois la même forme
        self.canvas.delete("robot")

        # Dessiner les obstacles dans l'environnement
        for obs in self.controleur.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")  # Obstacles en rouge

        # Dessiner le robot en bleu à sa position actuelle
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue", tags="robot")  # Robot dessiné en bleu
        
        
        # Ajouter la flèche indiquant la direction du robot
        angle_rad = math.radians(self.robot.orientation)  # Convertir l'orientation en radians
        arrow_length = 20  # Longueur de la flèche
        arrow_x = x + arrow_length * math.cos(angle_rad)  # Calculer la position X de la flèche
        arrow_y = y + arrow_length * math.sin(angle_rad)  # Calculer la position Y de la flèche
         # Dessiner la flèche avec une tête de flèche à la fin
        self.canvas.create_line(x, y, arrow_x, arrow_y, width=2, arrow=tk.LAST, fill="green")  # Flèche verte
 

        # Vérifier si toutes les stratégies sont terminées
        if not self.controleur.queue_strategies and not self.controleur.strategie_courante:
            self.running = False  # Arrêter l'exécution du thread si toutes les stratégies sont terminées
            # Fermer la fenêtre après un délai d'une seconde
            self.master.after(1000, self.master.destroy)
            return

        # Continuer la mise à jour graphique après 50 millisecondes
        self.master.after(50, self.update_affichage)

    def update_affichage_thread(self):
        """Mise à jour graphique dans un thread séparé."""
        while self.running:
            time.sleep(0.05)  # Réduit la charge CPU et ne bloque pas l'interface graphique

    def on_close(self):
        """Ferme la fenêtre et arrête proprement le thread."""
        self.running = False  # Arrêter le thread de mise à jour
        self.thread.join(timeout=1)  # Attendre que le thread se termine proprement
        self.master.destroy()  # Fermer la fenêtre tkinter
    def run(self):
        """Lance la mise à jour continue de l'affichage."""
        while self.running:
            self.update_affichage()
            time.sleep(0.05)

