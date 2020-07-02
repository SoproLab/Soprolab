from machine import Pin # importer la configuration des broches
from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir
    
while Bouton.value() == False: # Tant que le bouton poussoir n'a pas été enfoncé
    d = HCSR.distance_mm   # mesurer la distance
    print("Distance mesurée :", d, "mm") # Afficher le résultat de la mesure
    sleep_ms(300) # temporisation entre deux mesures