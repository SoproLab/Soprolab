import sys
from micropython import const
from machine import Pin, I2C, PWM, ADC, time_pulse_us
from bme280 import BME280
from girouette import Girouette
from lcd_i2c import My_LCD
from time import ticks_ms, sleep_ms, sleep
try:
  import usocket as socket
except:
  import socket
import network

pin_ledBlanche = const(13) # Commande d'éclairage
pin_servo = const(5)  # Broche du servo_moteur
pin_close = const(12) # Broche du fin de course fermeture
pin_open = const(4) # Broche du fin de course Ouverture
pin_anemometre = const(27) # Broche de connexion avec l'anemometre
pin_inter = const(15) # Broche de connexion vers l'interrupteur
pin_bp = const(2) # Broche de connexion vers le bouton poussoir
pin_LDR = const(33) # Broche de connexion vers la LDR

SERVO_OPEN = const(0) # angle position servo-moteur "toit OUVERT"
SERVO_CLOSE = const(30) # angle position servo-moteur "toit FERME"

# station = network.WLAN(network.STA_IF) # STA_IF station Interface #  AP_IF : Access Point
station = network.WLAN(network.AP_IF)
station.ifconfig(('192.168.10.1', '255.255.255.0', '192.168.10.1', '8.8.8.8'))
ssid = 'wifigrp0'
passwrd = 'wifigrp0'

fdc_close = Pin( pin_close, Pin.IN ) # Déclaration des broches (fdc<->FinDeCourse)
fdc_open = Pin( pin_open, Pin.IN )
anemometre = Pin( pin_anemometre, Pin.IN )
interrupteur = Pin( pin_inter, Pin.IN )
bp = Pin( pin_bp, Pin.IN )
ldr = ADC( Pin(pin_LDR) ) # Capteur de lumière
ldr.atten(ADC.ATTN_11DB) # Conversion AD sur la plage de 0 à 3,3V
led = Pin( pin_ledBlanche, Pin.OUT )

OPEN = const(1)  # état des capteurs de fin de course pour l'ouverture du toit
CLOSE = const(0)
UNKNOWN = const(-1)

etat_toit = CLOSE # ATTENTION : VARIABLE GLOBALE (Le toit est fermé par défaut)

# Utilisation du BME280 en mode i2C
bus_i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
sensor = BME280 ( i2c = bus_i2c )

# Utilisation de l'écran LCD 1602
lcd = My_LCD( i2c = bus_i2c )

# Utilisation du PCF8574 pour récupérer la position de la girouette
girouette = Girouette ( i2c = bus_i2c )

# ============================================================================ lire_html (...)
def lire_fichier ( fichier_source:str ) -> str :
    """
    fonction qui permet de charger le fichier html.txt dans une variable texte
    Entrée : fichier_source -> nom du fichier à ouvrir
    Sortie : chaîne de caractères contenant le fichier html
    """
    with open(fichier_source,"r") as fichier : # Ouvrir le fichier html
        code = fichier.readlines()
    instructions = "".join(code) # assembler toutes les lignes
    if ".html" in fichier_source :
        instructions = instructions.replace("\n","") # supprimer les fin de lignes
        instructions = instructions.replace("\r","") # supprimer les retour à la lignes
    return instructions
# ======================================================================== connexion_wifi (...)
def connexion_wifi ( station:object, ssid:str, passwrd:str )->bool :
    """
    Initialisation de la connexion Wifi en mode Access Point
    L'ESP32 diffuse un SSID et peut distribuer une IP à ses Clients
    Entrée : station -> Objet réseau wifi
            ssid -> identifiant du réseau
            passwrd -> mot de passe pour se connecter à l'ESP32
    Sortie : indicateur booléen sur l'état de la connexion wifi
    """
    station.active(True)
    station.config(essid=ssid, password=passwrd) # création d'un point d'accès WiFi
#    station.connect(ssid, password) # connexion à un réseau Wifi disponible

    # ===== Attendre 7s que la connexion soit établie
    t0 = ticks_ms()
    delta_t = 0
    while station.active() == False and delta_t<7000 :
      delta_t = ticks_ms() - t0
      sleep(0.5)

    # ===== Si la connexion est établie afficher l'adresse IP
    if station.active() == True :
        print(" ---------- Connection Wifi -> OK")
        print(station.ifconfig())
        return True
    else:
        print("########## ECHEC d'initialisation de la connexion wifi ")
        return False

