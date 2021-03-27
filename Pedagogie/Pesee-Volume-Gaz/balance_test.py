from balance import Balance
from time import sleep
from machine import Pin

# Utilisation du bouton poussoir pour effectuer une série de mesures
bp = Pin(35, Pin.IN)

# Utiliser une instance de classe : Balance (Prog. Orientée Objet)
# Le connecteur est relié aux broches 0 et 4 pour communiquer
# avec le convertisseur analogique / numérique 24 bits
balance = Balance(d_out=0, pd_sck=4)

# Effectuer la tare
print("Tare ...", end='')
sleep(0.5)
balance.tare()
print("Ok")

# Attendre tant que l'utilisateur n'a pas appuyé sur le
# bouton bleu de la carte SoproLab
print("Appuyer sur le BP pour effectuer 10 mesures.")
while bp.value()==0:
    pass
sleep(0.5)

# Effectuer une série de 10 mesures
val=[]
for i in range(10):
    val.append(balance.stable_value())
    print( val[i] )
    sleep(1)
    
# Eteindre la balance    
balance.power_off()
