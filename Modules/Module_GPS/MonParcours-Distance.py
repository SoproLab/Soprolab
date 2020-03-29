import folium # Bibliothèque pour créer un fond de carte
import pandas # bibliothèque pour lire un fichier de données
from math import sqrt, sin, cos, acos, pi

def distance ( lat1, lon1, lat2, lon2 ):
    """ Correction orthodromique de la distance entre deux points à la surface de la Terre
    Entrée : lat1, lon1, lat2, lon2
    Sortie : distance parcourue en km entre les deux points (lat1, lon1) et (lat2, long2)
    """
    rlat1 = pi*lat1/180 # conversion des angles degré -> radian
    rlat2 = pi*lat2/180
    rlon1 = pi*lon1/180
    rlon2 = pi*lon2/180
    
    theta = lon1-lon2;
    rtheta = pi*theta/180
    
    dist = sin(rlat1) * sin(rlat2) + cos(rlat1) * cos(rlat2) * cos(rtheta);
    dist = acos(dist);
    dist = dist * 180/pi;
    dist = dist * 60 * 1.1515;
    dist = dist * 1.609344
    return dist

# ==================================================================== Programme

# Lire le fichier de données et placer les positions dans une liste :
MesPositions = pandas.read_csv("GROUPE1.csv")   # Lire les coordonnées GPS

# Calculer la moyenne des latitude et longitude pour centrer la carte
lat_moy  = MesPositions['Latitude'].mean()
long_moy = MesPositions['Longitude'].mean()

# Créer la carte intitulée MonParcours
MonParcours=folium.Map(location=[ lat_moy, long_moy], zoom_start=19, tiles='OpenStreetMap' )

# Pour chaque enregistrement GPS, placer un marqueur
for num, gps in MesPositions.iterrows():
    folium.Marker(location=[gps[1],gps[2]],popup=gps[0]).add_to(MonParcours)
    
# Enregistrer la carte au format html pour l'ouvrir avec FireFox par exemple
MonParcours.save(outfile='GROUPE1.html')

# Calculer la distance parcourue
distance_totale=0
for num, gps in MesPositions.iterrows():
    lat = gps[1]
    lon = gps[2]
    if num :
        d = distance ( lat0, lon0, lat, lon )
        distance_totale = distance_totale + d
    lat0 = lat
    lon0 = lon
print("Distance parcourue : {:3.3f} km".format(distance_totale))