# ============================================================================= servo_degre ( )
def servo_degre ( servo:object, angle:int ):
    """
    Procédure qui reçoit :
        - un objet Pin (connexion servo-moteur)
        - l'angle souhaité pour le positionnement du servo-moteur
    Elle permet de faire la conversion pour obtenir la valeur
    du rapport cyclique pour le mode PWM ( duty )
    """
    pwm = int( ((angle * 95 ) // 180 ) + 30)
    servo.duty(pwm)
    sleep_ms(5) # temporisation pour gérer la vitesse de déplacemnt
    
# =========================================================================== fermer_toit (...)
def fermer_toit ( fdc:object, pin_servo:int )->bool:
    """
    Fonction qui permet de contrôler le servo moteur pour fermer le toit
    de la mini-serre.
    Entrée : fdc -> capteur de fin de course en fermeture
            pin_servo : n° de broche en mode PWM qui permet de piloter le servo moteur
    Sortie : True/False selon l'état du capteur de fin de course
    """
    fermeture_ok = fdc.value() # tester la valeur du fin de course
    if not fermeture_ok : # Si le toit n'est pas fermé, activier le moteur pour le fermer
        servo = PWM(Pin(pin_servo), freq=50)   # duty 180° -> cycle 30 < ... < 125
        for i in range ( SERVO_OPEN, SERVO_CLOSE+1 ):
            servo_degre ( servo, i) # Modification progressive de l'ouverture
            if fdc.value():
                break
        sleep(0.5)
        fermeture_ok = fdc.value()  # fdc = etat du toit avant de relâcher le servomoteur
        servo.deinit()
    if fermeture_ok :
        print(" ---------- Fermeture du toit -> OK")
    else :
        print(" ########## PROBLEME pour la FERMETURE du toit ")
    return fermeture_ok
# =========================================================================== ouvrir_toit (...)
def ouvrir_toit ( fdc:object, pin_servo:int )->bool:
    """
    Fonction qui permet de contrôler le servo moteur pour ouvrir le toit
    de la mini-serre.
    Entrée : fdc -> capteur de fin de course en ouverture
            pin_servo : broche en mode PWM qui permet de piloter le servo moteur
    Sortie : True/False selon l'état du capteur de fin de course
    """
    ouverture_ok = fdc.value() # tester la valeur du fin de course
    if not ouverture_ok : # Si le toit n'est pas ouvert, activer le moteur pour l'ouvrir
        servo = PWM(Pin(pin_servo), freq=50)   # duty 180° -> cycle 30 < ... < 125
        for i in range ( SERVO_CLOSE, SERVO_OPEN-1, -1 ):
            servo_degre ( servo, i) # Modification progressive de l'ouverture
            if fdc.value() :
                break
        sleep(0.5)
        ouverture_ok = fdc.value() # fdc = etat toit avant de relâcher le servomoteur
        servo.deinit()
    if ouverture_ok :
        print(" ---------- Ouverture du toit -> OK")
    else :
        print(" ########## PROBLEME pour l' OUVERTURE du toit ")
    return ouverture_ok
# =========================================================================== ouvrir_toit (...)
def periode_rotation ( sensor:object )->int:
    pulse_level = 0 # mesure de la largeur d'impulsion niveau bas
    temps=0
    for i in range(10):
        if not sensor.value(): # Attendre que la broche passe de 0 à 1
            pass
        val = time_pulse_us(sensor, pulse_level)
        if val != -2 : # -2 -> timeout
            temps += val
        else :
            i = i-1 # refaire la mesure
    moyenne=temps//10
    return moyenne
# ==============================================================================


if __name__ == "__main__":
# ========================================== test lcd et bouton poussoir    
    lcd.afficher(0, 0, "   Mini serre\n  connectée V1  ") # texte, x_pos, y_pos
    sleep(3)
# ========================================== test ouverture / fermeture du toit
    lcd.effacer()
    lcd.afficher(0, 0, "Test ouverture\nAppui sur BP ...")
    while not bp.value():
        pass
    sleep(0.3) # attendre fin rebond du bp
    ouvrir_toit( fdc_open, pin_servo )
    sleep(1)
    fermer_toit ( fdc_close, pin_servo )
    sleep(1)
# ========================================== test interrupteur    
    lcd.effacer()
    lcd.afficher(0, 0, "Test interruptr")
    etat_memo = True
    while not bp.value():
        etat = interrupteur.value()
        if etat != etat_memo  :
            if etat :
                lcd.afficher(0, 1, "  ===  ON  ===  ")
            else :
                lcd.afficher(0, 1, "  ===  OFF ===  ")
            etat_memo = etat
    sleep(0.3) # attendre fin rebond du bp
# ========================================== test interrupteur    
    lcd.effacer()
    lcd.afficher(0, 0, "Test LDR # LED")
    while not bp.value():
        val = ldr.read()
        if val < 2024 :
            if not led.value() :        
                txt = "LDR:{:4d}".format(val)
                lcd.afficher(0, 1, txt+"  LED ON" )
                led.on()
        else :
            if led.value() :
                txt = "LDR:{:4d}".format(val)
                lcd.afficher(0, 1, txt+" LED OFF" )
                led.off()
        sleep(0.25)
    sleep(0.3) # attendre fin rebond du bp
# ========================================== test BME280    
    lcd.effacer()
    lcd.afficher(0, 0, "Test BME280")
    while not bp.value():
        temp = "{:02.01f}°C".format(sensor.temperature)
        press = " / {:4.1f}".format(sensor.pressure)
        lcd.afficher(0,1,temp+press)
        sleep(0.25)
    sleep(0.3)
# ========================================== test Girouette   
    lcd.effacer()
    lcd.afficher(0, 0, "Test Girouette")
    pos_memo = ""
    while not bp.value():
        pos = girouette.pt_cardinal
        if pos != pos_memo :
            pos_memo = pos
            lcd.afficher(0, 1, "                 ")
            lcd.afficher(0, 1, pos)
    sleep(0.3)
# ========================================== test Anemometre   
    lcd.effacer()
    lcd.afficher(0, 0, "Test Anémometre")
    if interrupteur.value() :
        lcd.afficher(0,1,"SVP Inter -> Off")
    while interrupteur.value() :
        pass
    while not interrupteur.value():
        lcd.afficher(0,1,"=> attente BP...")
        while not bp.value():
            pass
        lcd.afficher(0,1,"... en cours ...")
        sleep(0.3)
        txt = "{:d}".format(periode_rotation ( anemometre ))
        lcd.afficher(0,1,"                ")
        lcd.afficher(0,1,txt+" us")
        sleep(3)
# ========================================== test Anemometre   
    lcd.effacer()
    lcd.afficher(0, 0, "=== Fin test ===")
    sleep(2)
    lcd.effacer()
    lcd.backlight_off()
    lcd.off()

        
        
  
            
    
    
        
        
    
    