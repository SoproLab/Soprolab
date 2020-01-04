# Article en cours de rédaction ...

Dans ce dossier, vous pourrez trouver toutes les bibliothèques microPython nécessaires au bon fonctionnement des modules optionnels de la carte SoproLab.

Ces bibliothèques sont programmées sur le principe de la propragammation orientée objet.
Chaque module est donc considéré comme un "objet" (une instance de classe dans le jargon informatique) sur lequel s'appliquent
 les méthodes qui permettent de communiquer avec le module : [ objet.mesure() ] pour effectuer une mesure par exemple.
 
# ========= Module DS18B20 :
  - Objet : 
      DS
  - Méthode : 
      DS.mesure()
  - Résultat : 
      valeur = DS.temperature

# ========= Module UltraSon Version 1 :
  - Objet : 
      HCSR
  - Méthode :
      valeur = HCSR.distance_mm()
      valeur = HCSR.distance_cm()

# ========= Module UltraSon Version 2 :
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
  - Objet : LCD
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
 
 
