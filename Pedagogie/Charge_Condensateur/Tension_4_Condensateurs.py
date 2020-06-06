"""
Ce code permet de mesurer la tension sur les 4 canaux de l'ADS1015.
1 - Lancer le code
2 - Appuyer sur l'interrupteur pour mesurer les tensions soit lors de la charge
ou la décharge des condensateurs.
3 - Les valeurs mesurées s'affichent une fois l'acquisition terminée
4 - Un copier / coller dans une feuille de calculs permet d'obtenir facilement
un graphique.
Un calcul de portionnalité devra toutefois être effectué pour obtenir
une valeur de tension (V) et non simplement le résultat de la conversion numérique.
Umax : 4,096V pour une valeur numérique de 2048.
Hors, les condensateurs sont alimentés en 3,3 V et on obtient un maximum
lors de la conversion de 1660 -> 1660/2048x4,096 = 3,32V soit Umax (CQFD)
"""
from machine import Pin, I2C # Paramétrage des broches de l'ESP32
from micropython import const
from time import ticks_ms # Chronomètre
import ads1x15 # Bibliothèque d'interface du capteur

# bus de communication avec l'ESP32
busi2c = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000 )

# Broche de contrôle lorsque la conversion Analogique / Numérique est terminée 
Pin_I2C_ALERT = const(27) # N° de Broche de conrtôle des conversions
conversion_OK = Pin(Pin_I2C_ALERT, Pin.IN, Pin.PULL_UP) 
flag = False # 'drapeau' de fin de converstion / mesure

"""
Réglage du gain selon la tension utilisée :
0 : 6.144V # 2/3x
1 : 4.096V # 1x
2 : 2.048V # 2x
3 : 1.024V # 4x
4 : 0.512V # 8x
5 : 0.256V # 16x

Réglage de la fréquence d'échantillongage
ads.conversion_start(freq echant, canal1, canal2=None)
0 :  128/8      samples per second
1 :  250/16     samples per second
2 :  490/32     samples per second
3 :  920/64     samples per second
4 :  1600/128   samples per second (~ T = 8ms )
5 :  2400/250   samples per second
6 :  3300/475   samples per second
7 :  - /860     samples per Second
"""

gain = 1 # Tension de travail : 3,3 V
addr_ads1015 = 72 # Adresse du convertisseur sur le bus I2C
ads = ads1x15.ADS1015(busi2c, addr_ads1015, gain)
conversion_valeur = 0

def echantillon_flag ( x , adc=ads.alert_read ):
    """
Cette fonction est activée par l'ADS1015 lorqu'il a terminé
d'effectuer la conversion analogique numérique
-> La valeur est disponible dans les registres pour lecture de donnée.
L'activation se fait par la mise à l'état bas reliée à la broche 27
    """
    global flag
    global conversion_valeur
    conversion_valeur = adc() # Lecture de la conversion
    flag = True # Indication : la valeur a été mémorisée


_BUFFERSIZE = 128 # Nombre de valeurs sur chaque entrée
mesures = [[]] # [128][t(ms), canal 0, canal 1, ... 2, ... 3 ]

# Etablir un lien entre l'état logique d'une broche et la fonction associée
conversion_OK.irq(trigger=Pin.IRQ_FALLING, handler=echantillon_flag)

t0 = ticks_ms() # relever le compteur de millisecondes
for index in range(_BUFFERSIZE) : # Pour la série de mesures
    mesures.append([]) # ajouter un enregistrement
    mesures[index].append([]) # ajouter l'espace pour mémoriser 5 valeurs
    buff=[0,0,0,0,0] # Stockage d'une mesure
    for cptr in range (0,4): # Pour les quatre canaux 0 -> 3
        
        # Configurer le convertisseur pour faire une acquisition sur un canal
        ads.conversion_start(rate=5, channel1=cptr, channel2=None)
        while not flag: # Attendre que la mesure soit mémorisée
            pass 
        flag = False # 'redescendre' le drapeau pour la prochaine conversion
        buff[cptr+1] = conversion_valeur # stocker la valeur mémorisée
        
    buff[0] = ticks_ms() - t0 # stocker l'intervalle de temps en ms
    mesures[index] = buff # Stocker l'enregistrement dans le tableau

conversion_OK.irq(handler=None)  # Terminé -> Annuler les interruptions
    
# Afficher les résultats au format csv
# t(ms), canal 3, canal 0, canal 1, canal 2
# On peut ainsi faire un copier / coller des valeurs affichées dans la console
# pour les importer dans LibreOffice Calc et tracer les courbes de tension
for cptr in range(_BUFFERSIZE): 
    for i in range(4) :
        print (mesures[cptr][i],',',end='')
    print( mesures[cptr][4] )

# Pour info : je préfère effectuer les conversions numérique -> tension en volt
# sous LibreOffice plutôt que d'afficher la valeur de la tension dans la console
# Cela évite d'avoir à transformer le séparateur décimale '.' en python
# en séparateur décimal ',' sous LibreOffice après importation (chercher/remplacer)
