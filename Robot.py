import math

class Environnement:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille = [["." for _ in range(largeur)] for _ in range(hauteur)]

    def afficher(self, robot):
        for y in range(self.hauteur):
            for x in range(self.largeur):
                if (x, y) == (robot.x, robot.y):
                    print("R", end=" ")
                else:
                    print(self.grille[y][x], end=" ")
            print()
        print()


class Robot:
    def __init__(self, x, y, environnement, vitesse=1):
        self.x = x
        self.y = y
        self.env = environnement
        self.vitesse = vitesse
        self.position = (x, y)
        self.parcours = [self.position]
        self.env.afficher(self)

    def se_deplacer(self, angle):
        # Conversion de l'angle en radians
        angle_rad = math.radians(angle)
        # Calcul des nouveaux déplacements
        dx = round(self.vitesse * math.cos(angle_rad))
        dy = round(self.vitesse * math.sin(angle_rad))
        # Nouvelles positions
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérification des limites de la grille
        if 0 <= new_x < self.env.largeur and 0 <= new_y < self.env.hauteur:
            self.x = new_x
            self.y = new_y
            self.parcours.append((self.x, self.y))
            return True  # Déplacement réussi
        else:
            print("Obstacle ou limite atteinte ! Veuillez choisir un nouvel angle.")
            return False  # Déplacement échoué

    def afficher_position(self):
        print(f"Position actuelle : ({self.x}, {self.y})")

    def afficher_parcours(self):
        print("Parcours du robot :")
        for pos in self.parcours:
            print(pos)


# Initialisation
largeur = 5
hauteur = 5
env = Environnement(largeur, hauteur)

# Position initiale du robot
x = 0
y = 0
robot = Robot(x, y, env)

# Entrée utilisateur pour la vitesse
vitesse = int(input("Entrez la vitesse du robot (en unités par pas) : "))
robot.vitesse = vitesse

# Déplacement du robot
while True:
    # Saisir l'angle
    angle = int(input("Entrez l'angle de déplacement (en degrés) : "))

    # Tenter de déplacer le robot jusqu'à ce qu'un déplacement valide soit fait
    while not robot.se_deplacer(angle):
        angle = int(input("Veuillez entrer un nouvel angle : "))

    # Afficher la grille et la position actuelle du robot
    env.afficher(robot)
    robot.afficher_position()

    # Demander si l'utilisateur souhaite continuer
    continuer = input("Voulez-vous continuer (o/n) ? ").lower()
    if continuer != 'o':
        break

# Affichage final du parcours
robot.afficher_parcours()

    

