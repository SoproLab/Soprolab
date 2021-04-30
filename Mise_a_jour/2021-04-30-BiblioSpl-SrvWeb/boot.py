# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import sys
import network
from time import ticks_ms
from Dechiffrement import dechiffrement

"""
Initialisation de la connexion Wifi en mode Access Point
"STA" connexion à un réseau local  //  "AP" -> serveur DHCP en local
"""
access = "STA" 
if access == "STA" : # STA_IF station Interface
    infos_access = ('192.168.1.210', '255.255.255.0', '192.168.1.1', '213.186.33.102')
    station = network.WLAN(network.STA_IF)
    station.ifconfig( infos_access )
    station.active(True)
    try :
        # Remplacer dechiffrement("myVy2HNry9") par la ligne ci-dessous avec votre SSID wifi
        # ssid = "--- ? ---"
        ssid = dechiffrement("k@@@eu9DRW")
        
        # Remplacer dechiffrement("Zqs&Oeq8MLey9u5w8qy5") par la ligne ci-dessous avec votre password wifi
        # passwrd = "--- ? ---"
        passwrd = dechiffrement("VEjl2HbTrjUKmVRsVh@h")
        station.connect(ssid, passwrd) # connexion à un réseau Wifi disponible
            # ===== Attendre 7s que la connexion soit établie
        t0 = ticks_ms()
        delta_t = 0
        while station.active() == False and delta_t<7000 :
          delta_t = ticks_ms() - t0
          sleep(0.5)
        if station.active() == True :
            print("Connection Wifi -> Mode Objet Connecté au réseau Wifi ...")
            print(station.ifconfig())
            Wifi_Connected = True

    except :
        print("########## ECHEC d'initialisation de la connexion wifi ")
        print("Clé de déchiffrement absente ...")
        print("Merci de renseigner le SSID et le PASWORD dans boot.py")
        Wifi_Connected = False

else : #  AP_IF : Access Point
    ssid = 'WiFi-ESP32'
    passwrd = 'Soprolab'
    infos_access = ('192.168.10.1', '255.255.255.0', '192.168.10.1', '8.8.8.8')
    station = network.WLAN(network.AP_IF)
    station.ifconfig( infos_access )
    station.config(essid=ssid, password=passwrd) # création d'un point d'accès WiFi
    station.active(True)
    if station.active() == True :
        print("Connection Wifi -> Réseau : ", ssid)
        print(station.ifconfig())
        Wifi_Connected = True
    else :
        Wifi_Connected = False
        
    
