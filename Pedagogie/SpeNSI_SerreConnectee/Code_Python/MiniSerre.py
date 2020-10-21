"""
Mise à jour 21/10/2020 - Version ESP32
"""
from serre_biblio import *

# ============================================================================= web_page (...)
def web_page(fdc_close:object, fdc_open:object, capteur:object)->str:
    """
    """
    if fdc_close.value() : # Déterminer l'état du toit
        toit_html="FERMÉ"
    elif fdc_open.value() :
        toit_html="OUVERT"
    else :
        toit_html="## INCONNU ##"
    
    page_html = lire_fichier ( "www/index.html" ) 
    page_html = page_html.replace("<variable_toit>",toit_html)
    page_html = page_html.replace("<variable_temperature>",str(capteur.temperature))
    page_html = page_html.replace("<variable_pression>",str(capteur.pressure))
    
    css = lire_fichier ( "www/style.css")
    page_html = page_html.replace("<fichier_css>", css)
    
    js = lire_fichier ( "www/script.js")
    if toit_html == "FERMÉ" :
        js = js.replace("<variable_toit>", "close")
    elif toit_html == "OUVERT" :
        js = js.replace("<variable_toit>", "open")
    else :
        js = js.replace("<variable_toit>", "???")
    page_html = page_html.replace("<fichier_js>", js)
    
    return page_html

# ===========================================================================================
# ==================================================================================== main
test_toit = fdc_close.value()
if not test_toit : # Condition initiale : Fermeture du toit
    test_toit = fermer_toit ( fdc_close, pin_servo )

test_wifi = False
if test_toit :# Initialiser la station WiFi
    test_wifi = connexion_wifi ( station, ssid, passwrd )

try :
    temp = sensor.temperature
    test_bme280 = True
except :
    print("############# Problème de lecture avec le BME280 !")
    test_bme280 = False
    
if test_toit and test_wifi and test_bme280 : # Tout est OK => Attendre une requête
        
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.bind(('', 80))
    my_socket.listen(3)
    print("============= INITALISATION TERMINÉE ==============")
    print("Attente de connexion ...")
    # while station.isconnected() : # Si connexion à un réseau Wifi, en mode STA_IF
    repondre = False
    while True : # En mode AP_IF
        conn, addr = my_socket.accept()
        print("\nRéception d'une requête depuis : "+ str(addr))
        request = conn.recv(1024)
        request = str(request)
        print('================================ Entête de la requête =================')
        print('{:s}'.format(request)) 
        print('=======================================================================\n')
        ouverture = request.find('/?open_toit=1') # Récupérer les arguments dans l'URL
        fermeture = request.find('/?close_toit=1')
        requete = request.find('GET / HTTP')
        if requete == 2 : # Eviter de gérer des connexions parasites
            repondre = True
            
        if ouverture == 6:
            print("-------> Commande d'ouverture")
            print("ETAT TOIT commande de ouverture ->",etat_toit)
            if etat_toit != OPEN :
                retour = ouvrir_toit ( fdc_open, pin_servo )
                etat_toit = OPEN if retour else UNKNOWN
            repondre = True
            
        if fermeture == 6:
            print("-------> Commande de fermeture")
            print("ETAT TOIT commande de fermeture ->",etat_toit)
            if etat_toit != CLOSE :
                retour = fermer_toit ( fdc_close, pin_servo )
                etat_toit = CLOSE if retour else UNKNOWN
            repondre = True
            
        if repondre :
            print("-------> Requête traitée -> envoi réponse ...")

            response = web_page( fdc_close, fdc_open , sensor ) # Construction de la page Web

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()
            repondre = False



