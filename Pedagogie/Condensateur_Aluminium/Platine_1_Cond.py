"""
Auteur : jacques.chouteau@ac-nantes.fr
Ce script permet de mesurer la tension de charge ou décharge d'un condensateur à l'aide 
d'une carte à microcontrôleur ESP32 avec l'interpréteur microPython en mémoire flash.
"""
from machine import Pin, ADC
from time import sleep_us, sleep_ms, ticks_ms, ticks_us

# Le condensateur est relié à la broche 36
broche = ADC(Pin(36))
# On effectue une atténuation avant l'entrée du convertisseur
# analogique numérique pour éviter qu'il soit saturé à 1V
broche.atten(ADC.ATTN_11DB)

# Créer un tableau de 200 couples [ temps, mesure ]
tps_val = [[0,0] for i in range(200) ]

# Attendre tant que la valeur mesurée est nulle 
while broche.read() < 2 : 
    pass

t0 = ticks_us() # Relever le compteur de microsecondes
for n in range (200): # Effectuer 200 mesures
    tps_val[n][0] = ticks_us()-t0 # Calculer delta t
    tps_val[n][1] = broche.read() # Mesurer la valeur
    sleep_us(100) # Temporisation entre deux mesures

# Afficher les résultats
print("tps(us), val(0->4095)")

for n in range (200):
    print("{:d},{:d}".format(tps_val[n][0],tps_val[n][1]))
    sleep_us(500)
