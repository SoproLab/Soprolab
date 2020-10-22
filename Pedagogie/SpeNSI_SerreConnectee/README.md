# Mini serre connectée
## Projet d'activité autour d'une IHM
<strong>Le principal objectif est d'aborder :
- les notions de capteurs ( analogique, numérique, de contact, à distance, ... )
- les notions de transfert et traitement de l'information ( utilisation d'un microcontrôleur, bus de communication i2c, connexion wifi, ... ),
- les notions d'actionneurs piloté via une Interface Homme Machine : I.H.M. ( écran LCD ou navigateur Web )</strong>
<br />
L'évolution d'un projet : de la micro-station météo à la serre connectée muni d'un système aération piloté via une interface Web.<br />

## La micro station météo : Client <-> Serveur
<table><tr><td>
    A l'origine, le projet se voulait simple : un ESP8266-ESP01 équipé d'un capteur DHT11 : quelques euros, pas de soudure : un kit disponible prêt à l'emploi. L'ESP8266 peut faire office de micro serveur web via un socket <i>(en connexion Wifi)</i> programmé en microPython.<br />
    On obtient ainsi la température et l'humidité relative de l'air ambiant, données que l'on peut transmettre en HTML pour être visualisées via un navigateur.<br /></td>
<td>
<img src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/esp01_DHT11.jpg" alt="esp01 et DHT11" align=middle width="260">
    </td></tr></table>

## Un projet de mini-serre

![Schéma d'une mini-serre avec trappe d'aération](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/mini_serre_v2.jpg)
Suite à des échanges dans le cadre d'une formation DU ES-NSI, nous nous sommes orientés vers une situation plus étoffée dans le contexte d'une mini-serre.<br />
Afin de présenter la chaîne de traitement de l'information, il fallait alors partir du capteur et aller jusqu'à l'actionneur en passant par l'IHM.<br />
En guise d'actionneur, le plus simple était d'équiper le toit le la serre d'une trappe d'aération actionnée par un servo moteur ce qui évitait les interfaces de puissance pour piloter un moteur à courant continu.<br />
Même si ce type de motorisation ne nécessite pas forcément de rétrocontrôle pour déterminer la position de la trappe, dans le cas d'un asservissement, il convenait d'équiper le dispositif de deux interrupteurs de fin de course : position ouverte et position fermée.<br />
<br />
Les deux GPIO 0 et 2 <i>(entrée / sortie)</i> disponibles sur l'ESP8266-ESP01 devenaient alors insuffisantes :
- une pour le capteur numérique DHT11,
- une pour pour commander le servo moteur.<br />

Il fallait donc récupérer deux autres ports en soudant deux autres fils de connexion directement sur le microcontrôleur, ce qui n'est pas chose facile avec une puce au format SSOP ! <br />
Une fois le tout installé sur un plaque à trous métallisés il restait à relier le microcontrôleur à l'ordinateur pour la programmation.<br />
<table><tr><td>
Pour cela, nous avons confectionné des cordons de connexion muni d'un convertisseur de type FTDI pour assurer la conversion entre le port de communication USB côté ordinateur et le port série Rx/Tx côté microcontrôleur. <br />
    <br /></td>
    <td><img src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/ftdi.jpg" alt="ftdi adaptation USB - TxTx" align=middle width="300">
    </td></tr></table>
L'IDE de programmation retenu est Thonny. Il confère un environnement confortable et intuitif pour la programmation en microPython. D'autres enseignants font le choix de Mu ou encore VsCode avec les plugin qui permettent d'établir une connexion avec les ESP32 ou ESP8266.<br />
Dans la prochaine version 3.3, il sera possible d'éditer directement dans l'éditeur les fichiers HTML/CSS/JS stockés dans la mémoire flash du microcontrôleur, ce qui facilitera grandement les mises à jour et le développement d'un projet comme celui présenté ici.<br />

## Pourquoi faire simple quand on peut faire plus complet ?

