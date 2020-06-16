"""
Capteur_ADS1015.py
Ce code Python permet de s'affranchir du paramétrage pour l'utilisateur du convertisseur analogique / numérique.
Ainsi toute la partie déclaration / paramétrage / ... peut être oculté pour l'élève qui focalise sa démarche sur la mesure.
Une simple ligne de commande permet d'effectuer les mesures : 

capteur_ads ( nb_data, rate=4, canal0=0, canal1=None ) 
    -> nb_data -> nombre de mesures
    -> rate : fréquence d'échantillonnage (voir plus bas)
    -> canal0 -> canal 0, 1, 2 ou 3
    -> canal1 -> None si mesure entre une entrée et GND ou mesure différentielle entre deux entrées (canal0=0) -> canal1=1 ou alors  (canal0=2) -> canal1=3 

Voir le fichier ESP32_ADS1015_V2 pour l'utilisation simplifiée

"""
from machine import Pin, I2C, Timer
from array import array
import utime as time
import ads1x15

Pin_I2C_ALERT = const(27) # Alert
busi2c = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000 )
addr_ads1015 = 72
data_ads = []
gain = 1
""" ads = ads1x15.ADS1015(busi2c, addr_ads1015, gain)
gain :
0 : 6.144V # 2/3x
1 : 4.096V # 1x
2 : 2.048V # 2x
3 : 1.024V # 4x
4 : 0.512V # 8x
5 : 0.256V # 16x

ads.conversion_start(freq_echant, canal1, canal2=None)
freq_echant : 
0 :  128/8      samples per second
1 :  250/16     samples per second
2 :  490/32     samples per second
3 :  920/64     samples per second
4 :  1600/128   samples per second (~ T = 8ms )
5 :  2400/250   samples per second
6 :  3300/475   samples per second
7 :  - /860     samples per Second
"""
ads = ads1x15.ADS1015(busi2c, addr_ads1015, gain)
# Déclarer la broche d'interruption lorsque mesure disponible
irq_pin = Pin(Pin_I2C_ALERT, Pin.IN, Pin.PULL_UP)


_BUFFERSIZE = 512 # Nombre de valeurs
index_put = 0

def sample_auto(x, adc = ads.alert_read, data = data_ads):
    global index_put
    global data_ads
    global _BUFFERSIZE
    if index_put < _BUFFERSIZE:
        data_ads[index_put] = adc()
        index_put += 1

def capteur_ads ( nb_data, rate=4, canal0=0, canal1=None ):
    global index_put
    global _BUFFERSIZE
    global data_ads
    _BUFFERSIZE = nb_data
    
    data_ads = array("h", (0 for _ in range(_BUFFERSIZE)))
    index_input = 0

    irq_pin.irq(trigger=Pin.IRQ_FALLING, handler=sample_auto)

    ads.conversion_start(rate, canal0, canal1)  
    while index_put < nb_data:
        pass
    irq_pin.irq(handler=None)  # Annuler les interruptions
    return data_ads



