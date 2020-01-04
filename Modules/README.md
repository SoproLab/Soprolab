Dans ce dossier, vous pourrez trouver toutes les bibliothèques microPython nécessaires au bon fonctionnement des modules optionnels de la carte SoproLab.

Ces bibliothèques sont programmées sur le principe de la propragammation orientée objet.
Chaque module est donc considéré comme un "objet" (une instance de classe dans le jargon informatique) sur lequel s'appliquent
 les méthodes qui permettent de communiquer avec le module : [ objet.mesure() ] pour effectuer une mesure par exemple.
 
# ========= Module DS18B20 :
Capteur numérique de température
  - Objet : 
      DS
  - Méthode : 
      DS.mesure()
  - Résultat : 
      valeur = DS.temperature

# ========= Module UltraSon Version 1 :
Capteur de distance HCSR04
  - Objet : 
      HCSR
  - Méthode :
      valeur = HCSR.distance_mm()
      valeur = HCSR.distance_cm()

# ========= Module UltraSon Version 2 :
Capteur de distance HCSR04 fixé sur un servo moteur
  - Objets : 
      HCSR
      PIV
  - Méthodes :
      valeur = HCSR.distance_mm()
      valeur = HCSR.distance_cm()
      PIV.direction ( angle, vitesse ) # angle : [ 0, 180] / vitesse : [ 1 ; 10 ]
=== Note ===
Sur la version 2, le capteur de distance est fixé sur un servo moteur orientable sur 180° : l'objet PIV ( pivot ). 

# ========= Module LCD :
Ecran LCD rétroéclairé : 16 caractères / 2 lignes
  - Objet :
      LCD
  - Méthodes : 
      LCD.effacer()
      LCD.texte(" ")
      LCD.place_curseur( x ,y ) # x [ 0; 15 ]  /  y [ 0 - 1 ] (ligne)
      LCD.curseur_on()
      LCD.curseur_off()
      LCD.curseur_blink_on()
      LCD.curseur_blink_off()
      LCD.ecran_off()
      LCD.ecran_on()
      LCD.backlight_off()
      LCD.backlight_on()
      LCD.caractere (' ')
 
 # ========= Module Celerité du son dans l'air :
=> SOPROLAB_celeriteSon.py :
Module pour mesurer la célérité du son dans l'air contenu dans un tuyau PE de 2m.
(tuyau de diamètre 16mm utilisé pour la distribution d'eau dans les habitations)
  - Objets :
      buzzer
      microphone
  - Méthodes : 
      Chrono_µs-on()
      Chronoµs—off()
      buzzer.on ( )
      buzzer.off ( )
      t0 = Chrono_µs—on ( )
      duree = Chrono_µs—off ( ) - t0

=> celerite_son.py
Code microPython pour mesurer la celerite du son dans l'air

 # Autres modules et bibliothèques à venir ....
- Mesure de l'absorption de lumière Rouge/Verte/Bleue
- Mesure de lumière IR / Visilbe / UVA

Plus d infos sur le site : https://j-chouteau.org/index.php/carte-soprolab/
