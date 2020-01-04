# Test_SOPROLAB.py 2019-12-28 - 12h -
"""
Code de test des fonctionnalités de la carte SOPROLAB V1.0
Exemples de code pour utiliser les fonctionnalités de la carte ainsi que les objets et variables de la bibliothèque SOPROLAB.py
"""
from SOPROLAB import *

# ================================== Attendre : Donner une indication à l'utilisateur sur le test à venir
def Attendre ( texte ): 
    print( texte )
    while BP.impulsion==False:
        continue
    sleep_ms(200) # BP.impulsion reste à True pendant 200 ms pour éviter les problèmes de rebond.
                  # Retour automatique à False ensuite
    
# ================================================================================ Test Communication USB
nb_mesures = 0
while nb_mesures == 0:
    try:
        nb_mesures = int(input("Combien voulez-vous faire de mesures pour chaque test [ entre 5 et 20 ] ? "))
        if nb_mesures>20:
            nb_mesures = 20
        elif nb_mesures<5:
            nb_mesures = 5
    except:
        print("Seules les valeurs numériques entières sont acceptées - Merci")
        nb_mesures = 0

Attendre ("Appuyez sur le bouton poussoir entre chaque test … \n")

# ================================================================================ Test de l'eeprom
print("Les valeurs affichées ci-dessous ont été stockées précédemment dans l'eeprom.")
print("Evolution de la tension mesurée au potentiomètre au cours du temps : ")
# Format des données (la tension est comprise entre 0 et 3,30V
# 2 octets pour le temps en ms [ 0 - 65535 ] 
# 1 octet pour la partie entière ( 1 digit )
# 2 octets pour la partie décimale (2 digits) < 255
#  octets : 0 1     2 [0-16]         3 4 [ 0 - 99 ]
#  data   : temps   Partie entière   Partie décimale
nbval = int( MEMOIRE[0]<<8 )   # Récupérer le nombre de valeurs enregistrées : 2 premiers octets
nbval = nbval + MEMOIRE[1]
print("{:3d} valeurs mémorisées dans l'eeprom :".format(nbval))
print(" Temps (ms) , Tension (V)")
offset = 2 # Décalage des deux premiers octets où est stocké le nombre de valeurs mémorisées
for cptr in range ( nbval ): # Afficher les [ nbval ] mesures stockées dans l'eeprom 
    temps = int(MEMOIRE[5*cptr+offset] << 8) # le temps est codé sur 2 octets [ 0 et 1 ]
    temps = temps + MEMOIRE[5*cptr+1+offset]
    val_ent = MEMOIRE[5*cptr+2+offset] # partie entière de la mesure codée sur 1 octet [ 2 ]
    val_dec = int(MEMOIRE[5*cptr+3+offset] << 8) # partie décimale de la mesure codée sur 2 octets [ 3 et 4 ]
    val_dec = val_dec + MEMOIRE[5*cptr+4+offset]
    valeur = float(val_ent + val_dec/100)
    print("{:03d} , {:1.2f}".format(temps, valeur) ) # Affichage au format CSV
    if (val_ent<0 or val_ent>3 ) or (val_dec<0 or val_dec>99):
        print("C'est peut être la première fois que le test est réalisé ?!")
        print("Une des valeurs mémorisées ne semblent pas cohérente [ 0; 3.3]")
        print("Il est donc conseillé de terminer puis refaire ce test pour vérifier le fonctionnement de l'eeprom ...")
        break
# ================================================================== Test LED Verte / Jaune / Rouge
Attendre("\nTest des 3 LEDs Verte / Jaune / Rouge ...")

LED_v.on()  # Allumer la LED verte 
LED_j.on()  # Allumer la LED jaune
LED_r.on()  # Allumer la LED rouge
sleep_ms(1000) # Temporisation de 1000 ms
LED_v.off()   # Eteindre la LED verte
LED_j.off()   # Eteindre la LED jaune
LED_r.off()   # Eteindre la LED rouge

# ============================================== Test du capteur de pression MPX et memoire eeprom
Attendre("\nTest du capteur de pression ...")

print("Valeurs du MPX5700 : [ 0 - 4095 ] ")
for cptr in range ( nb_mesures ):
    MPX.mesure()
    print( MPX.valeur ) # MPX.valeur int 16 bits
    sleep_ms ( 250 )
# ================================================================================ Test du potentiomètre POT
print ("\nTest du potentiomètre et de la mémoire eeprom ( tournez le potentiomètre )")
print ("Les valeurs vont être mémorisées dans la mémoire eeprom.")
Attendre ("===== Pour TERMINER le test, appuyez sur le bouton poussoir de la carte ... =====")
print("temps (ms) , valeur [0-4095], tension(V)")
BP.drapeau=False
cptr = 0
offset = 2 # les deux premiers octets contiendront le nombre de mesures enregistrées
t0 = ticks_ms() # relever le chronomètre en millisecondes
while BP.drapeau == False: # BP.drapeau est mis à True lors de lappui mais reste ensuite à True contrairement à BP.impulsion
    POT.mesure()
    t = ticks_ms() - t0 # mesurer le temps de la mesure en millisecondes
    val_ent = int(POT.tension) # partie entière
    val_dec = int((round(POT.tension,2) - val_ent)*100) # partie décimale arrondie à 2 décimales
    
    MEMOIRE[5*cptr+offset] = ((t & 0xFF00)>>8) # Mémorisation des 8 bits de poids fort du temps
    MEMOIRE[5*cptr+1+offset] = t & 0x00FF # mémorisation des 8 bits de poids faible
    MEMOIRE[5*cptr+2+offset] = (val_ent & 0x00FF) # Mémorisation des 8 bits de la partie entière
    MEMOIRE[5*cptr+3+offset] = ((val_dec & 0xFF00)>>8) # mémorisation des 8 bits de poids fort de la partie décimale
    MEMOIRE[5*cptr+4+offset] = (val_dec & 0x00FF) # Mémorisation des 8 bits de poids faible du temps
    
    print("    {:05d}  ,      {:4d}      ,    {:1.2f}".format(t, POT.valeur, POT.tension) ) # Affichage au format CSV
    cptr = cptr+1
    sleep_ms ( 200 )
