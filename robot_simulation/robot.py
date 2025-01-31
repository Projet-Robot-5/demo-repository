import math

class Robot:
    def __init__(self, canevas, x=50, y=50, taille=20, angle=0):
        """Initialise le robot avec ses propriétés, y compris l'angle de rotation."""
        self.canevas = canevas
        self.x = x
        self.y = y
        self.taille = taille
        self.angle = angle  # L'angle du robot pour la rotation
        self.robot = self.canevas.create_oval(x, y, x + taille, y + taille, fill="blue")

    def deplacer(self, dx, dy):
        """Déplacer le robot de dx, dy."""
        self.canevas.move(self.robot, dx, dy)
        self.x += dx
        self.y += dy

    def tourner(self, direction="gauche"):
        """Faire tourner le robot à gauche ou à droite."""
        if direction == "gauche":
            self.angle -= 15  # Tourner à gauche de 15 degrés
        elif direction == "droite":
            self.angle += 15  # Tourner à droite de 15 degrés

        # Limiter l'angle entre 0 et 360 degrés
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

    def avancer(self, distance=10):
        """Avancer dans la direction du robot."""
        # Calculer les nouvelles coordonnées en fonction de l'angle
        radian = math.radians(self.angle)
        dx = distance * math.cos(radian)
        dy = distance * math.sin(radian)

        self.deplacer(dx, dy)

    def detecter_obstacle(self, obstacles, distance=30):
        """Détecter si un obstacle est à proximité."""
        radian = math.radians(self.angle)
        dx = distance * math.cos(radian)
        dy = distance * math.sin(radian)

        # Vérifier si un obstacle est dans le rayon de détection
        for obs in obstacles:
            ox, oy = obs
            if abs(self.x + dx - ox) < self.taille and abs(self.y + dy - oy) < self.taille:
                return True  # Un obstacle est détecté
        return False

    def detecter_bordure(self, largeur_canvas, hauteur_canvas):
        """Vérifier si le robot atteint le bord du canevas."""
        if self.x <= 0 or self.x >= largeur_canvas - self.taille or self.y <= 0 or self.y >= hauteur_canvas - self.taille:
            return True  # Le robot atteint le bord
        return False
    def eviter_obstacle(self,obstacles,largeur_canvas,hauteur_canvas):
        """eviter un obstacle en tournant à gauche ou à droite"""
        if self.detecter_obstacle(obstacles):
            #Tourner à droite si un obstacle est détecté
            self.tourner("droite")
        elif self.detecter_bordure(largeur_canvas,hauteur_canvas):
            #Tourner à gauche si le robot atteint le bord
            self.tourner("gauche")
        else:
            #Avancer si aucun oobstacle ou bordure n'est detecté
            self.avancer(10)
    
   
