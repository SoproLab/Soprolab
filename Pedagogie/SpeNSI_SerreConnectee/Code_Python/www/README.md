### Cahier des charges

Le cahier des charges (objectif n°1) est de passer de la première version :<br />
<div align="center">
  
![IHM de base](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/Code_Python/www/Presentation_1.jpg)
</div>
à une version ou un seul bouton s'affiche selon la position de la trappe d'aération :
- si la trappe est ouverte le bouton OUVRIR doit être caché,
- si la trappe est fermée, le bouton FERMER doit être caché.
<div align="center">
  
![IHM version 2](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/Code_Python/www/Objectif_1.jpg)
</div>
Pour cela, le javascript ajoutera une classe .hidden au bouton adhoc selon l'état de la trappe.<br>
C'est le code Python qui placera l'état de la trappe dans le fichier javascript pour initialiser la variable **toit** avant d'envoyer le tout au navigateur du client via la connexion wifi.
