"""
Donner l'impression de deux lumières rouge et verte qui se déplacent
"""
from machine import Pin
from neopixel import NeoPixel
from time import sleep

led = NeoPixel ( Pin(2), 8 ) # Ruban de 8 led multicolores connecté à la broche n°2

rouge = ( 125,   0, 0 )
vert = (    0, 125, 0 )
eteinte = ( 0,   0, 0 )

for i in range(5): # faire 5 fois
    for i in range(8): 
        led[ i ] = rouge # de 0 à 7
        led[7-i] = vert  # de 7 à 0 
        led.write()
        sleep(0.05)
        led[ i ] = eteinte # éteindre les deux led
        led[7-i] = eteinte
        led.write()        
    for i in range(7, -1, -1): 
        led[ i ] = rouge # de 7 à 0
        led[7-i] = vert  # de 0 à 7 
        led.write()
        sleep(0.05)
        led[ i ] = eteinte # éteindre les deux led
        led[7-i] = eteinte
        led.write()        
sleep(2)
for i in range(8) : # éteindre
    led[i] = eteinte  
led.write()