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

    delta_t = (t1 - t0) - 352 # remplacer 352 par votre temps de réaction mesuré

    print("n°",n,"-> temps mesuré : ",delta_t,"µs")

    somme = somme + delta_t # cumulés les delta_t pour calculer la moyenne
    sleep(1) # attendre 1 seconde entre deux essais
moyenne = somme / 8
print("Le temps moyen mesuré est de ",moyenne,"µs")

# Si on connait delta_t on peut calculer la vitesse de propagation du son dans l'air
distance = 2 # la longeur du tuyau en m
vitesse = distance / (delta_t*1e-6) # 1e-6 parce que ce sont des micro secondes
print ("La vitesse de propagation du son dans l'air calculée est de :",vitesse,"m/s")

    