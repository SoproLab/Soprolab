import folium
import pandas
from math import sqrt, sin, cos, acos, pi

def distance ( lat1, lat2, lon1, lon2 ):
    """ Correction orthodromique de la distance entre deux points à la surface de la Terre
de latitude et longitude connues.
    Entrée : lat1, lat2, lon1, lon2
    Sortie : distance parcourue en km
    """
    rlat1 = pi*lat1/180 # conversion des angles degré -> radian
    rlat2 = pi*lat2/180
    rlon1 = pi*lon1/180
    rlon2 = pi*lon2/180
    
    theta = lon1-lon2;
    rtheta = pi*theta/180
    
    dist = sin(rlat1) * sin(rlat2) + cos(rlat1) * cos(rlat2) * cos(rtheta); # correction
    dist = acos(dist);
    dist = dist * 180/pi;
    dist = dist * 60 * 1.1515;
 
    dist = dist * 1.609344 # résultat en km
    return dist

fichier=pandas.read_csv("MonParcours.txt") # Lire les coordonnées GPS

MonParcours=folium.Map(location=[ fichier['Latitude'].mean(),
                                  fichier['Longitude'].mean()],
               zoom_start=14,
               tiles='OpenStreetMap' ) # Obtenir un fond de carte centré sur le parcours

for num, gps in fichier.iterrows(): # repérer chaque psition GPS sur la cart par un Marqueur
    folium.Marker(location=[gps[1],gps[2]],popup=gps[0]).add_to(MonParcours)
    
MonParcours.save(outfile='MonParcours.html') # Enregistrer le résulat au format html

# Calculer la distance totale du parcours
distance_totale=0
for num, gps in fichier.iterrows():
    lat = gps[1]
    lon = gps[2]
    if num :
        d = distance ( lat0, lat, lon0, lon ) # distance entre deux positions successives
        distance_totale = distance_totale + d # distance totale
    lat0 = lat # la position actuelle devient la position précédente pour la prochaine itération
    lon0 = lon
print("Distance parcourue : {:3.3f} km".format(distance_totale)) 