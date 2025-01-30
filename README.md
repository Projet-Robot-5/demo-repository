# 🚀 **Robot Simulation Project**

Bienvenue dans le **Robot Simulation Project** ! Ce projet contient une simulation de robot interactive. Le robot peut se déplacer, tourner, éviter les obstacles et réagir aux bords du canevas.

---

## ⚠️ **Branche de Test**

Cette branche est **réservée aux tests** seulement. Elle est utilisée pour tester de nouvelles fonctionnalités et expérimentations dans la simulation de robot avant de les intégrer dans la branche principale. 

---

## 📂 **Hiérarchie du package**

Le package principal du projet est `robot_simulation/`. Voici la structure du répertoire :

- **`__init__.py`** : Fichier d'initialisation du package. Ce fichier permet de rendre le dossier `robot_simulation` comme un module Python. Il importe les classes principales nécessaires à l'exécution de la simulation.
  
- **`environnement.py`** : Définit la classe `Environnement` qui crée et gère l'affichage du canevas. Ce fichier contient aussi la logique pour dessiner des obstacles à des positions spécifiques sur le canevas.
  
- **`robot.py`** : Définit la classe `Robot` qui permet de déplacer le robot, de le faire tourner, et d'éviter les obstacles. Le robot peut aussi détecter les bords du canevas pour ne pas en sortir.

- **`simulation.py`** : Ce fichier contient la classe `Simulation`, qui est responsable de la logique de la simulation. Il initialise l'environnement, place le robot, et permet l'interaction avec l'utilisateur via le clavier (les touches fléchées pour déplacer et tourner le robot).

- **`main.py`** : Le fichier principal du programme. Il initialise la fenêtre Tkinter et lance la simulation en appelant la classe `Simulation`.
