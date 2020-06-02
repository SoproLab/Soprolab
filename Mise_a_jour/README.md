## Mise à jour des bibliothèques SoproLab
<br />
Vous trouverez dans ce dossier les mises à jour des bibliothèques SoproLab.
<br />
21/05/2020 : dépôts des bibliothèque microWebServer_V1. (Cf Jean-Christophe BOS : https://github.com/jczic/MicroWebSrv )<br />
<strong>Ici c'est la version 1 qui est mise en oeuvre</strong><br />
+ microWebSocket.py<br />
+ microWebSrv.py<br />
+ microWebTemplate.py<br /> 
<br />
+ P8_Serveur_Web.py -> Menu de démarrage appelé par menu.py<br />
	il faut modifier les lignes 29 et 30 : SSID et mot de passe Wifi<br />
<br />
+ start.py -> Fichier de démarrage du serveur Web<br />
	++ gestion des méthodes GET et POST<br />
	++ contrôle des LED rouge / jaune / verte<br />
	++ contrôle de l'écran LCD<br />
<br />
+ Le dossier www contient des fichiers hmtl ... <br />
<br />
**Appels au serveur :**<br />
+ IP_SoproLab/ -> index.html avec un lien vers page 2.html et réciproquement<br />
+ IP_SoproLab/wstest.html -> microWebSocket ( JavaScript )<br />
+ IP_SoproLab/formGET -> formulaire renvoyé avec la méthode GET (mot de passe : NSI)<br />
+ IP_SoproLab/formPOST -> formulaire renvoyé avec la méthode POST (mot de passe : NSI)<br />
+ IP_SoproLab/led/... -> contrôle des led rouge / jaune / verte (Cf start.py )<br />
+ IP_SoproLab/LCD/... -> affichage d'un texte sur l'écran LCD (Cf start.py )<br />
==============================
