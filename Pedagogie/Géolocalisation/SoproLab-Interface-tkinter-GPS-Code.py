"""
Développement d'une interface graphique avec la bibliothèque tkinter pour :
- capturer les données transmises via le port USB (trames NMEA)
- enregistrer les données dans un fichier [texte]
    Les trames NMEA peuvent être fournies par un capteur GPS ou un microcontrôleur. Selon le type de source, le pilote d'interface
et la configuration du port USB différent. Il est donc nécessaire de choisir une configuration du port USB avant de lancer la
captation des données.

    La fonction [mainloop] de la bibliothèque tkinter rend difficile le contrôle en parallèle d'un autre processus indépendant.
    Le mode de fonctionnement est donc basé sur la mise en place des Thread. C'est aussi un choix pédagogique.
"""
# Importation des bibliothèques python
from tkinter import *    # Interface graphique
from serial import *   # Lecture de données disponibles sur le port USB
from threading import Thread    # Gestion de deux parties du programme qui fonctionnent en parallèle (interface grahique / captation des données)
import time    # gestion de l'horodatage pour le nom de fichier de données
from tkinter.messagebox import *

# Variable de controle
bouton_save = False
bouton_save_ok = False
bouton_exit = False
etat_usb = False # Port USB configuré ou non
fin_tempo = True # Temporisation entre deux captation -> synchronisation de la Thread captation avec quitterAppli
path_fichier = '/Users/jacqueschouteau/Desktop/'
# ============================================= AFFICHER_VARIABLES 
"""
Fonction de débeugage
"""
def afficher_variables ( texte ) :
    global bouton_save
    global bouton_save_ok
    global bouton_exit
    global etat_usb
    global fin_tempo
    
    print("\n\n========================== ", texte )
    print("bouton_save : ", str(bouton_save))
    print("bouton_save_ok :", str(bouton_save_ok))
    print("bouton_exit: ", str(bouton_exit))
    print("etat_usb :", str(etat_usb))
    print("fin_tempo :", str(fin_tempo))

# ============================================= DELTA_T_SHOW 
"""
Configurer la connexion avec le port USB
"""
def param_USB ( ):
    global port_usb
    global etat_usb
    
# Déclaration de variables et essais de configuration du port USB
# pour proposer une configuration OK par défaut
 
    try :   # Tester si le port USB peut être ouvert avec la carte SoproLab    
        port_usb = Serial('/dev/tty.SLAB_USBtoUART', 115200, timeout=6, writeTimeout=1)
        config_usb1.select() # Carte Soprolab configurée par défaut pour la connexion USB
        ligne = port_usb.readline()
        etat_usb = True
    except :
        pass
    if not etat_usb : # Tester si le port USB peut être ouvert avec lecapteur GPS    
        try :   # Tester si le port USB peut être ouvert avec la carte SoproLab    
            port_usb = Serial('/dev/tty.usbserial-00000000', 9600, timeout=6, writeTimeout=1)
            config_usb2.select() # Capteur GPS configuré par défaut pour la connexion USB
            ligne = port_usb.readline()
            etat_usb = True                     
        except :
            pass
    if not etat_usb :   # Aucune des deux config n'est satisafaisante ! -> informer du besoin de modifier la configuration
        showinfo("Configuration du port USB",
                "Merci de vérifier la connexion sur le port USB\n" +
                "ou de modifier le choix de configuration ...")
        transfert_ctrl["state"]='disable' # Activer le bouton de d'enregistrement
        ligne=b'#FFFF'
    return ligne
# ============================================= QUITTER_APPLI 
"""
Mettre la réaction au clique sur le bouton [QUITTER]
Cette fonction permet de gérer les interactions entre la Thread principale (tkinter) et
la Thread de gestion de la captation des données lorsque l'utilisateur clique sur [QUITTER]
"""
def quitterAppli ( ):
    global monAppli
    global bouton_exit
    global fin_tempo
    
    bouton_exit = True
    while not fin_tempo : # Attendre que la Thread captation se termine
        pass
    time.sleep(0.5) # Temporisation pour ecriture des données dans le fichier avant de le fermer
    
    monAppli.quit()

# ============================================= START_STOP 
"""
Gérer la réaction au clique sur le bouton [Enregistrer] / [Terminer l'enregistrement ...]
Cette fonction permet de gérer les interactions entre la Thread principale (tkinter) et
la Thread de gestion de la captation des données lorsque l'utilisateur clique sur le bouton d'enregistrement

"""
def start_stop ( ):
    global bouton_save
#    global bouton_save_ok
    if bouton_save :  # 2eme clic sur [SAVE] et [record] en cours -> Terminer l'enregistrement
        bouton_save = False
        transfert_ctrl_txt.set("[ ENREGISTRER ]")
    else : # 1er clic sur [SAVE]
        bouton_save = True
        transfert_ctrl_txt.set("[ TERMINER l'enregistrement ]")
    
