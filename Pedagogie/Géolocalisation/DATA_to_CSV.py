"""
Objectif : générer un fichier CSV à partir d'un fichier de données transmis
par un récepteur GPS ( trames NMEA )

Structure du fichier de données :
    - pour chaque position, on dispose de 10 lignes d'informations
    - La première ligne correspond au Numéro de position
    - les 9 lignes suivantes sont les trames NMEA correspondant à cette position
"""
from math import floor

nbLignesNMEA = 10 # Chaque position est renseignée par 10 trames NMEA
fichier_source = "DATA_GPS_20200417_16h04"

# Ouverture du fichier en mode lecture
MyFile = open ( fichier_source+".txt",'r')
Lignes = MyFile.readlines()  # Déterminer le nombre de lignes dans le fichier
nbPos = len(Lignes) // nbLignesNMEA  # En déduire le nombre de positions

MyCSV = open (fichier_source+".csv",'w', newline='\n' )
MyCSV.write('Heure,Latitude,Longitude,Vitesse\n')

# Pour chaque position
for cptrPos in range(nbPos):

    numPos = ord(Lignes[cptrPos][0]) # Récupérer le numéro d'enregistrement

    # Extraire la ligne qui correspond à la trame $GPRMC (heure,latitude,longitude)
    for numLigne in range ( nbLignesNMEA ):
        if '$GPVTG' in Lignes[cptrPos*nbLignesNMEA+numLigne] :
            maVit = Lignes[cptrPos*nbLignesNMEA+numLigne]
        if '$GPRMC' in Lignes[cptrPos*nbLignesNMEA+numLigne] :
            maPos = Lignes[cptrPos*nbLignesNMEA+numLigne]

    infoVit = maVit.split(',') # Extraire les informations de la trame
    vitPos = floor(float(infoVit[7])) # Vitesse en km/h sans décimal
    vitPosTxt = str(vitPos)    

    infoPos = maPos.split(',') # Extraire les informations de la trame
    # infoPos[0] = '$GPRMC'
    # infoPos[1] = 'hhmmss.00'
    heurePos = int(infoPos[1][0])*10+int(infoPos[1][1])
    heurePos = heurePos + 1 if heurePos < 24 else 0 # Heure UTC -> Paris +1h
    textPos = str(heurePos)+'h'+infoPos[1][2:4]+'min'+infoPos[1][4:6]+'sec'

    # infoPos[2] = 'A' ou 'W'
    # infoPos[3] = 'xxxx.xx' infoPos[4] = 'N' ou 'S' LATITUDE
    latiPosDeg = int( infoPos[3][0:2] ) # Degré
    latiPosMin = float ( infoPos[3][2:]) # Minutes
    latiPosMin = latiPosMin / 60
    latiPos = latiPosDeg + latiPosMin
    if infoPos[4] == 'S':
        latiPos = - latiPos
    latiPosTxt = "{:2.6f}".format(latiPos)

    # infoPos[5] = 'xxxx.xx' infoPos[6] = 'E' ou 'W' LONGITUDE
    longPosDeg = int( infoPos[5][0:2] ) # Degré
    longPosMin = float ( infoPos[5][2:]) # Minutes
    longPosMin = longPosMin / 60
    longPos = longPosDeg + longPosMin
    if infoPos[6] == 'W':
        longPos = - longPos
    longPosTxt = "{:2.6f}".format(longPos)
    
    # enregistrer les informations pour chaque position au format csv
    MyCSV.write(textPos+','+latiPosTxt+','+longPosTxt+','+vitPosTxt+'\n')

MyFile.close()
MyCSV.close()

    