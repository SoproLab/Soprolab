"""
Serveur réseau
Objets connectés
"""
import esp
import gc
import network

from SOPROLAB_V2 import *

def Serveur_Web ( ):
    
    esp.osdebug(None)
    gc.collect()
    try:
        import usocket as socket
    except:
        import socket
    
    try:
        LCD.effacer()
        LCD_plugged = True
    except:
        LCD_plugged = False


    print("Fonctionnement en serveur ....")

    SSID_WIFI = "???" # Votre SSID Wifi
    MOT_PASSE_WIFI = "???" # Votre mot de passe Wifi
 
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(SSID_WIFI , MOT_PASSE_WIFI)

    cptr0 = ticks_ms()
    cptr = 0
    while ( not station.isconnected() ) and cptr<5000 : # Attendre 5s pour connexion
      cptr = ticks_ms() - cptr0  
      pass

    if station.isconnected() :
        A,B,C,D = station.ifconfig()

        if LCD_plugged==True:
            LCD.effacer()
            LCD.backlight_on()
            LCD.afficher ( 0, 0, "IP:"+A)
            LCD.afficher ( 0, 1, "Serveur waiting")
            sleep(1)
        else:
            print('IP:',A)
            print("Serveur en attente de connexion ...")       
        SoproLab_Connected = True
        from start import *
    else:
        if LCD_plugged==True:
            LCD.effacer()
            LCD.afficher(0, 0, 'IP:--.--.--.--  Init Serv Failed')
        else:
            print('IP:--.--.--.--')
            print("L'initialisation du serveur a échouée !")
        SoproLab_Connected = False
        return 9
# ----------------------------------------------------------------------------
# Serveur_Web() # Pour tester le fonctionnement de la bibliothèque en dehors du mode menu