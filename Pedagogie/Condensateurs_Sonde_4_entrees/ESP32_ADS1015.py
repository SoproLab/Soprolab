"""
ESP32_ADS1015.py
Ce code permet de mémoriser 512 mesures avec une fréquence d'échantillonnage
de 128 mesures par seconde. La mesure dure donc 4 secondes
C'est l'entrée A0 qui est utilisée pour effectuer la mesure de tension entre A0 et GND soit Uc.
En fin de programma on obtient le temps global de la mesure et la période d'échantillonnage ainsi
qu'une liste de mesures exploitables (copier/coller) dans une feuille de calculs.

IMPORTANT : Ce code est davantage destinés aux enseignants pour effectuer des séries de mesures.
La gestion des signaux de contrôle (interruption) me paraît trop complexe pour des élèves de spé physique (spé NSI ça serait envisageable ... )

Adresses I2C :
0x48 -> 72 ADS1015
0x50 -> 80 Mémoire I2C
0x27 -> 39 Afficheur LCD
0x77 -> 119 BMP180
"""

from machine import Pin, I2C, Timer
import ads1x15 
from array import array
from time import ticks_ms

Pin_I2C_CMD2 = const(27) # Signal de fin de conversion envoyé par l'ADS1015
i2c = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000 ) # Bus de communication I2C entre l'ESP32 e l'ADS1015

addr = 72 # Adresse I2C de l'ADS1015
gain = 1 # Mesure effectuée entre 0V et 3,3V
"""
0 : 6.144V # 2/3x
1 : 4.096V # 1x
2 : 2.048V # 2x
3 : 1.024V # 4x
4 : 0.512V # 8x
5 : 0.256V # 16x
"""

_BUFFERSIZE = const(512) # 512 mesures

data = array("h", (0 for _ in range(_BUFFERSIZE))) # Tableau pour récupérer les mesures
ads = ads1x15.ADS1015(i2c, addr, gain) # Objet ADS1015 pour communiquer avec le convertisseur  Analogique Numérique
#
# Interrupt service routine for data acquisition
# activated by a pin level interrupt
#
def sample_auto(x, adc = ads.alert_read, data = data):
    global index_put
    if index_put < _BUFFERSIZE:
        data[index_put] = adc() # Mesure de la valeur sur l'ADS1015
        index_put += 1 # Valeur suivante

index_put = 0

irq_pin = Pin(Pin_I2C_CMD2, Pin.IN, Pin.PULL_UP) # Gestion des interruptions lorsque la conversion est disponible pour être enregistrée
ads.conversion_start(4, 0) # Canal 0 / 128 échantillons par seconde
"""
0 :  128/8      samples per second
1 :  250/16     samples per second
2 :  490/32     samples per second
3 :  920/64     samples per second
4 :  1600/128   samples per second (default) période 7,8ms
5 :  2400/250   samples per second
6 :  3300/475   samples per second
7 :  - /860     samples per Second
"""
t0 = ticks_ms() # relever le compteur  de millisecondes
irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=sample_auto) # Activer les signaux de contrôle (interruption)
while index_put < _BUFFERSIZE: # Tant que les mesures ne sont pas terminées
    pass
irq_pin.irq(handler=None) # Fin des signaux de contrôle
t1 = ticks_ms() # relever le compteur de millisecondes
delta_t = t1-t0 # calculer delta_t pour toutes les mesures

#
# at that point data contains 512 samples acquired at the given rate
#
print("Durée des mesures : {:d} ms".format(delta_t))
print("Période d'échantillonnage : {:3.2f} ms".format(delta_t/_BUFFERSIZE))
for i in range ( 512 ):
    print("{:d},{:d}".format(i,data[i])) # Afficher le numéro de mesure et la valeur mesurée