## Mise à jour des bibliothèques SoproLab
<br />
Vous trouverez dans ce dossier une mise à jour du menu de démarrage affiché sur l'écran LCD de la carte SoproLab.
<br />
24/06/2020 : Modification de la bibliothèque menu.py mémorisée dans la mémoire flash de l'ESP32.
<br /> Cette modification permet de détecter que l'écran LCD n'est pas en place. Cela évite les erreurs de démarrage liées à un module qui n'est pas connecté.<br />
La carte démarre donc en mode [programmation Python] par défaut.