Lors de la réalisation, on a eu quelques soucis de connexion avec le prototype. L'interfaçage avec Windows n'était pas toujours chose facile mais globalement le projet était encourageant et nous arrivions à piloter l'ouverture et la fermeture de la trappe à partir d'un ordinateur ou d'un smartphone.<br />
<br />
### Des soucis de connexion
Cependant les petits soucis multipliés par le nombre de groupes en situation de simulation d'activité élève lors de la formation rendent le projet peut confortable au risque de perdre trop de temps à résoudre les problèmes des uns et des autres.<br />
<table><tr><td>
    <h3> Un dispositif assez limité dans les scénarios pédagogiques </h3>
Compte tenu du fait qu'on ne pouvait pas développer davantage les connexions avec le microcontrôleur, les perspectives d'évolution étaitent très limitées.<br />
Certes, l'utilisation d'un Wemos D1 en lieu et place d'un ESP8266-ESP01 aurait permis une plus grande souplesse.<br />
Mais quitte à changer de microcontrôleur autant prendre son grand frère pour le même budget : l'ESP32.<td>
    <td><img src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/wemos.jpg" width="400" alt="Wemos D1 : esp8266 et capteurs, indicateurs lumineux, ... en sandwitch"></td></tr></table>

### Ouvrir les horizons des possibles
Dans ce contexte, il convient alors de repenser la chaîne de traitement de l'information pour intégrer d'autres types de capteurs ou d'IHM et pourquoi pas produire une maquette qui pourrait alors servir de support pour un groupe d'élèves dans le cadre d'un mini projet et ou projet NSI !<br />

![Photo du prototype de maquette](https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/Diagramme.jpg)

