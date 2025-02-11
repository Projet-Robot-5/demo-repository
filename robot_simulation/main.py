import tkinter as tk
from affichage_graphique import AffichageGraphique



def main():
    """Initialiser et démarrer la simulation."""
    racine = tk.Tk()  # Créer la fenêtre principale
    racine.title("Simulation de Robot")
    simulation = AffichageGraphique(racine)  # Créer et lancer la simulation
    racine.mainloop()  # Lancer la boucle Tkinter


if __name__ == "__main__":
    main()