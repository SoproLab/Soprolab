Trame="$GPGGA,122337.345,4852.4266,N,0217.7023,E,1,04,2.7,50.0,M, , , , *"
Champs=Trame.split(",")
print("Type de trame=",Champs[0])
print("Heure=",Champs[1])
print("Latitude=",Champs[2])
print("orientation de la latitude=",Champs[3])
print("Longitude=",Champs[4])
print("orientation de la Longitude=",Champs[5])
print("Altitude=",Champs[9],"M")
def degre(x):
    partie_decimale=(x-100*(x//100))/60
    degre=x//100+partie_decimale
    return degre
if Champs[3]=="N":
    print("latitude","+",degre(float(Champs[2])))
else:
    print("latitude","-",degre(float(Champs[2])))
if Champs[5]=="E":
    print("longitude","+",degre(float(Champs[4])))
else:
    print("longitude","-",degre(float(Champs[4])))