Dans ce dossier, vous pourrez trouver toutes les bibliothèques microPython nécessaires au bon fonctionnement des modules optionnels de la carte SoproLab.

Ces bibliothèques sont programmées sur le principe de la propragammation orientée objet.
Chaque module est donc considéré comme un "objet" (une instance de classe dans le jargon informatique) sur lequel s'appliquent
 les méthodes qui permettent de communiquer avec le module : [ objet.mesure() ] pour effectuer une mesure par exemple.
 
 
 # ========= Module Celerité du son dans l'air :
=> SOPROLAB_celeriteSon.py :
Module pour mesurer la célérité du son dans l'air contenu dans un tuyau PE de 2m.
(tuyau de diamètre 16mm utilisé pour la distribution d'eau dans les habitations)
  - Objets :
      buzzer
      microphone
  - Méthodes : 
      Chrono_µs-on()
      Chronoµs—off()
      buzzer.on ( )
      buzzer.off ( )
      t0 = Chrono_µs—on ( )
      duree = Chrono_µs—off ( ) - t0

=> celerite_son.py
Code microPython pour mesurer la celerite du son dans l'air

 # Autres modules et bibliothèques à venir ....
- Mesure de l'absorption de lumière Rouge/Verte/Bleue
- Mesure de lumière IR / Visilbe / UVA

Plus d infos sur le site : https://j-chouteau.org/index.php/carte-soprolab/
