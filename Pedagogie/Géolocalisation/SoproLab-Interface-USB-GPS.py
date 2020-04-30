"""
Objectif : lire les données transmises sur le port USB
pendant une durée déterminée.


"""
# Module de lecture/ecriture du port série
# -*- coding: UTF8 -*-

from serial import *
from time import monotonic
# Port série /dev/tty.SLAB_USBtoUART
# Vitesse de baud : 115200
# Timeout en lecture : 6 sec
# Timeout en écriture : 1 sec

chemin = '/Users/jacqueschouteau/Documents/@-ESP32/ESP32-Interface-MacOS/'+'DATA-GPS.txt'
with open ( chemin,'w', newline='\n') as MyFile :
    
#    port_usb = Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=6, writeTimeout=1)
    port_usb = Serial('/dev/tty.usbserial-00000000', 9600, timeout=6, writeTimeout=1)
        
    if port_usb.isOpen():
    # Lire le compteur de temps monotonic de l'ordinateur
        t0 = int(monotonic())
        t1 = 0
        cptr = 1
        print(cptr)
        MyFile.write(str(cptr)+'\n')

        while t1 < 120 : # Mémoriser le transfert pendant 2 min
            
            ligne = port_usb.readline() # Reçoit des byte
            
            fin = len(ligne)-2 # enlever ...[\r\n']
            chaine = str(ligne[:fin])  # enlever [b']...
            fin = len(chaine)-1 # chaine="b' ... '"
            chaine2 = chaine[2:fin] # enlever [b'] et [']
            if '$' in chaine2 :

                print(chaine2)
                MyFile.write(chaine2+'\n')
                
                if '$GPRMC' in chaine2 :
                    cptr = cptr + 1
                    print(cptr)
                    MyFile.write(str(cptr)+'\n')
                                  
            t1 = int(monotonic()) - t0
        
        port_usb.close()
    MyFile.close()
