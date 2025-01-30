import tkinter as tk

class Environnement:
    def __init__(self, racine, largeur=500, hauteur=500):
        """Initialise l'environnement et le canevas."""
        self.racine = racine  # La fenêtre principale (Tkinter)
        self.largeur = largeur  # Largeur de l'environnement
        self.hauteur = hauteur  # Hauteur de l'environnement
        self.canevas = tk.Canvas(racine, width=self.largeur, height=self.hauteur, bg="white")
        self.canevas.pack()

    def dessiner_obstacle(self, x, y, taille=20):
        """Dessiner un obstacle à la position (x, y)."""
        self.canevas.create_rectangle(x, y, x + taille, y + taille, fill="black")

    def obtenir_canevas(self):
        """Retourner le canevas pour l'utiliser dans d'autres parties."""
        return self.canevas
