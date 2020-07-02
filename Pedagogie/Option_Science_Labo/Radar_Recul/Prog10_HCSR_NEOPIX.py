from machine import Pin # importer la configuration des broches
from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons
from SOPROLAB_V2 import * # importer la bibliothèque pour gérer les diodes NEOPIXEL

NEOPIX.LED[0] = (0, 140, 0) # Configurer la diode NEOPIXEL[0] avec ( 0, 140, 0 )

BP.drapeau = False

while not BP.drapeau : # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm # mesurer la distance
    
    if d>700 : # Si distance est supérieure à 700mm alors
        for n in range ( 1, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 1 à 7 ] incluses
    elif d>600: # sinon, si la distance est supérieure à 600 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        for n in range ( 2, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 2 à 7 ] incluses
    elif d>500: # sinon, si la distance est supérieure à 500 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        for n in range ( 3, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 3 à 7 ] incluses
    elif d>400: # sinon, si la distance est supérieure à 400 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        NEOPIX.LED[3] = ( 60,  80, 0) # configurer la NEOPIXEL [ 3 ] 
        for n in range ( 4, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 4 à 7 ] incluses
    elif d>300: # sinon, si la distance est supérieure à 300 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        NEOPIX.LED[3] = ( 60,  80, 0) # configurer la NEOPIXEL [ 3 ] 
        NEOPIX.LED[4] = ( 80,  60, 0) # configurer la NEOPIXEL [ 4 ] 
        for n in range ( 5, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 5 à 7 ] incluses
    elif d>200: # sinon, si la distance est supérieure à 200 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        NEOPIX.LED[3] = ( 60,  80, 0) # configurer la NEOPIXEL [ 3 ] 
        NEOPIX.LED[4] = ( 80,  60, 0) # configurer la NEOPIXEL [ 4 ] 
        NEOPIX.LED[5] = (100,  40, 0) # configurer la NEOPIXEL [ 5 ] 
        for n in range ( 6, 8 ):
            NEOPIX.LED[n] = (0, 0, 0) # éteindre les NEOPIXELS [ 6 à 7 ] incluses
    elif d>100: # sinon, si la distance est supérieure à 100 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        NEOPIX.LED[3] = ( 60,  80, 0) # configurer la NEOPIXEL [ 3 ] 
        NEOPIX.LED[4] = ( 80,  60, 0) # configurer la NEOPIXEL [ 4 ] 
        NEOPIX.LED[5] = (100,  40, 0) # configurer la NEOPIXEL [ 5 ] 
        NEOPIX.LED[6] = (120,  20, 0) # configurer la NEOPIXEL [ 6 ] 
        NEOPIX.LED[7] = (  0,   0, 0) # éteindre la NEOPIXEL [ 7 ] 
    else : # sinon, si la distance est inférieur à 100 mm
        NEOPIX.LED[1] = ( 20, 120, 0) # configurer la NEOPIXEL [ 1 ] 
        NEOPIX.LED[2] = ( 40, 100, 0) # configurer la NEOPIXEL [ 2 ] 
        NEOPIX.LED[3] = ( 60,  80, 0) # configurer la NEOPIXEL [ 3 ] 
        NEOPIX.LED[4] = ( 80,  60, 0) # configurer la NEOPIXEL [ 4 ] 
        NEOPIX.LED[5] = (100,  40, 0) # configurer la NEOPIXEL [ 5 ] 
        NEOPIX.LED[6] = (120,  20, 0) # configurer la NEOPIXEL [ 6 ] 
        NEOPIX.LED[7] = (140,   0, 0) # configurer la NEOPIXEL [ 7 ]
    NEOPIX.LED.write() # mettre à jour l'état des diodes NEOPIXEL
    
    sleep_ms ( 50 ) # Attendre 300ms entre deux mesures

NEOPIX.eteindre()