from time import sleep_ms # importer la fonction d'attente en millisecondes
from SOPROLAB_UltraSonV1 import * # importer la biblioth!que pour gérer le capteur
                                  # de distance à ultrasons
d_tot = 0
for cptr in range ( 5 ): # Faire 5 mesures
    d = HCSR.distance_mm # Mesurer la distance
    print("Distance mesurée : ", d ) # Afficher la valeur obtenue
    d_tot = d_tot + d # Calculer la somme des mesures
    sleep_ms ( 500 )   # Attendre 0,5s

d_moy = int( d_tot / 5 ) # Diviser la somme des mesures par 5

print("La distance moyenne est de", d_moy,"mm") # Afficher le résultat