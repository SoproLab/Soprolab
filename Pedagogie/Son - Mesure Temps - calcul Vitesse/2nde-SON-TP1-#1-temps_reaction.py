from machine import Pin
from time import ticks_us, sleep

buz = Pin(4, Pin.OUT)
micro = Pin(0, Pin.IN)

somme = 0
for n in range(1,9): # faire 8 essais n = 1, 2, 3, ... jusqu'à 9 exclu
    buz.on()
    t0 = ticks_us()
    while micro.value()==1 :
        pass
    t1 = ticks_us()
    buz.off()
    
    delta_t = t1 - t0 # delta_t : temps de réaction entre 300 et 400 µs selon le réglage de sensibilité du micro

    print("n°",n,"-> temps mesuré : ",delta_t,"µs")

    somme = somme + delta_t # cumulés les delta_t pour calculer la moyenne
    sleep(1) # attendre 1 seconde entre deux essais
moyenne = somme / 8
print("Le temps moyen mesuré est de ",moyenne,"µs")    