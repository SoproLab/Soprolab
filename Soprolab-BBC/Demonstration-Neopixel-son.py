from microbit import pin8, pin14, pin1, button_a, display, Image
from neopixel import NeoPixel
from utime import sleep_ms
import music
"""
P0 -> XH2P Analog [ 3,3V -  10kΩ PULL Down ]
P1 -> MPX5700
P2 -> Analog Grove
P3 -> Switch [ Test SIL / Servo / Led col1
P4 -> Switch [ Test SIL / Servo / Led col2
P8 -> NeoPixel
P13 -> Test SIL / Servo
P14 -> BUZZER
P15 -> XH4P-1 [ 3,3V - 5V ]
P16 -> XH4P-2

P19 -> Grove I2C [ 3,3V - 5V ]
P20 -> Grove I2C

P5 -> Bouton A
P6 -> Led col9
P7 -> Led col8
P9 -> Led col7
P10 -> Led col3
P11 -> Bouton B
P12 -> Reserved

"""

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

def bargraphe ( led, niv ): # Permet de réaliser un barre_graph [0 -> 8]
    """
    Entrée : objet led (NeoPixel) / niv : niveau du bargraphe
    Sortie : Aucune
    Fonction : permet d'allumer les led neopixel avec une graduation du vert -> rouge
    en fonction de la valeur de la variable niv
    """
    for n in range ( niv ):
        led[n] = ( n*10, 70-n*10, 0 )
    for n in range ( niv, 8 ):
        led[n] = (0, 0, 0) # éteindre les autres NEOPIXELS
    led.show() # mettre à jour l'état des diodes NEOPIXEL

def proportion ( val ) :
    """
    Entrée : valeur de la pression mesurée 0 - pression_max
    Sortie : index pour le bargraphe neopixel 0 -> 8
    """
    global pression_max # la variable pression_mas est définie en dehors de cette fonction
    global nb_led
    return int((nb_led * val) / pression_max)

pression_max = 200 # valeur maximale mesurée avec la fonction pression.py
nb_led = 8 # nombre de led neopixel
display.show(Image.HAPPY)
sleep_ms(800)
led = NeoPixel ( pin8, nb_led ) # 8 led NeoPixel connectées sur la broche 16
arc_en_ciel ( led )
display.clear()
# ========================= Début du programme =========
music.play(music.ENTERTAINER, pin=pin14, wait=True, loop=False)
while not button_a.is_pressed() :
    val = pin1.read_analog()
    print("val : ",val)
    num_led = proportion(val)
    print("num led : ", num_led)
    bargraphe ( led, num_led )
    sleep_ms(200)
bargraphe ( led, 0 )