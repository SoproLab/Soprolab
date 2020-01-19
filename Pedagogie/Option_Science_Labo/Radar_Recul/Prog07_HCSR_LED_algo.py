# importer la configuration des broches
# importer la fonction d'attente en millisecondes
# importer la bibliothèque pour gérer le capteur de distance à ultrasons

# paramétrer les broches reliées aux trois LED verte, jaune et rouge
# paraméter la broche reliée au bouton poussoir

# Tant que le bouton poussoir n'a pas été enfoncé

    # mesurer la distance
    
    # Si la distance est supérieure à 1000 mm alors
        # Allumer la LED verte et éteindre les autres LED
    # sinon, si la distance est supérieure à 500mm alors
        # Allumer les LED verte et jaune et eteindre la LED rouge
    # Sinon
        # Allumer les trois LED
    # attendre 200 ms