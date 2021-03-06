import folium # Bibliothèque pour créer un fond de carte
import pandas # bibliothèque pour lire un fichier de données

fichier_source = "DATA_GPS_20200417_16h04"

# Lire le fichier de données et placer les positions dans une liste :
MesPositions = pandas.read_csv(fichier_source+".csv")   # Lire les coordonnées GPS

# Calculer la moyenne des latitude et longitude pour centrer la carte
lat_moy  = MesPositions['Latitude'].mean()
long_moy = MesPositions['Longitude'].mean()

# Créer la carte intitulée MonParcours
MonParcours=folium.Map(location=[ lat_moy, long_moy], zoom_start=28, tiles='OpenStreetMap' )

# Pour chaque enregistrement GPS, placer un marqueur
for num, gps in MesPositions.iterrows():
    folium.Marker(location=[gps[1],gps[2]],popup=gps[3]).add_to(MonParcours)
    
# Enregistrer la carte au format html pour l'ouvrir avec FireFox par exemple
MonParcours.save(outfile=fichier_source+".html")
