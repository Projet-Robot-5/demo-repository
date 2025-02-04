import tkinter as tk
from simulation import Simulation


def main():
    """Initialiser et démarrer la simulation."""
    racine = tk.Tk()  # Créer la fenêtre principale
    racine.title("Simulation de Robot")
    simulation = Simulation(racine)  # Créer et lancer la simulation
    racine.mainloop()  # Lancer la boucle Tkinter


if __name__ == "__main__":
    main()