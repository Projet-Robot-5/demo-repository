class Environnement :
    def __init__(self,largeur,hauteur):
        self.largeur = largeur
        self.hauteur = hauteur
        self.grille =[["_" for _ in range(largeur)]for _ in range (hauteur)]
    def afficher (self,robot):
        for y in range (self.hauteur):
            for x in range(self.largeur):
                if (x,y)==(robot.x,robot.y):
                    print(robot.orientation,end=" ")
                else:
                    print(self.grille[y][x],end=" ")
            print()
        print()

class Robot:
    def __init__(self,x,y,orientation,environnement):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.env = environnement
    def avancer(self):
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
        self.orientation = directions[i]
    
largeur = 12
hauteur = 12
env = Environnement(largeur,hauteur)
x=5
y=0


robot = Robot(x,y,"N",env)

env.afficher(robot)
robot.avancer()

robot.tourner_droite()
robot.avancer()
env.afficher(robot)