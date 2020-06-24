"""
Menu de démarrage de la carte SOPROLAB
"""
from SOPROLAB_V2 import *
from machine import reset
from micropython import const

menu_Python = const ( 0 )
menu_MonProg = const ( 1 )
menu_Pression = const ( 2 )
menu_Thermometre = const ( 3 )
menu_Distance = const ( 4 )
menu_RecupData = const ( 5 )
menu_RecepGPS = const ( 6 )
menu_Serveur_Web = const ( 7 )
menu_Vitesse_son = const ( 8 )

fichiers_python = [ "P1_< Python >", "P2_MonProg.py", "P3_Pressiometre." ,
    "P4_Thermometre.py", "P5_Distance.py", "P6_Recup_data.py",
    "P7_Recep_GPS.py" , "P8_Serveur_Web.py", "P9_Vitesse_son.py"]

menu = [ "1> Python", "2-MonProg.py","3-Pression",
         "4-Température", "5-Distance", "6-Récup_Data",
         "7-Récep GPS","8-Serveur_Web", "9-Vitesse du Son" ]

# ======================================================================  menu_main
def menu_main ( ):
    try :
        LCD.backlight_on()
        LCD.afficher (0, 0, "BP -> Valider...")
        LCD_connected = True # LCD Ok
    except :
        print("Le module LCD ne semble pas en place ...")
        print("Fonctionnement en mode PROGRAMMATION microPython")
        LCD_connected = False # LCD Ok
 # pas de menu possible
    BP.drapeau = False
    choix0 = len(menu)+1  # permet de rentrer dans la boucle
    # ---------    AFFICHAGE DU MENU  ---------
    while choix0 > len(menu) : # 8 -> correspond au choix [ 9-Serveur_Web ]
        if LCD_connected :
            while not BP.drapeau :
                choix = int(POT.valeur // 512)
                if choix != choix0 :
                    choix0 = choix
                    LCD.afficher ( 0, 1, menu[choix] )
                sleep_ms(200)
            BP.drapeau = False
        else :
            print( "Possibilités d'initialisation de programmes : ")

            for i in range(len(menu)) :
                print("  [{:d}]-> {:7s}".format(i+1, menu[i]))
            while not (0 <= choix0  < len(menu) ) : # so choix <0 ou max <= choix
                erreur_choix=0 # pas d'erreur en saisie clavier par defaut
                try :
                    choix0 = int(input("Choix du programme à lancer ? "))
                    choix0 = choix0 - 1
                except :
                    erreur_choix=1
                if erreur_choix or choix0 < 0 or len(menu) <= choix0 :
                    print("\nMerci de choisir entre : [ ", end='')
                    for i in range (1, len(menu)+1):
                        print(" ",i," ", end='')
                    print(" ]")            
#    print("=== Choix du menu : ",choix0, " ===")
    return choix0

# ======================================================================  choisir_delta_t
""" mini correspond au delta_t minimum proposé """
def choisir_delta_t( mini=100 ):
    global LCD_connected
    # tempo minimum 100 ms / proposer des tempo multiples de 100ms
    select_time = [ 'Retour Mesure', '0,1 sec', '1 sec', '5 sec',
                    '10 sec', '30 sec', '1 min', '5 min',
                    '10 min', 'Retour Menu >' ] # Affichage menu
    # Période d'échantillonage en millisecondes
    delta_time = [ 0, 100, 1000, 5000, 10000, 30000, 60000, 300000, 600000, -1 ]
    i = 1
    while delta_time[i] < mini and delta_time[i] > 0: # enlever les valeurs trop basses (GPS)
        delta_time.pop(i)
        select_time.pop(i) # ne pas faire i = i+1 il faut supprimer que le deuxième élément
    
    delta_t = 0
    choix0 = int(POT.valeur * (len(select_time)-1) // 4095 )
    choix=len(select_time)+1 # permet de rentrer dans la boucle while (saisie clavier :except)
    try :
        LCD.backlight_on()
        LCD.afficher ( 0, 0, "Choix période :")
        LCD.afficher ( 0, 1, select_time[choix0] )
        BP.drapeau = False
        while not BP.drapeau :  # Tant que le choix n'est pas validé            
            choix = int(POT.valeur * (len(select_time)-1) // 4095 )
            if choix != choix0 :
                choix0 = choix
                LCD.afficher ( 0, 1, select_time[choix] )
            sleep_ms(200)
        BP.drapeau = False
        LCD.effacer()
    except :  
        erreur_choix=0 # pas d'erreur en saisie clavier par defaut
        print("Possiblités pour la période d'échantillonnage : ")
        for i in range(len(select_time)) :
            print(" [{:d}]-> {:7s} #".format(i+1, select_time[i]))
        while not (0 <= choix  < len(select_time) ) : # so choix <0 ou max <= choix
            try :
                choix = int(input("Choix de la période d'échantillonnage ? "))
                choix = choix - 1
            except :
                erreur_choix=1
            if erreur_choix or choix < 0 or len(select_time) <= choix :
                print("Merci de choisir entre : [ ", end='')
                for i in range (len(select_time)):
                    print(" ",i+1," ", end='')
                print(" ]")
                print("Choisir [ 1 ] pour annuler l'enregistrement des données\n")
            print("delta_t sélectionné : ", select_time [ choix ])
    delta_t =  delta_time [ choix ]
    return delta_t
# retourne 0 -> Annuler retour aux mesures
# retourne -1 -> Fin du mode sélectionner retour au menu main

NEOPIX.arc_en_ciel ( )

# modification en attendant de trouver une solution
# au blocage de la carte au démarrage avec la fonction input ...
#retour = 1
try : # LCD Ok
    LCD.effacer ( )
    LCD.afficher( 0, 0, " SoproLab V2")
    retour = -1 # fin normale d'un programme -> boucler sur le menu
except :
    retour = 1 # Pas de module LCD connecté

# ========================================== tant que choix différent de Python ( )
while retour == -1 :
 
    choix0 = menu_main ( )
    
    # =================================================== Python ====
    if choix0 == menu_Python :
        retour = 0
    # =================================================== MonProg ( )
    if choix0 == menu_MonProg :
        try :
            from P2_MonProg import *
            MonProg ( )
        except :
            retour = choix0
    # =================================================== Pressiometre ( )
    if choix0 == menu_Pression :
        try :
            from P3_Pressiometre import Pressiometre
            retour = Pressiometre ( )
        except :
            retour = choix0
    # =================================================== Thermometre ( )
    if choix0 == menu_Thermometre :
        try :
            from P4_Thermometre import Thermometre
            retour = Thermometre ( )
        except :
            retour = choix0
    # =================================================== Distance ( )
    if choix0 == menu_Distance :
        try :
            from P5_Distance import Distance
            retour = Distance()
        except :
            retour = choix0
    # =================================================== Recup_data ( )
    if choix0 == menu_RecupData :
        try :
            from P6_Recup_data import Recup_data
            Recup_data ( )
        except :
            retour = choix0
    # =================================================== Recep_GPS ( )
    if choix0 == menu_RecepGPS :
        try :
            from P7_Recep_GPS import *
            Recep_GPS ( )
        except :
            retour = choix0
    # =================================================== Serveur_Web ( )
    if choix0 == menu_Serveur_Web :
        try :
            from P8_Serveur_Web import Serveur_Web
            Serveur_Web( )
        except :
            retour = choix0
    # =================================================== Vitesse_son ( )
    if choix0 == menu_Vitesse_son :
        try :
            from P6_Vitesse_son import Vitesse_son
            retour = Vitesse_son ( )
        except :
            retour = choix0
    if retour > 0 :  # ERREUR d'initialisation
        try :
            LCD.effacer()
            LCD.afficher ( 0, 0, "# ERREUR init. #")
            LCD.afficher ( 0, 1, fichiers_python[retour])
        except :
            print ("\n\n### Problème de lancement du module [", fichiers_python[retour],"] #### \n\n" )
        sleep ( 4 )
    else : # fin normale du programme ( 0 -> Python )
        try :
            LCD.effacer()
            LCD.afficher ( 0, 0, "Fin du programme" )
            sleep(1)
        except :
            print ( "\n\n===== Fin du programme =====\n\n" )
        sleep ( 2 )
# ===================================== choix0 = 0 AND retour = 0 -> menu_Python
try : # LCD Ok
    LCD.effacer ( )
    LCD.afficher( 0, 0, "  Mode REPL :   Programme Python")
    LCD.backlight_off ( )
except :
    print( "\n\nMode REPL :   Programme Python  \n")
    