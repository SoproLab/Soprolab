from machine import Pin # importer la configuration des broches
from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons
from SOPROLAB_V2 import * # importer la bibliothèque pour gérer les diodes NEOPIXEL

NEOPIX.LED[0] = (0, 140, 0 ) # Allumer la première diode NeoPixel en vert
for n in range ( 1, 8 ):
    NEOPIX.LED[n] = ( 0, 0, 0 ) # Eteindre les autres diodes NeoPixel
NEOPIX.LED.write()

def Gestion_Neopix ( n ):
    for i in range ( 1, 9-n ): # pour les i premières led NEOPIXEL
        NEOPIX.LED[i] = ( 20*i, 140-20*i, 0)
    for i in range (9-n, 8): # éteindre les autres led NEOPIXEL
        NEOPIX.LED[i] = (0, 0, 0)
    NEOPIX.LED.write()

BP.drapeau = False

while not BP.drapeau : # Tant que le bouton poussoir n'a pas été enfoncé
    d = HCSR.distance_mm   # mesurer la distance
    n = 1 + d // 100 # indice de l'intervalle -> 100mm -> n=1  // 200mm -> n=2 // ...
    if n > 8 :
        n = 8
    # Attention si le capteur de distance n'arrive pas à
    # effectuer une mesure correcte, il renvoit comme valeur -1 !!!
    
    if 0 < n : # Si la distance mesurée est dans un des huit premiers intervalles
        Gestion_Neopix ( n )

    sleep_ms(100) # temporisation entre deux mesures
    
NEOPIX.eteindre()