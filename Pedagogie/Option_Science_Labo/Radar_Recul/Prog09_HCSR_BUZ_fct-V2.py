from SOPROLAB import *
from SOPROLAB_UltraSonV1 import * # bibliothèque du capteur de distance à ultrasons

n = 150 # valeur d'initialisation sans intérêt

BP.drapeau = False    
while BP.drapeau == False: # Tant que le bouton poussoir n'a pas été enfoncé

    d = HCSR.distance_mm() # mesurer la distance
    
    if d < 100 : # distance inférieure à 100mm
        n = 40
    elif  50 <= d < 100 : # distance comprise entre 50mm et 100mm
        n = 60
    elif 100 <= d < 200: # distance comprise entre 100mm et 200mm
        n = 80
    elif 200 <= d < 300: # distance comprise entre 200mm et 300mm
        n = 100
    elif 300 <= d < 400: # distance comprise entre 300mm et 400mm
        n = 120

    if d < 400 :       
        BUZ.son( 1000 - n, n )
        sleep_ms ( 15+n ) # temporisation minimum de 10ms entre deux mesures