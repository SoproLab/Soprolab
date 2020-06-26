## Mise à jour des bibliothèques SoproLab


24/06/2020 : Modification de la bibliothèque " menu.py " mémorisée dans la mémoire flash de l'ESP32.



Vous trouverez dans ce dossier une mise à jour du menu de démarrage affiché sur l'écran LCD de la carte SoproLab.



Pour mettre en place la platine d'étude de charge et décharge d'un condensateur, il est nécessaire de retirer le module LCD.


Cette modification permet de détecter que l'écran LCD n'est pas en place. Cela évite les erreurs de démarrage liées à un module qui n'est pas connecté.<br />


La carte démarre alors en mode " programmation Python " , ce qui permet de lancer la séquence d'échantillonnage de mesures et traiter ensuite les données recueillies.