# ============================================= USB_TXT
"""
Cette fonction convertit en une chaine de données de type [byte] du port USB en [STR] pour être enregistrée.
"""
def usb_txt ( ligne ) -> str :
    # Convertir les données du format [byte] -> au format [texte]
    trame_str = str( ligne ) # trame_str = b'....\r\n'
    n = len(trame_str)-5 # retirer [b'] en début de trame et [\r\n'] en fin de trame
    chaine = trame_str[2:n]
    return chaine
# ============================================= CAPTATION
"""
Ce Thread a pour fonction de gérer la captation des données en parallèle de l'interface graphique.
"""
# Le problème dans ce Thread est de ne pas bloquer l'affichage de l'interface avec les boucles de contrôle et d'attente
# ni de bloquer la Thread dans une boucle while et empécher ainsi l'interface de se fermer -> Plantage
class captation ( Thread ):
    def __init__ ( self ):
        Thread.__init__(self)
    
    def run ( self ):
        global etat_usb
        global bouton_save
        global bouton_save_ok
        global bouton_exit
        global fin_tempo

        etat_usb = False
        time.sleep(0.8) # Attendre que la Thread principale affiche l'interface graphique

# Tant que l'utilisateur n'a pas cliqué sur [QUITTER] garder la Thread active
        while not bouton_exit :
            # Attendre que l'utilisateur active l'enregistrement par un clic sur [SAVE_STOP]
            # ou quitte l'application s'il clique sur [QUITTER] (Thread principale)
            while not bouton_save and not bouton_exit :
                pass
            if bouton_exit : # Sortir
                break
            # Tant que le port USB n'est pas correctement configuré
            while not etat_usb :
                ligne = param_USB ( )
                
                if not etat_usb : # Problème lors de la lecture d'une ligne de données
                    bouton_save = False
                    bouton_save_ok = False
                    break

            # Si l'utilisateur a cliqué [ENREGISTRER] et configuration du port USB est OK
            if etat_usb and bouton_save :
                fenetre_data.delete(0,fenetre_data.size()) # Efffacer la fenêtre d'affichage de données
                fenetre_data.insert(0,"================== Début des enregistrements ==================")
                cptr_ligne=1 # compteur de lignes dans la fenêtre d'affichage

                # Construire le nom du fichier de données avec [DATA_PGS_Année/mois/jour_heure h minutes.txt]
                nom_fichier = path_fichier+"DATA_GPS_"
                jour=time.localtime() # récupérer les données d'horodatage du poste
                for i in range (5):
                    nom_fichier = nom_fichier+"{:02d}".format(jour[i]) # Année/Mois/Jour/Heures/Minutes
                    if i==2 :
                        nom_fichier = nom_fichier + "_"
                    if i==3 :
                        nom_fichier = nom_fichier + "h"                        
                nom_fichier = nom_fichier+".txt"
                cptr_pos = 0 # Compteur de position
                    
            # Si l'ouverture du fichier de données en écriture [DATE-HEURE h MINUTE.txt] ne pose pas de problème
                with open ( nom_fichier,'w', newline='\n') as MyFile : 
                    bouton_save_ok = True # Enregistrement en cours ...
        # Tant que l'utilisateur n'a pas cliqué sur [Stop] ni sur [ QUITTER ]
        
                    while bouton_save and not bouton_exit :
            # Attendre la première trame NMEA de la position actuelle                        
                        while not '$GPVTG' in str(ligne) and not bouton_exit and bouton_save:
                            ligne = port_usb.readline()
                        if bouton_exit or not bouton_save:
                            break;
                        
                        cptr_pos = cptr_pos + 1    # Enregistrer / afficher le numéro de position actuel
                        MyFile.write(str(cptr_pos)+'\n')
                        cptr_ligne = cptr_ligne + 1                        
                        fenetre_data.insert(cptr_ligne,str(cptr_pos))
                        
                        trameNMEA = usb_txt ( ligne ) # Mémoriser la première trame et passer à la trame suivante
            # Enregistrer / Afficher la première trame de la position actuelle 
                        MyFile.write(trameNMEA+'\n') # Enregistrer la trame dans le fichier
                        cptr_ligne = cptr_ligne + 1
                        fenetre_data.insert(cptr_ligne, trameNMEA) # Afficher la trame
                        if cptr_ligne > 25 :
                            fenetre_data.yview_moveto(cptr_ligne)
                    
                        ligne = port_usb.readline()  # Lire la trame suivante

            # Tant que la Première trame de la position suivante n'est pas reçue
                        while not '$GPVTG' in str(ligne) and not bouton_exit and bouton_save: 

                # Capturer chaque ligne de données sur le port USB -> [ USB_TXT() ]            
                            trameNMEA = usb_txt ( ligne )
                            
                # Enregistrer / Afficher la ligne de texte correspondant à la trame            
                            MyFile.write(trameNMEA+'\n') # Enregistrer la trame dans le fichier
                            cptr_ligne = cptr_ligne + 1
                            fenetre_data.insert(cptr_ligne, trameNMEA) # Afficher la trame
                            if cptr_ligne > 25 :
                                fenetre_data.yview_moveto(cptr_ligne)
                            ligne = port_usb.readline()  # Lire la trame suivante
                        if bouton_exit or not bouton_save:
                            break;
                        # Attendre delta_t secondes avant la prochaine position                         
                        fin_tempo = False
                        tempo = int(delta_t.get() ) * 10 
                        for n in range ( tempo ) :
                            if bouton_exit or not bouton_save :
                                break
                            time.sleep (0.1)
                        fin_tempo = True
                        port_usb.flush() # Vider le buffer du port USB
                        
        # fermer le fichier [DATE-HEURE-MINUTE.txt] pour provoquer l'écriture physique des données dans le fichier
                    MyFile.close()
                    fenetre_data.insert(cptr_ligne+1,"================== Enregistrement des données dans le fichier :")
                    fenetre_data.insert(cptr_ligne+2, nom_fichier )
                    fenetre_data.insert(cptr_ligne+3,"==================" )
                    if cptr_ligne+3 > 25 :
                        fenetre_data.yview_moveto(cptr_ligne)
                bouton_save = False # Revenir à l'attente du clic sur [Enregistrer] en mode record dans la Thread
        if etat_usb :
    # fermer le port USB
            port_usb.close()

