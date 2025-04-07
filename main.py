import sys
import time
import threading
import tkinter as tk
from robot_simulation.controleur.strategie import AvancerDroit, StrategieDemiTours, Tourner, Reculer
from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule
from robot_simulation.affichage.affichage_graphique import AffichageGraphique
from robot_simulation.affichage.affichage_3d import Affichage3D
from robot_simulation.controleur.controleur import Controleur
from robot_simulation.controleur.strategie import StrategieSequencielle
from robot_simulation.modele.environnement import Environnement
from robot_simulation.modele.robot import Robot

def mode_terminal():
    print("Mode terminal activé")
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))

    try:
        while True:
            controleur.update()
            # Remplacer par :
            if hasattr(adaptateur, 'robot'):
                x, y = adaptateur.robot.x, adaptateur.robot.y
            else:
                x, y = 0, 0
            print(f"Position estimée: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nArrêt du programme")

def mode_graphique():
    # Initialisation (conservez votre code existant)
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    
    adaptateur.dessine(True)

    adaptateur.avancer(100)

    adaptateur.dessine(False)
    
    strategie = StrategieDemiTours(
        adaptateur,
        env=500,
        iterations_max=10
    )
    controleur.set_strategie(strategie)
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))
    controleur.environnement = Environnement(width=500, height=500)
    
    # Configuration de la fenêtre
    root = tk.Tk()
    root.title("Simulation Robot")
    
    
    affichage = AffichageGraphique(root, adaptateur, controleur)
    affichage.pack(fill=tk.BOTH, expand=True)
    
    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)
    
    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()
    
    root.mainloop()

def mode_3d():
    robot = Robot(x=250, y=250)
    adaptateur = AdaptateurRobotSimule(robot)
    controleur = Controleur(adaptateur)
    actions = [
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 800), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))
    controleur.environnement = Environnement()

    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)

    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()

    affichage = Affichage3D(adaptateur, controleur)
    try:
        while getattr(controleur, 'running', True):
            affichage.update_affichage()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nArrêt du programme")
    finally:
        affichage.on_close()

def main():
    if "--no-gui" in sys.argv:
        mode_terminal()
    elif "--3d" in sys.argv:
        mode_3d()
    else:
        mode_graphique()

if __name__ == "__main__":
    main()
