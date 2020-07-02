from machine import Pin # importer la configuration des broches
from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

ledv = Pin ( 12, Pin.OUT) # Broche reliée à la LED verte
ledj = Pin ( 13, Pin.OUT) # Broche reliée à la LED jaune
ledr = Pin ( 14, Pin.OUT) # Broche reliée à la LED rouge
Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir

while Bouton.value() == False: # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm    # mesurer la distance
    
    if d > 1000 : # Si la distance est supérieure à 1000 mm alors
        ledv.on()  # Allumer la LED verte et éteindre les autres LED
        ledj.off()
        ledr.off()
    elif d>500:   # sinon, si la distance [ 500mm ;  1000mm ]
        ledv.on()  # Allumer la LED verte, et jaune et éteindre la LED rouge
        ledj.on()
        ledr.off()
    else : # sinon
        ledv.on() # Allumer les trois LED
        ledj.on()
        ledr.on()
    sleep_ms ( 200 )    # attendre 200 ms