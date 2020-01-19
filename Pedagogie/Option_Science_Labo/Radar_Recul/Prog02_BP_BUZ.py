from machine import Pin # importer la configuration des broches
from time import sleep_us # importer la fonction sleep_us()

Buzzer = Pin ( 25, Pin.OUT ) # Broche reliée au buzzer
Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir

T = int( (1/440) * 10**6 ) # Période en microsecondes, d'un son de 440 Hz
print ( "Période : ", T, "µs" )
nbT = int ((0.5 * 10**6 ) / T) # nombre de périodes pour une durée de 0,5 s
print ( "Nombre de périodes : ", nbT )

while True: # boucle infinie
    
    etat = Bouton.value() # lire l'état du bouton poussoir
    if etat == 1 : # Si le bouton poussoir est enfoncé alors
        for cptr in range ( nbT ): # Pour le nombre de périodes nécessaires
            Buzzer.off() # Mettre la broche du buzzer à 0
            sleep_us ( int(T/2 ) ) # Attendre une demie-période
            Buzzer.on() # Mettre la broche du buzzer à 1
            sleep_us ( int(T/2 ) ) # Attendre une demie période