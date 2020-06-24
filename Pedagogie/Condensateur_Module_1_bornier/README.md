# Mesure de tension sur une entrée analogique / numérique

Application à la mesure de tension lors de la charge ou la décharge d'un condensateur.

## Mise en évidence du régime variable lors de la charge ou décharge du condensateur à travers une résistance.

Utilisation de la carte SoproLab basée sur un microcontrôleur ESP32 programmable en Python (Cf micropython.org).

Cette version du code n'utilise aucune bibliothèque préprogrammée !

Il est donc nécessaire de faire la déclaration des broches en mode analogique
 <br />
 <br />
 La conversion Mesure / Tension est faite dans LibreOffice lors du traitement des données sachant que le maximum ( 4095) correspond à une tension de 3,3V.
 <br /> Ici j'utilise un condensateur 4,7 µF et une résistance de 100 kΩ.
 <br /> Le temps est indiqué en millisecondes.
 
<br /> ![Courbe de charge d'un condensateur](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/Condensateur_Module_1_bornier/Charge_condensateur.png)

<br /> ![Module de mesure avec bornier](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/Condensateur_Module_1_bornier/Module_Condensateur_1.jpg)

<br /> Etant donné que l'afficheur n'est plus en place, pour simplifier la synchronisation entre la carte SoproLab et Thonny, il peut être nécessaire de meetre à jour la bibliothèque menu.py dispo,nible dans le dossier <a href="https://github.com/SoproLab/Soprolab/tree/master/Mise_a_jour"><b>mise à jour</b></a>.
