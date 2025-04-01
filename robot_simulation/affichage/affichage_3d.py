import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class Affichage3D:
    def __init__(self, adaptateur, controleur):
        self.adaptateur = adaptateur
        self.controleur = controleur
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([0, 500])
        self.ax.set_ylim([0, 500])
        self.ax.set_zlim([0, 500])
        self.trajet = []