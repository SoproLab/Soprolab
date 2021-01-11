"""
Donner l'impression de deux lumières rouge et bleues qui se déplacent
"""
from machine import Pin
from neopixel import NeoPixel
from time import sleep

led = NeoPixel ( Pin(2), 8 ) # Ruban de 8 led multicolores connecté à la broche n°2

eteinte = (0, 0, 0)
couleurs = [(113,  15,   0),
            ( 81,  47,   0),
            ( 47,  81,   0),
            ( 15, 113,   0),
            (  0, 113,  15),
            (  0,  81,  47),
            (  0,  47,  81),
            (  0,  15, 113)]

for i in range(8):
    led[i] = couleurs[i]
led.write()

sleep(2)
for i in range(8) : # éteindre
    led[i] = eteinte  
led.write()