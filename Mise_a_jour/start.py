from SOPROLAB_V2 import *
from microWebSrv import MicroWebSrv
# ----------------------------------------------------------------------------  POST

@MicroWebSrv.route('/formPOST')
def _httpHandlerFormPOST(httpClient, httpResponse) :
    LCD.afficher( 0, 1, "Req form POST")
    # stockage de la page web dans une variable texte
    print("########## HTTP - Demande Connexion Client ########## POST")
    msg = httpClient.GetRequestHeaders()
    print(msg)
    print("=============================")
    content = """\
    <!DOCTYPE html>
    <html lang=fr>
        <head>
            <meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h4>TEST méthode : POST</h4>
            IP address du Client = %s <br />
            <h5>Merci de vous identifier :</h5>
            <form action="/test" method="POST" accept-charset="ISO-8859-1">
                Login : <input type="text" name="logId"><br />
                Password : <input type="password" name="passwrd"><br />
                <input type="submit" value="VALIDER">
            </form>
        </body>
    </html>
    """ % httpClient.GetIPAddr()
    # Le serveur répond en envoyant la page web 
    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )

@MicroWebSrv.route('/test', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse) :
    try :
        LCD.backlight_on()
        LCD.afficher( 0, 1, "form method POST")
        LCD_ok=True
    except:
        LCD_ok=False
    formData  = httpClient.ReadRequestPostedFormData()
    print("########## HTTP - Retour formulaire Client ########## POST")
    msg = httpClient.GetRequestHeaders()
    print(msg)
    print("======= Données =============")
    print(formData)
    print("=============================")
    logId = formData["logId"]
    passwrd  = formData["passwrd"]
    if passwrd=='NSI':
        msgAffiche = 'Ok '+MicroWebSrv.HTMLEscape(logId)+' vous êtes identifié <br />'
        msgMeteo = 'Température :'+str(BMP.temperature)+ '°C <br />'
        msgMeteo = msgMeteo + 'Pression atmosphérique : '+ str(BMP.pression)+' hPa'
    else :
        msgAffiche = 'Connexion refusée - Id ou PassWord incorrect(s) -<br />'
        msgMeteo = "*** Vous n'avez pas accès aux données ***"
    content   = """\
    <!DOCTYPE html>
    <html lang=fr>
        <head>
            <meta charset="UTF-8" />
            <title>TEST méthode POST</title>
        </head>
        <body>
        <div style="text-align:center;color:#4477AA">
            <h3> Identification pour connexion au serveur </h3>
            <h4>ESP32 - SoproLab</h4>
        </div>
        <h5>=== TEST méthode POST ===</h5>
        <div style="background-color:#CCDDEE"><strong>
            Login = %s<br />
            %s<br />
            %s<br /></strong>
        </div>
        </body>
    </html>
    """ % ( MicroWebSrv.HTMLEscape(logId),
            msgAffiche,
            msgMeteo)
#            MicroWebSrv.HTMLEscape(passwrd),
    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )
    if LCD_ok :
        sleep(2)
        if passwrd=='NSI':
            LCD.afficher(0,1, "== Loging OK ==")
        else:
            LCD.afficher(0,1, "= Loging ERROR =")
        sleep(2)
        LCD.backlight_off()
                     
# ----------------------------------------------------------------------------  GET

@MicroWebSrv.route('/formGET')
def _httpHandlerFormGET(httpClient, httpResponse) :
    # stockage de la page web dans une variable texte
    print("########## HTTP - Demande Connexion Client ########## GET")
    msg = httpClient.GetRequestHeaders()
    print(msg)
    print("=============================")
    content = """\
    <!DOCTYPE html>
    <html lang=fr>
        <head>
            <meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h4>TEST méthode : GET</h4>
            IP address du Client = %s <br />
            <h5>Merci de vous identifier :</h5>
            <form action="/test" method="GET" accept-charset="ISO-8859-1">
                Login : <input type="text" name="logId"><br />
                Password : <input type="password" name="passwrd"><br />
                <input type="submit" value="VALIDER">
            </form>
        </body>
    </html>
    """ % httpClient.GetIPAddr()
    # Le serveur répond en envoyant la page web 
    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )


