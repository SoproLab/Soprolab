"""
Allumer sept led neopixel :
 - couleurs primaires :  Rouge, Verte, Bleue
 - couleurs complémentaire : Jaune, Magenta, Cyan
 - Blanche / Noire (éteinte)
pendant 2 secondes
"""
from machine import Pin
from neopixel import NeoPixel
from time import sleep

led = NeoPixel ( Pin(2), 8 ) # Ruban de 8 led multicolores connecté à la broche n°2

#        Rouge Vert Bleu   (les espaces n'ont pas d'importance) 
rouge = ( 125,   0,   0 )
vert = (    0, 125,   0 )
bleu = (    0,   0, 125 )
jaune = (  85,  85,   0 ) # valeurs comprises entre 0 et 255 (125 c'est souvent suffisant !)
cyan = (    0,  85,  85 )
magenta =( 85,   0,  85 )
blanche =( 50,  50,  50 )
eteinte = ( 0,   0,   0 )

led[0] = rouge
led[1] = vert
led[2] = bleu
led[3] = jaune
led[4] = cyan
led[5] = magenta
led[6] = blanche
led[7] = eteinte
led.write()

sleep(4)
for i in range(8) : # éteindre
    led[i] = (0, 0, 0)  
led.write()