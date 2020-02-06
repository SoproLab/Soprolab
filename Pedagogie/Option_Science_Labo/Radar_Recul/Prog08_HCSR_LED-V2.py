from SOPROLAB import *
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

BP.drapeau = False
while BP.drapeau == False: # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm( )    # mesurer la distance
    
    if d > 300 : # Si la distance est supérieure à 1000 mm alors
        LED_v.on()  # Allumer la LED verte et éteindre les autres LED
        LED_j.off()
        LED_r.off()
    elif d>150:   # sinon, si la distance [ 500mm ;  1000mm ]
        LED_v.on()  # Allumer la LED verte, et jaune et éteindre la LED rouge
        LED_j.on()
        LED_r.off()
    else : # sinon
        LED_v.on() # Allumer les trois LED
        LED_j.on()
        LED_r.on()
    sleep_ms ( 100 )    # attendre 200 ms
LED_v.off()
LED_j.off()
LED_r.off()
