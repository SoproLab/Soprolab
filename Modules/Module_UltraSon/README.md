<a href="https://github.com/SoproLab/Soprolab/tree/master/Pedagogie/Option_Science_Labo/Radar_Recul"> Exemple d'activité pédagogique : radar de recul </a>

# ========= Module UltraSon Version 1 :
Capteur de distance HCSR04
  - Objet : <br />
      HCSR
  - Méthode : <br />
      valeur = HCSR.distance_mm()<br />
      valeur = HCSR.distance_cm()<br />

# ========= Module UltraSon Version 2 :
Capteur de distance HCSR04 fixé sur un servo moteur
  - Objets : <br />
      HCSR<br />
      PIV
  - Méthodes :<br />
      valeur = HCSR.distance_mm()<br />
      valeur = HCSR.distance_cm()<br />
      PIV.direction ( angle, vitesse ) # angle : [ 0, 180] / vitesse : [ 1 ; 10 ]
=== Note ===<br />
Sur la version 2, le capteur de distance est fixé sur un servo moteur orientable sur 180° : l'objet PIV ( pivot ). 

------  Sources : </br>
http://www.micropython.org<br />
section forum ....
