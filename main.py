import threading
import sys
import time
import tkinter as tk
import importlib.util
# robot_simulation/controleur/controleur.py
from robot_simulation.controleur.strategie import AvancerDroit, Tourner, Reculer 
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot
from robot_simulation.modele.simulation import Simulation
def initialiser_simulation():
    """
    Fonction pour initialiser la simulation avec les objets nécessaires,
    utilisée par les modes terminal et graphique.
    
    Retourne :
    - adaptateur : L'adaptateur pour le robot.
    - controleur : Le contrôleur qui gère les actions du robot.
    - actions : La liste des actions à effectuer (séquence).
    """
    robot = Robot(x=250, y=250)  # Création du robot
    adaptateur = AdaptateurRobotSimule(robot)  # Création de l'adaptateur pour le robot simulé
    controleur = Controleur(adaptateur)  # Création du contrôleur
    """"""
    # Création d'une séquence pour un carré
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    
    # Configuration de la stratégie
    controleur.set_strategie(StrategieSequencielle(actions))
    
    return adaptateur, controleur, actions 
def mode_terminal():
    print("Mode terminal activé")
    adaptateur, controleur, actions = initialiser_simulation() 
    
    try:
        while True:
            controleur.update()
            x, y = adaptateur.get_position()
            print(f"Position actuelle: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nArrêt du programme")

def mode_graphique():
    # Initialisation des composants
    adaptateur, controleur, actions = initialiser_simulation()
    
    controleur.environnement=Environnement()
    # Thread pour le contrôleur
    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()
    
    # Interface graphique dans le thread principal
    root = tk.Tk()
    root.title("Simulation Robot")
    
    # Configuration de l'affichage
    affichage = AffichageGraphique(root, adaptateur, controleur)
    root.protocol("WM_DELETE_WINDOW", lambda: [
        setattr(controleur, 'running', False),
        ctrl_thread.join(timeout=0.1),
        root.destroy()
    ])
    
    root.mainloop()

def main():
    if "--no-gui" in sys.argv:
        mode_terminal()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()