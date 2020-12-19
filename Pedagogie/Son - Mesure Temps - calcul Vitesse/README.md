Modification : 19/12/2020 : 
- ajout des fichiers STL pour impression 3D des blocs de fixation du micro et buzzer sur un tuyau PE diametre 16mm

# Déterminer expérimentalement la vitesse de propagation du son dans l'air

## Première partie

Je propose aux élèves une première approche des microcontrôleurs de façon simpliste :
- allumer et éteindre une led

Cela permet de vérifier le bon fonctionnement (logiciel / connexion / ...)<br>
<br>
## Installation du module SON

Ensuite, je leur fais configurer une broche en sortie pour piloter le buzzer et une autre en entrée pour le micro.<br>

### 1ere étape  : temps de réaction

Le buzzer est collé au micro.<br>
On détermine alors delta_t : temps de réaction. Ce temps sera à soustraire par la suite à la mesure du temps de propagation.<br>

### 2eme étape : temps de propagation du son 

Ils mesurent le temps de propagation du son dans l'air d'un tuyau PE diamètre 16mm, longueur 2m. Ils doivent ensuite calculer la vitesse.<br>

## Correction de l'activité

Lors de la correction de l'activité, je leur montre l'utilisation de boucles [ for ] pour effectuer 8 essais consécutifs.<br>
-> notions de variation des mesures --> mesure statistique / calcul de la moyenne ...<br>
<br>
On obtient alors des valeurs proches de 340 m/s<br>
<br>
Bonne lecture ...<br>
<br>
Jacques Chouteau
<br>
*Si vous souhaitez les fichiers STL pour imprimer vous même les adaptateurs micro/buzzer au tuyau de PE 16mm, il suffit de m'envoyer un message via le site j-chouteau.org* ...
