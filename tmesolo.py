#TME Solo

def q1_1():
    from robot_simulation.modele.environnement import Environnement
    from robot_simulation.modele.robot import Robot
    from robot_simulation.modele.simulation import Simulation
    from robot_simulation.affichage.affichage_graphique import AffichageGraphique
    import tkinter as tk

    obstacles = [(150, 250), (250, 250), (350, 250)]  # position des 3 obstacles
    environnement = Environnement(obstacles)

    robot = Robot(x=50, y= 450, orientation =0)  # Coin inférieur gauche
    simu = Simulation(robot, environnement)

    root = tk.Tk()
    gui = AffichageGraphique(root, simu.adaptateur, simu.controleur)
    root.mainloop()

def q1_2():
    from robot_simulation.controleur.strategie import StrategieSequencielle, AvancerDroit, Tourner, StrategieConditionnelle
    from robot_simulation.modele.robot import Robot

    # Coin inférieur gauche
    robot = Robot(x=50, y=450, orientation=0)

    actions = []
    for _ in range(10): # Boucle de 10
        actions.append(StrategieConditionnelle(
            condition=lambda adapt: adapt.get_distance_devant() < 30,
            if_true = Tourner(angle=180),  # demi tour
            if_false = AvancerDroit(distance= 50)
        ))

    return StrategieSequencielle(actions)


def q1_3():
    from robot_simulation.controleur.strategie import StrategieSequencielle, AvancerDroit
    from robot_simulation.modele.simulation import Simulation

    def activer_trace(adaptateur):
        adaptateur.robot.dessine(True)

    actions = [
        lambda adapt: activer_trace(adapt),  # Active la trace
        AvancerDroit(distance=100)
    ]

    return StrategieSequencielle(actions)

#robot.py 13-18
#affichege_graphique.py 57-66

#Q1_4
#Robot.py 20-24
def q1_4():
    from robot_simulation.controleur.strategie import StrategieSequencielle, AvancerDroit, Tourner

    def rouge(adapt): adapt.robot.rouge()
    def bleu(adapt): adapt.robot.bleu()
    def activer_trace(adapt): adapt.robot.dessine(True)

    return StrategieSequencielle([
        lambda adapt: activer_trace(adapt),
        lambda adapt: rouge(adapt),
        AvancerDroit(100),
        lambda adapt: bleu(adapt),
        Tourner(90),
        AvancerDroit(100)
    ])


def q1_5():
    from robot_simulation.controleur.strategie import StrategieSequencielle, AvancerDroit, Tourner
    from robot_simulation.controleur.strategie import StrategieBleu, StrategieRouge, StrategieInvisible

    return StrategieSequencielle([
        StrategieRouge(),
        AvancerDroit(100),
        StrategieBleu(),
        Tourner(90),
        AvancerDroit(100),
        StrategieInvisible(),
        Tourner(90),
        AvancerDroit(100)
    ])

# startegie.py 251-283 

def q2_1():
    from robot_simulation.modele.simulation import Simulation
    from robot_simulation.modele.robot import Robot
    from robot_simulation.environnement import Environnement
    from robot_simulation.controleur.controleur import Controleur
    from robot_simulation.controleur.strategie import AvancerDroit
    from robot_simulation.adaptateur.adaptateur_robot_simule import AdaptateurRobotSimule

    # Création de l'environnement avec quelques obstacles (facultatif ici)
    environnement = Environnement(obstacles=[(200, 200), (300, 1000), (150, 300)])

    # Création de la simulation
    sim = Simulation(environnement)

    # Création du robot chat (trace rouge)
    chat = Robot(x=50, y=50, orientation=0)  # Coin supérieur gauche
    chat.couleur_trace = "red""
    adaptateur_chat = AdaptateurRobotSimule(chat, environnement)
    strategie_chat = AvancerDroit(distance= 100)
    controleur_chat = Controleur(adaptateur_chat, starategie_chat)
    sim.ajouter_robot(chat, controleur_chat)

    # Démarrer la simulation
    sim.lancer()