@MicroWebSrv.route('/test', 'GET')
def _httpHandlerTestGet(httpClient, httpResponse, args={}) :
    try :
        LCD.backlight_on()
        LCD.afficher( 0, 1, "form method GET")
        LCD_ok=True
    except:
        LCD_ok=False

    print("########## HTTP - Retour formulaire Client ########## GET")
    msg = httpClient.GetRequestHeaders()
    print("GetRequestQueryParams ",msg)
    print("======= Données =============")
    args = httpClient.GetRequestQueryParams()
    print("GetRequestQueryParams ",args)
    print("Données récupéréses du formulaire :")
    idOk = False
    passwrdOk = False
    for arg in args.keys():
        print(arg, " : ", args[arg] )
        if arg=='logId' :
            logId = args[arg]
            idOk = True
        if arg=='passwrd':
            passwrd = args[arg]
            if not passwrdOk and passwrd=='NSI':
                passwrdOk = True
    if passwrdOk and idOk :
        msgAffiche = 'Ok '+str(logId)+' vous êtes identifié <br />'
        msgMeteo = 'Température :'+str(BMP.temperature)+ '°C <br />'
        msgMeteo = msgMeteo + 'Pression atmosphérique : '+ str(BMP.pression)+' hPa'
    else :
        msgAffiche = 'Connexion refusée - Id ou PassWord incorrect(s) -<br />'
        msgMeteo = "*** Vous n'avez pas accès aux données ***"
    content   = """\
    <!DOCTYPE html>
    <html lang=fr>
        <head>
            <meta charset="UTF-8" />
            <title>TEST méthode GET</title>
        </head>
        <body>
        <div style="text-align:center;color:#4477AA">
            <h3> Identification pour connexion au serveur </h3>
            <h4>ESP32 - SoproLab</h4>
        </div>
        <h5>=== TEST méthode GET ===</h5>
        <div style="background-color:#EEDDCC"><strong>
            Login = %s<br />
            %s<br />
            %s<br /></strong>
        </div>
        </body>
    </html>
    """ % ( MicroWebSrv.HTMLEscape(logId),
            msgAffiche,
            msgMeteo)

    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )
    if LCD_ok :
        sleep(2)
        if passwrdOk and idOk :
            LCD.afficher(0,1, "== Loging OK ==")
        else:
            LCD.afficher(0,1, "= Loging ERROR =")
        sleep(2)
        LCD.backlight_off()


# ----------------------------------------------------------------------------  led / LCD

@MicroWebSrv.route('/led/<myLed>')             # <IP>/led/R           ->   args['myLed'] = 'V' / 'J' / 'R'
@MicroWebSrv.route('/led/<myLed>/etat/<etat>')   # <IP>/led/R/etat/ON   ->   args['myLed']='R'  args['etat']='ON' / 'OFF'
@MicroWebSrv.route('/led')                     # <IP>/led               ->   args={}
@MicroWebSrv.route('/LCD/<myTexte>')           # <IP>/LCD/Bonjour ->   args=['myTexte']='Bonjour'

def _httpHandlerLedWithArgs(httpClient, httpResponse, args={}) :
    content = """\
    <!DOCTYPE html>
    <html lang=fr>
        <head>
            <meta charset="UTF-8" />
            <title>Etat des LED V/J/R</title>
        </head>
        <body>
    """
    content += "<h1>Contr&ocirc;le des LED par passage d'arguments : {}</h1>"\
        .format(len(args))
    print("Arguments : ",args)
    if 'myLed' in args :
        led_ctrl = "{}".format(args['myLed']) # V ou J ou R
        print("led_ctrl :", led_ctrl)
        content += "<p>led = "+led_ctrl+"</p>"

    if 'myTexte' in args :
        LCD_ctrl = "{}".format(args['myTexte']) # Texte à afficher
        print("LCD_ctrl :", LCD_ctrl)
        content += "<p>Texte pour l'écran LCD = "+LCD_ctrl+"</p>"
        try :
            LCD.afficher(0,1,LCD_ctrl)
        except :
            print("\nAffichage sur l'écran LCD impossible !!!\n")
    
    if 'etat' in args :
        action = "{}".format(args['etat']) # ON ou OFF
        content += "<p>etat = "+action+"</p>"
        if action=="ON":
            if led_ctrl=='V':
                LED_v.on()
            elif led_ctrl=='J':
                LED_j.on()
            elif led_ctrl=='R':
                LED_r.on()
        elif action=="OFF":
            if led_ctrl=="V":
                LED_v.off()
            elif led_ctrl=="J":
                LED_j.off()
            elif led_ctrl=="R":
                LED_r.off()

    content += """
        </body>
    </html>
    """
    httpResponse.WriteResponseOk( headers        = None,
                                  contentType    = "text/html",
                                  contentCharset = "UTF-8",
                                  content        = content )

# ----------------------------------------------------------------------------

def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback     = _closedCallback

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
    print("WS CLOSED")

# ----------------------------------------------------------------------------
# routeHandlers = [ ( "/test",  "GET",  _httpHandlerTestGet ),
#     ( "/test",  "POST", _httpHandlerTestPost ) ]


srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded       = False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
srv.Start()