sleep_ms(200)
BP.drapeau = False # BP.drapeau est remis à False manuellement ( acquittement)

MEMOIRE[0] = ((cptr-1) & 0xFF00)>>8 # mémoriser le nombre de valeur enregistrées
MEMOIRE[1] = (cptr-1) & 0x00FF
print("{:2d} valeurs mémorisées : ".format(cptr-1) ) # Formatage de l'affichage : 2 digits / valeurs entières

# ====================================== Test du capteur de pression atmosphérique et température ambiante BMP
Attendre("\nTest du capteur de température ambiante et pression atmosphérique - BMP180 ... ")
BMP.mesure()
print("     - Pression atmosphérique : {:4d} hPa", BMP.pression) # Affichage 4 digits
print("     - Température ambiante : {:2.2f} °C".format(BMP.temperature) ) # Affichage XX.XX

# ================================================================================ Test de la photorésistance LDR
Attendre("Test du capteur de lumière (couvrir puis découvrir la LDR) ... ")

print("Valeurs de la photorésistance LDR : [ 0 - 4095 ] ")
for cptr in range ( nb_mesures ):
    LDR.mesure()
    print( LDR.valeur ) # MPX.valeur int 16 bits
    sleep_ms ( 250 )
# ================================================================================ Test de la thermistance CTN
Attendre("\nTest de la thermistance ( Vérifiez que la CTN est connectée puis plongez-la dans de l'eau chaude ou froide ) ... ")

print("Valeurs de la thermistance CTN : [ 0 - 4095 ] ")
for cptr in range ( nb_mesures ):
    CTN.mesure()
    print( CTN.valeur ) # MPX.valeur int 16 bits
    sleep_ms ( 250 )
# ================================================================================ Test des 8 NeoPixels NEOPIX
Attendre("\nTest des 8 LED NeoPixels ...")
NEOPIX[0]=(  0,   0, 125)
NEOPIX[1]=(  0,  65,  65)
NEOPIX[2]=(  0, 125,   0)
NEOPIX[3]=( 65,  65,  0)
NEOPIX[4]=(125,   0,   0)
NEOPIX[5]=( 65,   0,  65)
NEOPIX[6]=( 15,  15,  15)
NEOPIX[7]=(255, 255, 255)
NEOPIX.write()
sleep_ms(1500)
buff = NEOPIX[7]
for cptr in range (64):
    NEOPIX[7] = NEOPIX[cptr%6]
    NEOPIX.write()
    sleep_ms(50)

for cptr in range(8): # décaler 8 fois les LED
    buff = NEOPIX[0] # Mémoriser la première LED pour la replacer en 7eme position
    for cptr in range(7): # décaler chaque LED d'un cran
        NEOPIX[cptr] = NEOPIX[cptr+1]
    NEOPIX[7] = buff
    NEOPIX.write()
    sleep_ms(150)
    
NEOPIX[7] = (0, 0, 0) # Eteindre la dernière LED
for cptr in range(8): # décaler 8 fois les LED
    for cptr in range(7): # décaler chaque LED d'un cran
        NEOPIX[cptr] = NEOPIX[cptr+1]
    NEOPIX.write()
    sleep_ms(150)
# ================================================================================ Test du BUZZER BUZ
Attendre ("\nTest du buzzer (vérifiez la position de l'interrupteur S2) ...")

note = { 'DO':262, 'RE':294, 'MI':330, 'FA':349, 'SOL':392, 'LA':440, 'SI':494 }
BUZ.son( note['DO'], 250 )
BUZ.son( note['RE'], 250 )
BUZ.son( note['MI'], 250 )
BUZ.son( note['DO'], 250 )
BUZ.son( note['RE'], 250 )
# ================================================================================ Test de l'eeprom
Attendre("- Pour vérification - Affichage des valeurs mémorisées dans l'eeprom ... ")
nbval = int( MEMOIRE[0]<<8 )   # Récupérer le nombre de valeurs enregistrées : 2 premiers octets
nbval = nbval + MEMOIRE[1]
print("{:3d} valeurs mémorisées dans l'eeprom :".format(nbval))
print(" Temps (ms) , Tension (V)")
offset = 2 # Décalage des deux premiers octets où est stocké le nombre de valeurs mémorisées
for cptr in range ( nbval ): # Afficher les [ nbval ] mesures stockées dans l'eeprom 
    temps = int(MEMOIRE[5*cptr+offset] << 8) # le temps est codé sur 2 octets [ 0 et 1 ]
    temps = temps + MEMOIRE[5*cptr+1+offset]
    val_ent = MEMOIRE[5*cptr+2+offset] # partie entière de la mesure codée sur 1 octet [ 2 ]
    val_dec = int(MEMOIRE[5*cptr+3+offset] << 8) # partie décimale de la mesure codée sur 2 octets [ 3 et 4 ]
    val_dec = val_dec + MEMOIRE[5*cptr+4+offset]
    valeur = float(val_ent + val_dec/100)
    print("{:03d} , {:1.2f}".format(temps, valeur) ) # Affichage au format CSV

print("===============  FIN DU TEST ================")