# Py-demie

# Lancer le jeu :
Dans le dossier Py-demie : exécuter "python -m Game.Game"


# Reste à faire :
- ## Kylian : 
    - ### Gestion des reproductions et des naissances :
        Mettre une probabilité vraiment petite d'une naissance en cas de 2 personnes à cotés de sexe HOMME et FEMME.
        Mettre un age petit et verif qu'il ne peux pas procréer tout de suite.
    - ### Déplacement en meme temps :
        Tous les humains doivent se déplacer en meme temps.
        Pour se faire, on va créer une deuxième matrice qui va calculer le nombre de personnes qui ont décidés d'aller sur une même case.
        Dans ce cas là, un des humains sera désignés et les autres resteront immobiles. 
        Pour cela, il faut copier la matrice actuelle et prédire les mouvements en fonction des cases actuellement disponibles.
        ATTENTION : dans le cas de plusieurs personnes qui souhaitent aller sur une meme case, il ne faut pas prendre le premier humain et il a une chance sur le nombre d'huamains. il faut faire un random.choice sur la liste