# ============================================= Programme principal
# Créer l'interface graphique

    # Créer la fenêtre principale
monAppli = Tk()    
monAppli.title (">====> Transfert de données de géolocalisation >=====>")
monAppli.geometry("980x600")
monAppli.config(bg='#0080A0') # Couleur fond
    # Créer une zone d'affichage des données avec un ascenseur sur le côté
zone_data = Frame ( monAppli ) 
zone_data.grid(row=0, column=0, padx=10, pady=10)
    # Créer une zone de conrôle de l'application
zone_control = Frame ( monAppli, bg='#D0D0F0' ) 
zone_control.grid(row=1, column=0, padx=10, pady=10)

    # -> ZONE_DATA -> Créer la frame d'affichage des données 
fenetre_data = Listbox( zone_data, bg='#A0A0C0',  # Affichage des données
                        height=25, width=100, relief='groove' )
ascen_data = Scrollbar( zone_data,  bg='#D0D0F0',    # Ascenceur
                        relief='groove')
fenetre_data.config ( yscrollcommand = ascen_data.set )
ascen_data.config ( command = fenetre_data.yview )
fenetre_data.pack( side=LEFT, padx=10, pady=10  )
ascen_data.pack( side=RIGHT, padx=10, pady=10   )
fenetre_data.insert(1,"En attente de réception de données à enregistrer ...")

    # -> ZONE_CONTROL -> Créer une zone de configuration du port USB
choix_config_usb = StringVar()
choix_config_usb.set("none")
delta_t_text = Label( zone_control, text="Intervalle \nde temps (s)", bg='#D0D0F0' )
delta_t_text.grid (row=1, column=0, padx=10 )
delta_t = StringVar() # Nombre de secondes entre deux enregistrements si utilisation du capteur GPS
delta_t.set(5)
delta_box = Spinbox( zone_control, from_=5, to=245, increment=10, textvariable=delta_t,
                     width=4, justify='center', relief='groove', state='normal' )
delta_box.grid (row=2, column=0, padx=10, pady=5)
config_label = Label (zone_control, text="Configuration du port USB :",
                      fg='#202040', bg='#D0D0F0', height=1)
config_label.grid(row=0, column=1, padx=10 )
config_usb1 = Radiobutton ( zone_control, text="Carte SoproLab",
                           value="soprolab", variable=choix_config_usb,
                           height=1, width=20, bg='#D0D0F0', command=param_USB )
config_usb1.grid(row=1, column=1, padx=30 )
config_usb2 = Radiobutton ( zone_control, text="Capteur GPS",
                           value="capteur", variable=choix_config_usb,
                           height=1, width=20, bg='#D0D0F0', command=param_USB   )
config_usb2.grid(row=2, column=1, pady=5 )

    # Créer une zone de commande avec les boutons [ Enregistrer ] et [ Quitter ]
transfert_ctrl_txt = StringVar()
transfert_ctrl_txt.set("[ ENREGISTRER ]")
transfert_ctrl = Button ( zone_control, textvariable=transfert_ctrl_txt, state='normal',
                          height=2, width=20, relief='groove', command=start_stop )
transfert_ctrl.grid(row=1, column=2, padx=30, pady=5 )
quitter = Button ( zone_control, text=" QUITTER ",
                   height=2, width=20, relief='groove', command=quitterAppli )
quitter.grid(row=1, column=3, padx=30, pady=5 )

# Tester la configuration du port USB et ajuster les varaibles d'environnement
param_USB ( )

# Lancer une deuxième Thread : réception des données
threadCaptation = captation()
threadCaptation.start()

#Interface graphique dans la Thread principale
monAppli.mainloop()

# Fermer les Thread et terminer l'application
# Attendre la fin de la deuxième Thread
threadCaptation.join()

monAppli.destroy()