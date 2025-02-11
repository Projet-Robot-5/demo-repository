import sys
import tkinter as tk 
from affichage_graphique import AffichageGraphique



def main():
    """Initialiser et démarrer la simulation."""
    if "--no-gui" in sys.argv:
        print("Mode sans interface graphique activé")
        simulation = Simulation()
        simulation.run()
        return #Quitte la fonction apres l'execution de la simulation
    
    
    # Mode normal utilisant l'interface graphique
    racine = tk.Tk()  # Créer la fenêtre principale
    racine.title("Simulation de Robot")
    simulation = AffichageGraphique(racine)  # Créer et lancer la simulation
    racine.mainloop()  # Lancer la boucle Tkinter


if __name__ == "__main__":
    main()