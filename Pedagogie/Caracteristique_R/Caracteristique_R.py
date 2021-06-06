from machine import Pin, I2C, DAC
from time import sleep_ms
from ads1x15 import * # convertisseur Analogique Numérique 12 bits

# l'ESP32 dispose de deux sorties analogiques dont la valeur peut être définie
# entre ~ 0 V et 3.3 V ( 0,08V et 3,3V )
# C'est un des deux DAC qui va servir de générateur pour déterminer la caractéristique

dac = DAC(Pin(26)) # Convertisseur Numérique -> Analogique
dac.write(0)

R_i = 10.4 # Résistance pour déterminer I = U/R

busi2c = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000 )
addr_ads1015 = 72

pas_mesures = 25
nb_mesures = round(255 / pas_mesures) # DAC de 0 à 255 par pas de 25
data = [[0, 0] for i in range(nb_mesures+1)]

""" GAIN :
0 : 6.144V # 2/3x
1 : 4.096V # 1x
2 : 2.048V # 2x
3 : 1.024V # 4x
4 : 0.512V # 8x
5 : 0.256V # 16x
"""

"""
effectuer 10 mesures à la fréquence de 128 mesures par seconde
sur l'entrée A0 préampli 5 -> [ 0 - 0,256V ]
A0 mesure la tension aux bornes d'une résistance de 10Ω
U = RxI -> I = U/R
"""

for num_mesure in range ( nb_mesures+1 ):
        # Modifier la valeur de U(V) sur la sortie DAC
    dac.write(num_mesure * pas_mesures) # Faire varier U
    sleep_ms(100) 
    
    # Mesure de U aux bornes de R = 10 Ω -> I(A) = U/R
    # Connecteur blanc entre la résistance de 10Ω et celle de 10kΩ
    # Gain maximum pour avoir le plus de précision possible
    capteur_ads = ADS1015(busi2c, addr_ads1015, gain=5)
    val = capteur_ads.read(rate=0, channel1=0, channel2=None)
    data[num_mesure][0] = capteur_ads.raw_to_v ( val ) / R_i  # I = U / R
        
    sleep_ms(100)

    # Mesure de U aux bornes de R = 10 kΩ -> U (V)
    # Connecteur jaune -> relié au DAC
    capteur_ads = ADS1015(busi2c, addr_ads1015, gain=1)
    val = capteur_ads.read(rate=0,channel1=1, channel2=None)
    data[num_mesure][1] = capteur_ads.raw_to_v ( val ) - 0.08 # ~ 0v -> 0,08 V
    
 


print("I(A), U(V)")
for num_mesure in range ( nb_mesures + 1):
    print(data[num_mesure][0],",",data[num_mesure][1])
print("\n Penser à convertir le séparateur décimal '.' par ',' pour LibreOffice ...")