**Capteurs à effet Hall :**
Les capteurs à effet Hall 49E (détection d'un aimant) permettent de déterminer la période de rotation d'un disque et ou la position approximative de celui-ci. Associés à des amplificateurs opérationnels montés en comparateurs (LM339) on peut ainsi réaliser d'une part un anémomètre et d'autre part une boussole.<br />
Ces capteurs permettent ainsi de mettre en pratique les capteurs à distance donc sans interaction physique avec le système contrairement aux interrupteurs de fin de course qui déterminent si la trappe est ouverte ou fermée.<br />
<br />
**-> Anémomètre :**
Il permet d'aborder la mesure de temps : la période de rotation de l'axe afin de déterminer une vitesse de rotation. Il restera à déterminer l'étalonnage de l'anémomètre afin d'en conclure la relation entre vitesse de rotation et vitesse du vent, notion d'étalonnage abordée en spécialité sciences physiques.<br />
<br />
**-> Girouette :**
Un disque muni de huit capteurs 49E permettent de déterminer la position de la girouette selon les quatre directions cardinales et les quatre directions ordinales. Là aussi, il conviendra d'avoir recours à un étalonnage de position notamment en équipant la maquette d'un compas numérique facilement accessible à faible coût. Ce point peut être laissé à la réflexion des élèves sur l'évolution à donner au projet pour le rendre plus fonctionnel ou les précautions d'usage à prévoir ...<br />
<br />
<table>
    <tr>
        <td>
    <strong> *** Liens avec des notions connexes du référentiel :*** </strong>
Le principal intérêt de cette girouette est d'aborder le codage d'une information sur huit bits. En effet, une entrée du pcf8574 passe à 1 lorsque le capteur associé détecte la position de l'aimant devant lui. Le PCF8574 transmet alors l'information au microcontrôleur sous la forme d'un octet où un seul bit est à 1 selon la position de l'axe de la girouette -> 1, 2, 4, 8, 16 ... 128.<br />
On peut aussi aborder ici la transmission d'une information depuis un capteur jusqu'au microntrôleur au regard de contraintes : distance / parasitage / précision / connexions / traitement de l'information / étalonnage / ...). Le bus i2c permet aussi de faire un parallèle avec le transfert d'informations dans le contexte d'une carte mère (bus de données, ...)<br />
<br />
C'est aussi l'occasion d'aborder un outil en Python adapté à ce type de situation : **le dictionnaire**.<br />
Il permet alors d'associer une valeur (clé) à une direction (value) : { 1:Nord, 2:Nord-Est, 4:Est, ...}<br />
    </td>
    <td>Coupe tranversale de la girouette<br />
        <img src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/coupe.jpg" alt="Coupe transversale de la girouette" width="600">
    </td>
   </tr>
</table>
<br />
**Capteur de lumière :** <br />
LDR (Light Dependent Resistor): Pour aborder la conversion analogique numérique, une LDR a été installée sur la maquette. La valeur de la luminosité est convertie sur une échelle de 0 à 4095 puisque le convertisseur analogique numérique de l'ESP32 est codé sur 12 bits.<br />
<br />
**Développer une I.H.M.**<br />
<br />
**Led blanche :** une led blanche permet de simuler l'éclairage de la serre dans le cas d'un ensoleillement insuffisant. Grace à la LDR, on peut ainsi déterminer un seuil en dessous duquel il convient d'allumer la lumière.<br />
<br />
**Interrupteur et bouton poussoir :** un interrupteur à bascule et un bouton poussoir permettent de mettre en place différents scénarios où l'utilisateur peut interagir physiquement pour transmettre une commande.<br />
<br />
**Afficheur à cristaux liquides :** un afficheur LCD 16 caractères sur chacune des deux lignes permet là aussi d'informer l'utilisateur sur les valeurs obtenues lors des mesures de grandeurs telles que la température, la pression ou l'humidité relative ou bien encore l'état du système : trappe ouverte ou fermée, ...<br />
<br />
### Activité elève ###

Dans un premier temps, elle porte sur l'analyse de la chaîne de traitement de l'information depuis le capteur jusqu'à l'actionneur.<br />
On donne une documentation technique sur le capteur de température / pression / humidité : le BME280. A partir de ce document, l'élève doit en extraire les informations pertinentes pour le projet et l'exploitation des données.<br />
<br />
Dans une deuxième temps, on lui demande de mettre en pratique ses connaissances sur le langage HTML/CSS/JS pour modifier l'IHM Web de telle sorte que le bouton OUVRIR ne doit s'afficher que si le toit est fermé et à contrario le bouton FERMER ne doit s'afficher que si le toit est ouvert.<br />
<strong>=== Précision sur le fonctionnement ===</strong>
Nous n'avons pas ici un serveur apache/php/sql ! les données ne sont pas stockées dans une table avant d'être intégrées dans la page Web. Cependant, on peut facilement faire le parallèle avec python dans notre activité et php sur un serveur Web.<br />
Ici, nous avons fait le choix de placer des balises orphelines <variable_temperature>, <variable_pression>, <variable_toit>, ... dans le code HTML et JS pour recevoir ensuite les données en fonctione de l'état du système.<br />
C'est la fonction Web_page (Cf code python) qui remplacera ces balises par les informations adhoc dans la page Web avant d'être transmise au Client.<br />
<br />
Pour les plus "audacieux" l'IHM pourra être complétée avec la sélection d'un mode automatique / manuel auquel cas, il faudra déterminer la température de contrainte pour l'ouverture de la trappe via l'IHM ...<br />
<br />

**La suite ...**
Il reste à développer un circuit imprimé et simplifier la connectique pour rendre cette maquette facilement réalisable par une équipe d'enseignants peu outillés.<br />
L'impression 3D de la structure de la serre n'est plus vraiment un obstacle aujourd'hui étant donné que ces machines se sont beaucoup démocratisées ces dernières années, notamment dans les collèges ...
<br />
<table><tr><td>Visuel du prototype<br />
    <img alt="Photo du prototype de maquette" src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/mini_serre_00.jpg" /></td>
<td>IHM via l'interface Web<br />
    <img alt="IHM serre connectee" src="https://github.com/SoproLab/Soprolab/blob/master/Pedagogie/SpeNSI_SerreConnectee/Code_Python/www/Objectif_1.jpg" /></td></tr></table>
