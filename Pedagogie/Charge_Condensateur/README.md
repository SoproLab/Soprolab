# Mesure de tension avec un ADS1015
## Convertisseur analogique / numérique 
### - 4 entrées soit indépendantes, soit couplées deux à deux pour de la mesure différentielle
### - Echantillonnage avec fréquence paramétrable de 8 à 860 échantillons par seconde
### - Gain variable programmable en fonction de Umax de 0,256V à 6,144V
### - Convertion sur 12 bits : [ -2018 ; +2048 ]

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
 