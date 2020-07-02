from machine import Pin # importer la configuration des broches
from time import sleep_us # importer la fonction d'attente en microsecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

Buzzer = Pin ( 25, Pin.OUT ) # Broche reliée au buzzer
Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir

periode = 2500 # Par défaut période = 2500µs (obstacle au delà de 500mm)

while Bouton.value() == False: # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm # mesurer la distance
    
    if d < 100 : # distance inférieure à 100mm
        periode = 470
        for cptr in range(400):
            Buzzer.on() # produire 400 périodes de 470 µs
            sleep_us(235)
            Buzzer.off()
            sleep_us(235)
    elif d<200: # distance comprise entre 100mm et 200mm
        periode = 970
        for cptr in range(400):
            Buzzer.on() # produire 400 périodes de 970 µs
            sleep_us(485)
            Buzzer.off()
            sleep_us(485)
    elif d<300: # distance comprise entre 200mm et 300mm
        periode = 1470
        for cptr in range(400):
            Buzzer.on() # produire 400 périodes de 1470 µs
            sleep_us(735)
            Buzzer.off()
            sleep_us(735)
    elif d<400: # distance comprise entre 300mm et 400mm
        periode = 1970
        for cptr in range(400):
            Buzzer.on() # produire 400 périodes de 1970 µs
            sleep_us(985)
            Buzzer.off()
            sleep_us(985)
    elif d<500: # distance comprise entre 400mm et 500mm
        periode = 2470
        for cptr in range(400):
            Buzzer.on() # produire 400 périodes de 2470 µs
            sleep_us(1235)
            Buzzer.off()
            sleep_us(1235)
    sleep_us ( 200*periode) # attendre 400 fois la période du son