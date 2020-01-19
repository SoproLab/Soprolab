from machine import Pin, ADC  # importer la configuration des broches
from time import sleep_us # importer la fonction sleep_us()

Buzzer = Pin ( 25, Pin.OUT ) # Broche reliée au buzzer
Bouton = Pin ( 35, Pin.IN ) # Broche reliée au bouton poussoir
Potentiometre = ADC ( Pin(34) ) # Broche reliée au potentiomètre
Potentiometre.atten(ADC.ATTN_11DB) # Adaptation des mesures

while Bouton.value() == False: # tant qu'on appuie pas sur le bouton poussoir

    freq = Potentiometre.read() + 200 # Lecture de la valeur du potentiomètre
    T = int(1000000/freq) # Période en microsecondes
    
    Buzzer.off() # Mettre la broche du buzzer à 0
    sleep_us ( int(T/2 ) ) # Attendre une demie-période
    Buzzer.on() # Mettre la broche du buzzer à 1
    sleep_us ( int(T/2 ) ) # Attendre une demie période