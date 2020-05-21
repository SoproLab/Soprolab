## Mise à jour des bibliothèques SoproLab
<br />
Vous trouverez dans ce dossier les mises à jour des bibliothèques SoproLab.
<br />
21/05/2020 : dépôts des bibliothèque microWebServer_V1. (Cf Jean-Christophe BOS : https://github.com/jczic/MicroWebSrv ). 
**Ici c'est la version 1 qui est mise en oeuvre**
microWebSocket.py. 
microWebSrv.py. 
microWebTemplate.py. 

**P8_Serveur_Web.py** -> Menu de démarrage appelé par menu.py. 
	il faut modifier les lignes 29 et 30 : SSID et mot de passe Wifi
	
**start.py** -> Fichier de démarrage et de gestion des méthodes GET et POST

**Le dossier www** contient les fichiers index.hmtl ... 

**Appels au serveur :**. 
*IP_SoproLab/* -> index.html avec un lien vers page 2.html et réciproquement. 
*IP_SoproLab/*wstest.html -> microWebSocket ( JavaScript ). 
*IP_SoproLab/*formGET -> formulaire renvoyé avec la méthode GET (mot de passe : NSI). 
*IP_SoproLab/*formPOST -> formulaire renvoyé avec la méthode POST (mot de passe : NSI). 
*IP_SoproLab/*led/... -> contrôle des led rouge / jaune / verte (Cf start.py ). 
*IP_SoproLab/*LCD/... -> affichage d'un texte sur l'écran LCD (Cf start.py )