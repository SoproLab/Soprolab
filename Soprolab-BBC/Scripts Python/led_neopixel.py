from microbit import pin8
from neopixel import NeoPixel
from utime import sleep_ms

def arc_en_ciel ( led ): # Permet de déclarer de nouvelles méthodes
    niv = [ 0, 0, 0, 35, 65, 35, 0, 0, 0 ]
    for i in range ( 6 ):
        led[i]=(  niv[i], niv[(i+2)%6], niv[(i+4)%6] )
    led[6]=( 5,  5,  5)
    led[7]=(125, 125, 125)
    led.show()
    sleep_ms(800)
    led[7] = (0, 0, 0) # Eteindre la dernière LED
    for cptr in range(8): # décaler 8 fois les LED
        for cptr in range(7): # décaler chaque LED d'un cran
            led[cptr] = led[cptr+1]
        led.show()
        sleep_ms(75)
def eteindre ( led ):
    for i in range(8):
        led[i]=(0,0,0)
    led.write()
def bargraphe ( led, niv ): # Permet de réaliser un barre_graph [0 -> 8]
    for n in range ( niv ):
        led[n] = ( n*10, 70-n*10, 0 )
    for n in range ( niv, 8 ):
        led[n] = (0, 0, 0) # éteindre les autres NEOPIXELS
    led.write() # mettre à jour l'état des diodes NEOPIXEL

led = NeoPixel ( pin8, 8 ) # 9 led NeoPixel connectées sur la broche 16
arc_en_ciel ( led )
