"""
Donner l'impression de deux lumières rouge et bleues qui se déplacent
"""
from machine import Pin
from neopixel import NeoPixel
from time import sleep

led = NeoPixel ( Pin(2), 8 ) # Ruban de 8 led multicolores connecté à la broche n°2

eteinte = (0, 0, 0)
couleurs = [(112,  16,   0),
            ( 80,  48,   0),
            ( 48,  80,   0),
            ( 16, 112,   0),
            (  0, 112,  16),
            (  0,  80,  48),
            (  0,  48,  80),
            (  0,  16, 112)]

for i in range(8):
    led[i] = couleurs[i]
led.write()

sleep(15)
for i in range(8) : # éteindre
    led[i] = eteinte  
led.write()