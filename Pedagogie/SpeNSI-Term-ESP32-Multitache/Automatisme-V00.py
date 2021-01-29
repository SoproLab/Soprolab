"""
Principe des registres d'état/mémorisation/chgmnt d'état des capteurs
"""

from machine import Pin
from time import sleep

fdc_close = Pin(17, Pin.IN )
fdc_open = Pin (16, Pin.IN )

capteurs = 0
capteurs_mem = 0
capteurs_chg = 0

def mise_a_jour_capteurs ( ):
    global capteurs
    global capteurs_mem
    global capteurs_chg
    capteurs = (capteurs & 0xFE) | fdc_close.value ( ) # Màj du bit d’index 0
    capteurs = (capteurs & 0xFD) | ( fdc_open.value ( )  << 1 ) # Màj du bit d’index 1
    capteurs_chg = capteurs ^ capteurs_mem # Indicatr de chgmnt d’état
    capteurs_mem = capteurs # Mémoriser l’état pour la proch. boucle
    if capteurs_chg :
        sleep ( 0.3 )  # tempo d’anti-rebond pour les interrupteurs

def afficher_capteurs ( ): # permet de vérifier l'interface registres <-> connexions ( GPIO )
    print("\tcapteurs : ", capteurs)
    print("\tcapteurs_mem : ", capteurs_mem)
    print("\tcapteurs_chg : ", capteurs_chg)

while True:
    
    mise_a_jour_capteurs ( )
    
    if capteurs_chg & 1 and capteurs_mem & 1 :
        print("Close !")
    elif capteurs_chg & 2 and capteurs_mem & 2 :
        print("Open !")
    elif capteurs_chg :
        print("Ni Close, ni Open ?!")