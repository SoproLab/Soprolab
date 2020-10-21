# Mini serre connectée

Toutes mes excuses ici sur le fait qu'il manque des commentaires, qu'une partie des bibliothèques ont été récupérées sur d'autres projets et intégrées rapidement sachant qu'il faudra revenir sur le projet pour rendre la programmation plus "propre".<br />
<br />
En effet, une partie du code est en orienté objet "girouette", une autre est en impératif "LCD1602" avec des bibliothèques imbriquées, des variables globale ... ça ressemeble un peu à une coffre à jouet mal rangé ;) <br />
<br />
- bme280.py -> bibliothèque du capteur de température / pression amtosphérique et humidité relative de l'air ambiant,
- boot.py -> rien à signaler,
- girouette.py -> bibliothèque de gestion de la girouette. La position du disque est déterminée par le capteur 49E activé sur les huit disposés autour de l'axe de la girouette. Ainsi, le pcf8674 voit une de ses entrées passer de 0 à 1. Il transmet l'information sous la forme d'un octet où chaque bit correspond à une position de la girouette,
- lcd_i2c.py -> gestion de l'afficheur LCD 16 caractères - 2 lignes,
- main.py -> rien à signaler, juste une séquence qui permet de charger les bibliothèques en mémoire pour faire des tests
- **MiniSerre.py** lancement de la gestion de la mini serre connectée. **C'est ce fichier que les élèves devront modifier** pour atteindre l'objectif. Le code Python permet d'adapter le code HTML / CSS / JS au regard du cahier des charges fixé. Pour cela on utilise des "fausses balises orphelines" par exemple :  "<" variable_temperature ">" pour intégrer des valeurs de capteurs ou d'état dans le code HTML et ou modifier le Javascript et le css. Ils devront aussi créer un fichier javascript pour rendre la page intéractive au regard de l'état de la trappe de façon dynamique -> ajouter une classe qui permet de cacher un bouton.<br />
- pcf8574.py -> bibliothèque du composant qui récupère l'état des huits capteurs à effet Hall et retransmet cette information sur le bus i2c sous la forme d'un octet<br />
- serre_biblio.py -> Principale bibliothèque de fonctions préprogrammées disponibles. Le fait de les avoir regroupées dans un fichier Python à part permet de simplifier la lecture du code à modifier.<br />
<br />
<strong>Répertoire www</strong><br />
index.html<br />
script.js<br />
style.css<br />