from machine import Pin # importer la configuration des broches
from time import sleep_us # importer la fonction d'attente en microsecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

Buzzer = Pin ( 25, Pin.OUT ) # Broche reliée au buzzer
Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir

periode = 2500 # Par défaut période = 2500µs (obstacle au delà de 500mm)

def Produire_son ( periode ):
    demie_periode = periode // 2
    for cptr in range(400):
        Buzzer.on() # produire 400 périodes
        sleep_us ( demie_periode )
        Buzzer.off()
        sleep_us ( demie_periode )
    sleep_us ( periode * 200 ) # silence entre deux "beep"
    
while Bouton.value() == False: # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm # mesurer la distance
    
    if d < 100 : # distance inférieure à 100mm
        Produire_son ( 470 )
    elif d>=100 and d<200: # distance comprise entre 100mm et 200mm
        Produire_son ( 970 )
    elif d>=200 and d<300: # distance comprise entre 200mm et 300mm
        Produire_son ( 1470 )
    elif d>=300 and d<400: # distance comprise entre 300mm et 400mm
        Produire_son ( 1970 )
    elif d>=400 and d<500: # distance comprise entre 100mm et 200mm
        Produire_son ( 2470 )
    sleep_us ( 10000 ) # temporisation minimum de 10ms entre deux mesures