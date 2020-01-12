from SOPROLAB import *
from SOPROLAB_LCD import *

def Attendre ( texte ):
    print( texte )
    while BP.impulsion==False:
        continue
    sleep_ms(200)

Attendre("Appuyez sur le bouton poussoir entre chaque test ...")

LCD.effacer()
LCD.texte("    SoproLab")
LCD.place_curseur(3,1)
LCD.texte("Module LCD")

print(" Soprolab")
Attendre("Module LCD ")

LCD.effacer()
Attendre(" LCD.effacer() ")

LCD.curseur_on()
Attendre(" LCD.curseur_on() ")

LCD.curseur_off()
Attendre(" LCD.curseur_off() ")

LCD.curseur_blink_on()
Attendre(" LCD.curseur_blink_on() ")

LCD.curseur_blink_off()
Attendre(" LCD.curseur_blink_off() ")

LCD.texte("Bonjour le monde")
Attendre("...")
LCD.ecran_off()
Attendre(" LCD.ecran_off() ")

LCD.ecran_on()
Attendre(" LCD.ecran_on() ")

LCD.backlight_off()
Attendre(" LCD.backlight_off() ")

LCD.backlight_on()
Attendre(" LCD.backlight_on() ")

LCD.effacer()
LCD.curseur_on()
LCD.place_curseur (6, 1)
Attendre(" LCD.place_curseur (6, 1) # [6] -> 6eme colonne (X), [1] -> 2eme ligne (Y)")
LCD.curseur_off()

LCD.caractere ( 'A' )
Attendre(" LCD.caractere(\'A\') ")

LCD.place_curseur(5,1)
LCD.texte("Au revoir ")
LCD.caractere ( chr(1) )
