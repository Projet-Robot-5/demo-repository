import tkinter as tk
import math
from .simulation import Simulation


class AffichageGraphique:
    def __init__(self, master):
        """Initialise l'affichage graphique de la simulation."""
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="white")
        self.canvas.pack()

        self.simulation = Simulation()
        if self.simulation.robot is None or self.simulation.environnement is None:
            raise ValueError(
                "Simulation non initialisée correctement ! Vérifiez l'initialisation de robot et environnement.")

        self.update_affichage()

        # 🔹 Ajout du bouton Reset ici
        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_simulation)
        self.reset_button.pack()

    def reset_simulation(self):
        """Réinitialise la simulation et met à jour l'affichage."""
        self.simulation = Simulation()
        self.update_affichage()  # Redémarrer l'affichage

    def update_affichage(self):
        """Met à jour l'affichage graphique du robot."""
        self.simulation.update()  # Utiliser update_all() qui synchronise tout
        self.canvas.delete("all")

        # Dessiner les obstacles
        for obs in self.simulation.environnement.obstacles:
            self.canvas.create_oval(obs[0] - 5, obs[1] - 5, obs[0] + 5, obs[1] + 5, fill="red")

        # Dessiner le robot
        x, y = self.simulation.robot.x, self.simulation.robot.y
        self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="blue")

        self.master.after(50, self.update_affichage)


if __name__ == "__main__":
    root = tk.Tk()
    app = AffichageGraphique(root)
    root.mainloop()
