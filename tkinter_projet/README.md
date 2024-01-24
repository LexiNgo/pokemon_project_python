REPARTITION DES RESPONSABILITES :

Julie et Alireza se sont occupés de la partie django pour le front
Jean, Christian et Lexi se sont occupés de la partie tkinter et de la partie back.


FONCTIONNEMENT DE L'APPLICATION :

Au démarrage de l'application, la fenêtre tkinter s'ouvre présentant 02 options 
"Pokedex" et "Combat"

En cliquant sur Pokedex, une autre interface s'affiche : ceci permet de faire les recherches
concernant un pokémon;

En cliquant sur Combat, une interface s'affiche : elle presente les deux pokémons qui
devront s'affronter. Le déroulé du combat se fait sur un terminal graphique.


Installation de django
Avec la commande pip install django
Configuration de la base de données avec la commande python manage.py migrate
Lancement du serveur avec python manage.py runserver
On a décidé de faire deux projets pour deux raisons, pour découvrir toutes les facettes de python dont tkinter et django
Et seconde raison pour la difficulté rencontré lors de la partie combat qui ne pouvait être fait en django
Toutes les fonctionnalités du pokedex se déroulent en django
Et les fonctionnalités liées à l'équipe (Team) se déroulent aussi en django
Seulement la partie combat se déroule sur tkinter où l'on sélectionne nos équipes pour s'affronter


