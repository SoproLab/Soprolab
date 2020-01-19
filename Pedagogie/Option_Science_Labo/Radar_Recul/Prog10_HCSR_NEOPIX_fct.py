from machine import Pin # importer la configuration des broches
from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons
from SOPROLAB import * # importer la bibliothèque pour gérer les diodes NEOPIXEL

Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir

NEOPIX[0] = (0, 140, 0 ) # Allumer la première diode NeoPixel en vert
for n in range ( 1, 8 ):
    NEOPIX[n] = ( 0, 0, 0 ) # Eteindre les autres diodes NeoPixel
NEOPIX.write()

def Gestion_Neopix ( n ):
    for i in range ( 1, 9-n ): # pour les i premières led NEOPIXEL
        NEOPIX[i] = ( 20*i, 140-20*i, 0)
    for i in range (9-n, 8): # éteindre les autres led NEOPIXEL
        NEOPIX[i] = (0, 0, 0)
    NEOPIX.write()
    
while Bouton.value() == False: # Tant que le bouton poussoir n'a pas été enfoncé
    d = HCSR.distance_mm( )    # mesurer la distance
    n = 1 + d // 100 # indice de l'intervalle -> 100mm -> n=1  // 200mm -> n=2 // ...
    if n < 9:  # Si la distance mesurée est dans un des huit premiers intervalles
        Gestion_Neopix ( n )

    sleep_ms(100) # temporisation entre deux mesures
    
for n in range ( 8 ):
    NEOPIX[n] = ( 0, 0, 0 ) # Eteindre les diodes NeoPixel
NEOPIX.write()