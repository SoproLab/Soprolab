"""
Objectif : Mesurer la vitesse du son dans l'air.
Auteur : Jacques Chouteau - Octobre 2019 -
Matériel : Carte SoproLab ( Soprolec.com ) + Module de mesure de la vitesse du son
Principe :
On affiche la température ambiante pour rappeler que la célérité du son dans l'air dépend aussi de la température de l'air
Répéter 10 fois :
    Mettre le buzzer en marche pour produire un "beep"
    Déclencher le chonomètre de microsecondes
    Attendre que le microphone perçoive un son
    Arrêter le chronomètre de microsecondes
    Calculer la celerité du son dans l'air = 2m / delta t
"""
# Importation des modules propres à l'ESP32
from SOPROLAB import *
from SOPROLAB_CeleriteSon import *

for cptr in range ( 0, 10 ): # 10 essais pour vérifier la stabilité des résultats

    buzzer.on() # Front montant de la consigne de commande du buzzer
    sleep_us(100) # Attente : temps de réponse du buzzer
    
    t0 = Chrono_µs_on ( )   # Relever l'horloge en µs au moment du "beep"
    
    while microphone.impulsion == False : # Attente de la réception du "beep"
        continue

    t1 = Chrono_µs_off ( ) # Relever l'horloge en µs au moment de la réception du "beep"
    
    buzzer.off ( ) # Extinction du buzzer
    
    delta_t = t1 - t0
    print("Temps de propagation mesuré : ", delta_t, "µs")

    celerite = ( 2 / delta_t ) * 1000000  # Calcul de la vitesse : Longueur du tuyau = 2m
   
    print("Célérité calculée : {:5.2f} m/s".format(celerite))
    sleep(1)  # Attendre une seconde entre deux mesures

print("La célérité théorique du son dans l'air est de C = 331,5 + 0,607 T")
print("Avec : ")
print("    C = célérité du son dans l'air à une température proche de la température ambiante")
print("    T = température mesurée")
BMP.mesure()
print("La température est de ", BMP.temperature )
celerite = 331.5 + 0.607 * BMP.temperature
print("    Célérité théorique :  {:5.2f}".format(celerite))

