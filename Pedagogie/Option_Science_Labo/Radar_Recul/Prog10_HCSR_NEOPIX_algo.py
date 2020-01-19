# importer la configuration des broches
# importer la fonction d'attente en millisecondes
# importer la bibliothèque pour gérer le capteur de distance à ultrasons
# importer la bibliothèque pour gérer les diodes NEOPIXEL

# paramétrer la broche reliée au buzzer
# paraméter la broche reliée au bouton poussoir

# Configurer la diode NEOPIXEL[0] avec ( 0, 140, 0 )

# Tant que le bouton poussoir n'a pas été enfoncé

    # mesurer la distance
    
    # Si distance est supérieure à 700mm alors
        # éteindre les NEOPIXELS [ 1 à 7 ] incluses
    # sinon, si la distance est supérieure alors 600 mm
        # configurer la NEOPIXEL [ 1 ] et éteindre les autres
    # sinon, si la distance est supérieure alors 500 mm
        # configurer les NEOPIXEL [ 1 & 2 ] et éteindre les autres
    # sinon, si la distance est supérieure alors 500 mm
        # configurer les NEOPIXEL [ 1 à 3 ] et éteindre les autres
    # sinon, si la distance est supérieure alors 500 mm
        # configurer les NEOPIXEL [ 1 à 4 ] et éteindre les autres
    # sinon, si la distance est supérieure alors 500 mm
        # configurer les NEOPIXEL [ 1 à 5 ] et éteindre les autres
    # sinon, si la distance est supérieure alors 500 mm
        # configurer les NEOPIXEL [ 1 à 6 ] et éteindre la dernière [ 7 ]
    # sinon
        # configurer les NEOPIXEL [ 1 à 7 ] 
    # mettre à jour l'état des diodes NEOPIXEL
    
    # Attendre au minimum 10ms entre deux mesures (si 7>500 )
# Eteindre les led NeoPixel