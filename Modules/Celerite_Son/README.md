Autheur : Jacques Chouteau </br>
Date de la dernière modification : 12 janvier 2020</br>

Ce dossier contient les fichiers nécessaires à l'utilisation du module Son de la carte SoproLab :</br>
 . SOPROLAB_Son.py -> gestion du module</br>
 . Celerite_son.py -> exemple d'utilisation</br>
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

=> celerite_son.py<br />
Code microPython pour mesurer la celerite du son dans l'air
