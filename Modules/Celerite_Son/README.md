## ! Attention ce dossier utilise une version obsolète de la bibliothèque SoproLab.py
Une mise à jour est nécessaire suite à l'évolution de la carte SoproLab vers la version 2
 <i>Dorénavant le module LCD est placé sur le microcontrôleur. Il peut être considéré comme intégré à la carte. <br />
 De ce fait les bibliothèques du module LCD sont intégrées à la bibliothèque principale qui devient SoproLab_V2.py
 Par conséquent il est nécessaire que ce dossier soit mis à jour ( mise à jour programmée pour mi-mai 2020 - ...)
 Il est possible de me contacter si besoin pour obtenir une version mise à jour plus rapidement ...</i>

Autheur : Jacques Chouteau </br>
Date de la dernière modification : 18 janvier 2020</br>

Ce dossier contient les fichiers nécessaires à l'utilisation du module Son de la carte SoproLab :</br>
 . SOPROLAB_Son.py -> gestion du module (buzzer et microphone en programmation objet)</br>
 . Celerite_son.py -> exemple d'utilisation avec affichage dans la Console USB</br>
 . Celerite_son_LCD.py -> exemple d'utilisation avec affichage sur le module LCD et dans la Console USB</br>
 . quelques images pour visualiser ( mises à jour à venir ...)</br>
 
Un exemple de séance pédagogique avec différenciation peut être construit de la façon suivante :
# 1) Niveau Très simple :
  Donner un code complet à l'élève ( version simplifiée par rapport à l'exemple )</br>
  Lancer l'acquisition des mesures</br>
  Lui demander de commenter certains passages du code et des mesures affichées ( calcul de la célérité par exemple )

# 2) Niveau Fragile :
  Donner le code incomplet et certaines parties sont à compléter</br>
  Lancer l'acquisition des mesures</br>
  Lui demander de commenter certains passages du code et des mesures affichées ( calcul de la célérité par exemple )  

# 3) Niveau Satisfaisant :
  Donner une fiche ressource avec les fonctions disponibles dans la bibliothèque [ SOPROLAB_Son.py ]</br>
  Demander l'algorithme du programme</br>
  Coder le programme

# En complément :
  La mesure est effectuée 10 fois.</br>
  Calculer la célérité du son en prenant en compte l'incertitude de mesure.
  
# Pour aller plus loin : 
 Lorsque le code fonctionne, demander à l'élève de produire une version différente avec comme objectif :</br>
 MESURER LA LONGUEUR D'UN TUYAU EN CONNAISSANT LA CÉLÉRITÉ DU SON ET LE TEMPS DE PROPAGATION DE L'ONDE SONORE.
 
 - Mesurer la température ambiante </br>
 - Calculer la célérité du son théorique</br>
 - Mesurer le temps de propagation de l'onde sonore</br>
 - En déduire la longueure du tuyau.</br>
 - Vérifier le bon fonctionnement du code avec le tuyau de 2m</br>
 - Tester avec un tuyau de longueur inconnue et comparer avec un mètre ruban.</br>
 
 Y a plus qu'à ...  ;-)
 
 
 # ========= Module Celerité du son dans l'air :
=> SOPROLAB_celeriteSon.py :<br />
Module pour mesurer la célérité du son dans l'air contenu dans un tuyau PE de 2m.<br />
(tuyau de diamètre 16mm utilisé pour la distribution d'eau dans les habitations)<br />
  - Objets :<br />
      buzzer<br />
      microphone<br />
  - Méthodes : <br />
      Chrono_µs-on()<br />
      Chronoµs—off()<br />
      buzzer.on ( )<br />
      buzzer.off ( )<br />
      t0 = Chrono_µs—on ( )<br />
      duree = Chrono_µs—off ( ) - t0<br />

=> celerite_son.py et celerite_son_LCD.py<br />
Code microPython pour mesurer la celerite du son dans l'air
