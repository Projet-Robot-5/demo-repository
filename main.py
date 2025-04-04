import sys
import time
import threading
import tkinter as tk
from robot_simulation.controleur.strategie import AvancerDroit, Tourner, Reculer
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
    rayon_roue = 0.05  # Définir le rayon des roues (par exemple 5 cm)

    adaptateur = AdaptateurRobotSimule(robot, rayon_roue)

    controleur = Controleur(adaptateur)
    actions = [
        AvancerDroit(adaptateur,50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur,50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))

    try:
        while True:
            controleur.update()
            x, y = adaptateur.get_position()
            print(f"Position actuelle: ({x:.1f}, {y:.1f})")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nArrêt du programme")

def mode_graphique():
    robot = Robot(x=250, y=250)
    rayon_roue = 0.05  # Définir le rayon des roues (par exemple 5 cm)

    adaptateur = AdaptateurRobotSimule(robot, rayon_roue)
    controleur = Controleur(adaptateur)
    actions = [
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90),
        AvancerDroit(adaptateur, 50), Tourner(adaptateur, 90)
    ]
    controleur.set_strategie(StrategieSequencielle(actions))
    controleur.environnement = Environnement()

    def run_controleur():
        while getattr(controleur, 'running', True):
            controleur.update()
            time.sleep(0.05)

    ctrl_thread = threading.Thread(target=run_controleur, daemon=True)
    ctrl_thread.start()

    root = tk.Tk()
    root.title("Simulation Robot")
    affichage = AffichageGraphique(root, adaptateur, controleur)
    root.protocol("WM_DELETE_WINDOW", lambda: [
        setattr(controleur, 'running', False),
        ctrl_thread.join(timeout=0.1),
        root.destroy()
    ])
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
