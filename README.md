Carte à  microcontrôleur ESP32 avec microPython

Exemple de code Python pour utiliser la carte SoproLab et tester ses fonctionnalités.


"""
Code de test des fonctionnalit\'e9s de la carte SOPROLAB V1.0
"""
from SOPROLAB import *

input ("Appuyer sur [ Enter ] pour commencer le test ... ")

LED_v.on()  # Allumer la LED verte
LED_j.on()  # Allumer la LED jaune
LED_r.on()  # Allumer la LED rouge
sleep_ms(1000) # Temporisation de 1000 ms
LED_v.off()   # Eteindre la LED verte
LED_j.off()   # Eteindre la LED jaune
LED_r.off()   # Eteindre la LED rouge

BUZ.beep()

print("Vous pouvez faire varier la pression.")
print("Pour terminer, appuyer sur la touche [ Enter ] ...")

while BP.drapeau == False:
    MPX.mesure()
    print("Le niveau de pression est de : {:5.2f}".format(MPX.valeur))
    sleep_ms ( 3000 )
sleep_ms(200)
BP.drapeau = False # Drapeau est mis à True et reste ensuite à True, Il faut le remettre à False (acquitement)

BMP.mesure()
print("Pression atmosphérique : ", BMP.pression)
print("Température ambiante : ", BMP.temperature)

print("Appuyez sur le bouton poussoir pour continuer ...")

while BP.impulsion==False:
    continue
sleep_ms(200) # BP.impulsion reste à True pendant 200 ms pour éviter les problèmes de rebond. Retour à False ensuite

POT.mesure()
print("Valeur du potentiomètre : ", POT.valeur )
print("Tension mesurée au potentiomètre : {:3.2f} V".format(POT.tension))

LDR.mesure()
print("Valeur de la luminosité : ", LDR.valeur )

CTN.mesure()
print("Valeur de température CTN : ", CTN.valeur )

NEOPIX[0]=(     0,     0, 125)
NEOPIX[1]=(     0, 125,     0)
NEOPIX[2]=( 125,     0,     0)
NEOPIX[3]=(   75,   75,   75)
NEOPIX.write()

sleep_ms(3000)

for cptr in range(4):
    NEOPIX[cptr] = ( 0, 0, 0 )
NEOPIX.write()

note = { 'DO':262, 'RE':294, 'MI':330, 'FA':349, 'SOL':392, 'LA':440, 'SI':494 }

BUZ.son( note['DO'], 250 )
BUZ.son( note['RE'], 250 )
BUZ.son( note['MI'], 250 )
BUZ.son( note['DO'], 250 )
BUZ.son( note['RE'], 250 )
