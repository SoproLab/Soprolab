from Soprolab import *
from uselect import poll, POLLIN
try:
  import usocket as socket
except:
  import socket

global Wifi_Connected

# ============================================================================= web_page (...)
def web_page( )->str:
    page_html = lire_fichier ( "index.html" )
    
    fichier_css = lire_fichier ( "style.css" )
    # Replacer le CSS dans le HTML
    page_html = page_html.replace("<fichier_css>",fichier_css)

    fichier_js = lire_fichier ( "script.js" )
    # Mettre à jour l'état de la variable dans le JS
    etat_ledv = "ON" if ledv.value() else "OFF"
    fichier_js = fichier_js.replace("<etat_Ledv>",etat_ledv)
    # Replacer le JS dans le HTML    
    page_html = page_html.replace("<fichier_js>",fichier_js)
                                  
    page_html = page_html.replace("<variable_Potentiometre>",str(pot.valeur))
    page_html = page_html.replace("<variable_Pression>",str(bmp.pression))
    page_html = page_html.replace("<variable_Temperature>",str(bmp.temperature))

    return page_html

# ===========================================================================================
# ==================================================================================== main    
if Wifi_Connected :
    lcd.on()
    lcd.backlight_on()
    lcd.effacer()
    lcd.afficher(0, 0, "Soprolab :")
    lcd.afficher(0, 1, station.ifconfig()[0])
    sleep_ms(3000)
    
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('', 80))
    my_socket.listen(3)
    print("============= INITALISATION TERMINÉE ==============")
    lcd.effacer()
    lcd.afficher(0, 0, "Web connected...")
    lcd.afficher(0, 1, '.')
    repondre = False
    while True : # En mode AP_IF
        connexion = []
        poller = poll()
        poller.register(my_socket, POLLIN)
        i = 0
        while connexion==[] :
            connexion = poller.poll(1000)
            lcd.afficher(i%15, 1,' ')
            i += 1
            lcd.afficher(i%15, 1,'.')
        conn, addr = my_socket.accept()
        lcd.effacer()
        lcd.afficher(0, 0, "Connexion :")
        lcd.afficher(0, 1, str(addr[0]))
        request = conn.recv(1024)
        request = str(request)
        print('================ Entête de la requête =================')
        print('{:s}'.format(request)) 
        print('=======================================================\n')
        ledv_on = True if request.find('/?ledv_on')==6 else False # Récupérer les arguments dans l'URL
        ledv_off = True if request.find('/?ledv_off')==6 else False
        serveur_down = True if request.find('/?serveur_off')==6 else False
        
        if serveur_down :
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.close()
            break;
        
        requete = True if request.find('GET / HTTP')==2 else False
             
        if requete: # Eviter de gérer des connexions parasites
            repondre = True
            
        if ledv_on :
            # print("-------> Allumer la led verte")
            ledv.on()
            repondre = True
            
        if ledv_off :
            # print("-------> Eteindre la led verte")
            ledv.off()
            repondre = True
            
        if repondre :
            # print("-------> Requête traitée -> envoi de la réponse ...")

            reponse_html = web_page( ) # Construction de la page Web

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(reponse_html)
            conn.close()
            repondre = False
        sleep_ms(1000)

    my_socket.close()
    print("============= SERVEUR DOWN ==============")
    print("Fin du programme ...")

lcd.backlight_on()
lcd.effacer()
lcd.afficher(0, 0, "Fin du programme")
lcd.afficher(2, 1, "principal.")
sleep_ms(3000)
lcd.effacer()
lcd.backlight_off()
lcd.off()

