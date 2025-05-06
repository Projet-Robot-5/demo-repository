
import math

class Robot:
    def __init__(self, x, y, vitesse_gauche=10, vitesse_droite=10, orientation=0, taille=20):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.wheel_distance = 30
        self.taille = taille
        self.is_moving = False
        self.balise_detectee = False
        self.balise_position = (0, 0)

    def detecter_balise(self, environnement):
        self.balise_detectee = False
        if not hasattr(self, 'environnement') or not hasattr(self.environnement, 'balises'):
            return False

        for balise in environnement.balises:
            distance = math.sqrt((self.x - balise[0])**2 + (self.y - balise[1])**2)
            if distance < 50:
                self.balise_detectee = True
                self.balise_position = balise
                return True
        return False

    def set_wheel_speed(self, vitesse_gauche, vitesse_droite):
        self.vitesse_gauche = vitesse_gauche
        self.vitesse_droite = vitesse_droite
        self.is_moving = (vitesse_gauche != 0 or vitesse_droite != 0)

    def move(self, dt=1):
        if not self.is_moving:
            return

        vitesse_lineaire = (self.vitesse_gauche + self.vitesse_droite) / 2
        angle_rad = math.radians(self.orientation)

        self.x += vitesse_lineaire * math.cos(angle_rad) * dt
        self.y += vitesse_lineaire * math.sin(angle_rad) * dt

        if self.vitesse_gauche != self.vitesse_droite:
            rotation_vitesse = (self.vitesse_droite - self.vitesse_gauche) / self.wheel_distance
            delta_orientation = math.degrees(rotation_vitesse * dt)
            self.orientation += delta_orientation
            self.orientation %= 360

    def stop(self):
        self.vitesse_gauche = 0
        self.vitesse_droite = 0
        self.is_moving = False

    def get_position(self):
        return (self.x, self.y)

    def get_orientation(self):
        return self.orientation

    def get_distance_devant(self, obstacles):
        '''
        Calcule la distance au premier obstacle devant le robot dans un cône de 60°.
        Retourne la distance minimale ou -1 si aucun obstacle dans le cône.
        '''
        x, y = self.x, self.y
        orientation_rad = math.radians(self.orientation)
        dx = math.cos(orientation_rad)
        dy = math.sin(orientation_rad)

        cone_angle = math.radians(60)
        closest_distance = float("inf")

        for ox, oy in obstacles:
            vx = ox - x
            vy = oy - y
            distance = math.hypot(vx, vy)
            if distance == 0:
                continue

            ux = vx / distance
            uy = vy / distance
            dot_product = dx * ux + dy * uy
            angle_diff = math.acos(min(1.0, max(-1.0, dot_product)))

            if angle_diff <= cone_angle / 2:
                if distance < closest_distance:
                    closest_distance = distance

        return round(closest_distance, 2) if closest_distance != float("inf") else -1

    def get_distance_parcourue(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
