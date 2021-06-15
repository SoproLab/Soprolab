from balance import Balance
from time import sleep, ticks_ms, ticks_diff
from machine import Pin, disable_irq, enable_irq

def Set_BP_flag ( pin ): # gestion des interruptions sur le BP
    global bp_flag
    bp_flag = True

# Utilisation du bouton poussoir pour effectuer
# la tare ou pour éteindre
bp = Pin(35, Pin.IN)
bp.irq ( trigger=Pin.IRQ_RISING, handler=Set_BP_flag ) # Interruption si appui sur le BP
bp_flag = False

# Utiliser une instance de classe : Balance (Prog. Orientée Objet)
# Le connecteur est relié aux broches 0 et 4 pour communiquer
# avec le convertisseur analogique / numérique 24 bits
balance = Balance(d_out=0, pd_sck=4)

def tare ( )->int: # Effectuer la tare
    bp_flag = False
    print("Tare ...", end='')
    balance.tare()
    ajustement  = mesure( 0 )
    print("Ajustement : ", ajustement, end='')
    print(" -> Ok")
    return ajustement

    
def mesure ( ajustement:int )->int:
    global bp_flag
    val = 0
    for _ in range(3):
        val += balance.stable_value()
        if bp_flag :
            break
    return val // 3 - ajustement

def calcul_masse ( val_mesure:int )->float: # f(x) = 1954.4 x - 125
    val = round(10*val_mesure/1935)/10 
    return val

# Attendre tant que l'utilisateur n'a pas appuyé sur le
# bouton bleu de la carte SoproLab
print("Impulsion sur le BP -> tare")
print("2eme impulsion sur le BP -> OFF")

ajustement = tare()

while True :
    # Effectuer une série de 4 mesures
    val = mesure( ajustement )
    print( "{:5.01f}".format( calcul_masse ( val )) )   
    if bp_flag :
        sleep(0.3) # Attendre pour éviter d'éventuels rebonds
    if bp_flag :
        print("Tare ou OFF ?")
        bp_flag = False
        t0 = ticks_ms()
        while ticks_diff(ticks_ms(), t0) < 800 and not bp_flag :
            pass
        if bp_flag : # Deuxième impulsion -> OFF
            break
        else :
            ajustement = tare() # Une seule impulsion -> tare()
    
print(" ====== OFF =======")
# Eteindre la balance    
balance.power_off()
