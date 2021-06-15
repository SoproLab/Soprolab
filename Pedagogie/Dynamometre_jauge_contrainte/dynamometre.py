from balance import Balance
from time import sleep, ticks_ms, ticks_diff
from machine import Pin, I2C, disable_irq, enable_irq
from Lcd import Lcd1602

def Set_BP_flag ( pin ): # gestion des interruptions sur le BP
    global bp_flag
    bp_flag = True

my_i2c = I2C ( scl=Pin(22), sda=Pin(21), freq=100000 )
lcd = Lcd1602 ( my_i2c )

# Utilisation du bouton poussoir pour effectuer
# la remise à zéro ou pour éteindre
bp = Pin(35, Pin.IN)
bp.irq ( trigger=Pin.IRQ_RISING, handler=Set_BP_flag ) # Interruption si appui sur le BP
bp_flag = False

# Le connecteur est relié aux broches 0 et 4 pour communiquer
# avec le convertisseur analogique / numérique 24 bits
dynamometre = Balance(d_out=0, pd_sck=4)

def remise_a_zero ( )->int: # Effectuer la tare
    bp_flag = False
    print("========== DYNAMOMETRE =========")
    print("Initialisation ...")
    dynamometre.tare()
    ajustement  = mesure( 0 )
    print("Ajustement : ", ajustement," -> Ok")
    return ajustement

    
def mesure ( ajustement:int )->int:
    global bp_flag
    val = 0
    for _ in range(3):
        val += dynamometre.stable_value()
        if bp_flag :
            break
    return val // 3 - ajustement

def calcul_force ( val_mesure:int )->float: # f(x) = 1954.4 x - 125
    val = round(98*val_mesure/1935)/10000
    
    return val

# Attendre tant que l'utilisateur n'a pas appuyé sur le
# bouton bleu de la carte SoproLab
print("Impulsion sur le BP -> remise à zéro")
print("2eme impulsion sur le BP -> OFF")

ajustement = remise_a_zero()

lcd.on()
lcd.afficher(0,0, "Dynamomètre :")

while True :
    # Effectuer une série de 4 mesures
    val = mesure( ajustement )
    mesure_texte = "{:5.01f} N".format( calcul_force ( val ))
    
    print( mesure_texte )
    lcd.afficher (5,1, "       ")
    lcd.afficher (5,1, mesure_texte )

    if bp_flag :
        sleep(0.3) # Attendre pour éviter d'éventuels rebonds
    if bp_flag :
        print("Remise à zéro ou OFF ?")
        bp_flag = False
        t0 = ticks_ms()
        while ticks_diff(ticks_ms(), t0) < 800 and not bp_flag :
            pass
        if bp_flag : # Deuxième impulsion -> OFF
            break
        else :
            ajustement = remise_a_zero() # Une seule impulsion -> tare()
    
print(" ====== OFF =======")
# Eteindre la balance    
dynamometre.power_off()
    
lcd.backlight_off()
lcd.off()



