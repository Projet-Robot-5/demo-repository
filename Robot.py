class Environnement :
    def __init__(self,largeur,hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille =[["." for _ in range(largeur)]for _ in range (hauteur)]
    def afficher (self,robot):
        for y in range (self.hauteur):
            for x in range(self.largeur):
                if (x,y)==(robot.x,robot.y):
                    print("R",end=" ")
                else:
                    print(self.grille[y][x],end=" ")
            print()
        print()
     

class Robot:
    def __init__(self,x,y,environnement,vitesse=1):
        self.x = x
        self.y = y
        self.env = environnement
        self.vitesse = vitesse
        self.position = (0,0)
        self.parcours=[self.position]
        self.env.afficher(self)
        
    """def avancer(self):
        if self.orientation == "N" and self.y > 0: 
            self.y -= 1
        elif self.orientation == "S" and self.y < self.env.hauteur - 1:
            self.y += 1
        elif self.orientation == "E" and self.x < self.env.largeur - 1:
            self.x += 1
        elif self.orientation == "O" and self.x > 0:
            self.x -= 1
    def tourner_droite(self):
        directions = ["N","E","S","O"]
        i = (directions.index(self.orientation) + 1) % 4
        self.orientation = directions[i]
    def tourner_gauche(self):
        directions = ["N","E","S","O"]
        i = (directions.index(self.orientation) - 1) % 4
        self.orientation = directions[i]"""
    """def deplacer(self,x,y):
        self.position =(x,y)
        self.parcours.append(self.position)""" 
    def parcourir_grille(self):
        for ligne in range (self.env.largeur):
            if ligne % 2 == 0:
                for col in range (self.env.hauteur):
                    self.deplacer(ligne,col)
            else:
                for col in range (self.env.hauteur-1,-1,-1):
                    self.deplacer(ligne,col)
                    
    def afficher(self):
        
        for pos in self.parcours:
            print(pos)
            
def deplacer(self, angle):
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
        else:
            print("Obstacle ou limite atteinte ! Le robot s'arrête.")

    def afficher_position(self):
        print(f"Position actuelle : ({self.x}, {self.y})")


# Initialisation
largeur = 5
hauteur = 5
env = Environnement(largeur, hauteur)

# Position initiale du robot
x = 0
y = 0
robot = Robot(x, y, env)

# Entrée utilisateur pour la vitesse et l'angle
vitesse = int(input("Entrez la vitesse du robot (en unités par pas) : "))
angle = int(input("Entrez l'angle de déplacement (en degrés) : "))
robot.vitesse = vitesse

# Déplacement du robot
while True:
    robot.deplacer(angle)
    env.afficher(robot)
    robot.afficher_position()
    continuer = input("Voulez-vous continuer (o/n) ? ").lower()
    if continuer != 'o':
        break
    
largeur = 5
hauteur = 5
env = Environnement(largeur,hauteur)
x=0
y=0


robot = Robot(x,y,env,vitesse=1)

env.afficher(robot)
robot.parcourir_grille()
env.afficher(robot)

robot.afficher()
