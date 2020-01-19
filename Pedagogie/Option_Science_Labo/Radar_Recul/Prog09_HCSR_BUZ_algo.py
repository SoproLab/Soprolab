# importer la configuration des broches
# importer la fonction d'attente en microsecondes
# importer la bibliothèque pour gérer le capteur de distance à ultrasons

# paramétrer la broche reliée au buzzer
# paraméter la broche reliée au bouton poussoir

# Par défaut on fixe la période à 2500µs (obstacle au delà de 500mm)

# Tant que le bouton poussoir n'a pas été enfoncé

    # mesurer la distance
    
    # Si la distance est inférieure à 100mm alors
        # produire 400 fois un son de période 470 µs
    # sinon, si la distance est comprise entre 100mm et 200mm alors
        # produire 400 fois un son de période 970 µs
    # sinon, si la distance est comprise entre 200mm et 300mm alors
        # produire 400 fois un son de période 1470 µs
    # sinon, si la distance est comprise entre 300mm et 400mm alors
        # produire 400 fois un son de période 1970 µs
    # sinon, si la distance est comprise entre 400mm et 500mm alors
        # produire 400 fois un son de période 2470 µs
    # Silence de 200 fois la période du son entre deux "beep"
    # Attendre au minimum 10ms entre deux mesures (si d>500 )