"""
Niveau : Terminale NSI
Objectifs :
- développer une méthode d'analyse et de réflexion progressive avant le codage
- gérer les éventuelles erreurs de saisie de la part de l'utilisateur
-> assertion -> try/except
- utiliser des arguments passés en ligne de commande si lexécution se fait dans un shell

Source d'informations sur la gestion des erreurs :
https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/231688-gerez-les-exceptions

L'objectif est d'afficher deux pyramides d'étoiles inversées l'une par rapport à l'autre.
Le nombre de lignes [n] qui constituent les pyramides peut être passé en argument en ligne
de commande dans un shell : [> python Pyramides_d_etoiles n].

exemple pour n=7             i   esp0    X.  esp1   X  '.....'  X.  esp2  X
esp0..X.....X.X.X.X.X.X.X   ...    6    ...  ...    X           6   ...   X
.....X.X     X..esp 2..X     0     5     1    0     X           1    8    X
....X...X     X.......X      1     4     1    2     X           1    6    X
...X.....X     X.....X       2     3     1    4     X           1    4    X
..X.......X     X...X        3     2     1    6     X           1    2    X
.X..esp 1..X     X.X         4     1     1    8     X           1    0    X
X.X.X.X.X.X.X     X         ...   ...    6   ...    X          ...  ...   X

On en déduit que :

Il sera plus simple de traiter à part la première et la dernière ligne

Pour les lignes intermédiaires : pour i allant de 0 à nb_ligne-2 :
-> esp0 = nb_ligne-2-i
-> esp1 = 2*i
-> esp2 = 2*(nb_ligne-3-i)
"""
import sys # Permet de gérer les arguments passés en ligne de commande

# ==================================== Demander le nombre de lignes à l'utilisateur
def nombre_de_ligne ( ) -> int :
    """
    Demander à l'utilisateur le nombre de lignes pour les pyramides
    Entrée : rien
    Sortie : nombre de lignes
    """
    reponse = None
    while reponse == None :
        reponse = input("Entrez le nombre de lignes (1 < n) -> ") # demander le nombre de lignes
        if reponse.isnumeric() : # La réponse est-elle un nombre ?
            nb_ligne = int(reponse) # Effectuer la conversion str -> int
            if nb_ligne < 2 :
                print("Merci de saisir un nombre entier plus grand que 1.")
                reponse=None
        else :
            print("Merci de saisir un nombre entier positif non nul.")
            reponse=None
    return nb_ligne

# =============================================================== tracer_pyramides
def tracer_pyramides ( nb_ligne : int ) :
#    try :
        assert type(nb_ligne)==int and nb_ligne>1,"Attention à n !!!"
        print(' '*(nb_ligne-1)+'X'+'     '+'X '*(nb_ligne-1)+'X')
        for i in range(nb_ligne-2) :
            esp0 = nb_ligne-2-i
            esp1 = 2*i              # esp1 : [ 0 -> 2*(nb_ligne-3) ]
            esp2 = 2*(nb_ligne-3-i) # esp2 : [ 2*(nb_ligne-3) -> 0 ]
            print(' '*esp0+'X '+' '*esp1+'X'+'     '+'X '+' '*esp2+'X')
        print('X '*(nb_ligne-1)+'X'+'     '+'X')
#    except AssertionError :
#        print("\n\ntracer_pyramide ( n ) -> n doit être un entier strictement supérieur à 1")

# ===========================================================================
# ====================================================================== main

if __name__ == "__main__" :
    nb_ligne = 0
    # ======================== s'il y a un argument en ligne de commande
    if len(sys.argv) > 1 :
        # récupérer l'argument de la ligne de commande du shell
        argument_ligne = sys.argv[1]
        if argument_ligne.isnumeric() :
            nb_ligne = int(argument_ligne) # Convertir l'argument en entier           
    if nb_ligne < 2 : # Si l'argument n'est pas exploitable, demander à l'utilisateur
        nb_ligne = nombre_de_ligne ( )
                
    # ============================================= tracer les pyramides
    tracer_pyramides ( nb_ligne )
