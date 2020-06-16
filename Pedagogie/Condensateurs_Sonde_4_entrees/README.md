# Mesure de tension avec un ADS1015
## Convertisseur analogique / numérique 
<strong> - 4 entrées soit indépendantes, soit couplées deux à deux pour de la mesure différentielle
<br /> - Echantillonnage avec fréquence paramétrable de 8 à 860 échantillons par seconde
<br /> - Gain variable programmable en fonction de Umax de 0,256V à 6,144V
<br /> - Convertion sur 12 bits : [ -2018 ; +2048 ]</strong>

Application à la mesure de tension lors de la charge ou la décharge d'un condensateur.

## Mise en évidence du régime variable lors de la charge ou décharge du condensateur à travers une résistance.

Utilisation de la carte SoproLab basée sur un microcontrôleur ESP32 programmable en Python (Cf micropython.org).

Utilisation d'un ADS1015 pour effectuer les mesures.

## Deux versions de code 

### ESP32_ADS1015.py
Version avec déclaration de variables et paramétrage dans le fichier code.
Cette version peut paraître complexe pour un novice en Python ( élèves )

### ESP32_ADS1015_V2.py
Toute la partie déclaration de variables / paramétrage est déportée dans une bibliothèque : Capteur_ADS1015.py
Le code est nettement simplifié.
L'élève peut alors focaliser sont attention sur la partie [ effectuer / exploiter des mesures ].
 <br />
 <br />
 *Valeurs numériques en ordonnées comprises entre 0 et 2048 -> [ 0; 3,3V ]*
 <br />*Abscisse : le temps en ms*
 <br />*Condensateurs : 1µF - 2,2 µF - 3,3 µF - 4,7 µF chacun en série avec une résistance de 100 kΩ*
 <br />*On obtient une valeur expérimentale de RC = 0,099s pour une valeur théorique de 0,1s (avec 100kΩ - 1µF)*
![Courbe de charge de 4 condensateurs](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/Condensateurs_Sonde_4_entrees/4_condensateurs.png)