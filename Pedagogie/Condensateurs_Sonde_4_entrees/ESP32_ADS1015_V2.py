"""
Utilisation des bibliothèques pour simplifier l'usage de l'ADS1015 convertisseur analogique
numérique 12 bits : [-2048 ; 2048]
En fin de programme, c'est la valeur numérique qui est affichée et non la conversion en volt.
Ceci évite le soucis de remplacement du séparateur décimal entre python '.' et LibreOffice ','.
SOnt affiché : le temps(ms) , données -> affichage formaté CSV
La conversion en volt peut ensuite se faire dans la feuille de calculs.
Un simple copier/coller des valeurs affichées permet de passer de l'éditeur Python à la feuille de calculs pour l'exploitation : (console de l'éditeur python) sélectionner / copier -> (libreoffice calc) collage spécial / texte non formaté / données séparées par une virgule.
"""

from Capteur_ADS1015 import * # Intégration de toutes les déclaration / paramétrage ...
from time import ticks_ms

nb_data = 256 # Nombre de mesures

t0 = ticks_ms() # Relever le compteur de millisecondes

"""
effectuer 256 mesures
à la fréquence de 128 mesures par seconde
sur l'entrée A0
pour une tension entre l'entrée A0 et GND (mesure de potentiel)
"""
data = capteur_ads ( nb_data, rate=4, canal0=0, canal1=None ) 

t1 = ticks_ms() # Relever le compteur de millisecondes

delta_t = t1-t0 # Calculer le temps total des mesures

print("Durée de la mesure : {:d} ms".format(delta_t))
periode = delta_t // nb_data # valeur entière pour la période d'échantillonnage en ms (choix)
print("Période d'échantillonnage : {:3.2f} ms".format(periode))

for i in range ( nb_data ):
    print("{:d},{:d}".format(i*periode,data[i])) # Afficher les mesures au format CSV