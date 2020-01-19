# importer la configuration des broches
# importer la fonction sleep_us() de la bibliothèque [ time ]

# paramétrer la broche reliée au buzzer
# paraméter la broche reliée au bouton poussoir

# calculer la période en microseondes, d'un son de fréquence 440 Hz
# calculer le nombre de périodes pour obtenir une durée de 0,5s

# Faire une boucle infinie
    # lire l'état du bouton poussoir
    # Si le bouton poussoir est enfoncé alors
        # Faire une boucle pour le nombre de périodes nécessaires
            # Mettre la broche du buzzer à 0
            # Attendre une demie-période
            # Mettre la broche du buzzer à 1
            # Attendre une demie période 