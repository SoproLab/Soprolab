"""
JChouteau - Version 0 - Sept 2020
Terminale NSI - Lycée Bourg Chevreau Ste Anne - Segre-en-Anjou-Bleu

-> Exercice 1 de la feuille d'exercices de début d'année
Objectif : Demander une série de notes à l'utilisateur pour :
- calculer la moyenne,
- afficher la note la plus petite,
- afficher la note la plus haute.

A faire :
Demander le nombte de notes à saisir à l'utilisateur

Extension possible :
-> Lire un fichier texte qui contient la liste des élèves (fichier csv),
-> En déduire le nombre de notes à saisir,
-> Afficher un graphique avec la répartition des notes
-> Dans le fichier [notes.csv], ajouter les notes saisie à la suite pour chaque élève

Aborder les moyens d'anticiper les erreurs de saisie ou d'utilisation d'une fonction
-> assertion
-> try / except
-> raise
-> Prévoir les valeurs qui permettront de tester la correction de l'algorithme
Rappel : correction signifie que :
    - l'objectif est atteint, il correspond au cahier des charges,
    - les tests de stabilité sont positifs ( pas de plantage aux tests )
    - le code se termine correctement.
"""
import sys # permet de récupérer les arguments en ligne de commande depuis le shell

# ====================================================================== is_float
def isfloat( note:str ) -> tuple :
    """
    Cette fonction a pour objectif de renseigner si la chaîne de caractères peut ou non
    être convertie en type [ float ].
    Entrée -> "note" : une chaîne de caractères qui correspond à la valeur à convertir
    Sortie -> tuple : ( True, valeur en float après conversion )
                      ( False, 0 ) si la conversion est impossible
    exemple :
    si note = "-23.345" alors
        signe = -1
        split('.') découpe la chaîne de caratères en deux :
        -> partie_entier = '23'
        -> partie_deci = '345'
            -> div_10 = 3 car il faudra diviser ensuite 345 par 1000
        il faudra ensuite calculer la conversion et adapter le type
        si partie_deci est nulle alors
            nombre = int(signe * partie_entier)
        sinon
            nombre = float(signe * partie_entier + partie_deci / 10**div_10)
    
    Note : On considère ici que le développement est terminé.
    Les [ assert ] ont été remplacés par des [ raise ] pour lever des
    exceptions qui vont être traités par la suite dans les différents
    [ except ] selon le type d'erreur rencontré ...
    """
    try :
        # tester si note est bien de type [ str ]
        if type(note)!=str :
            raise TypeError("isfloat( note ) : note doit être de type str")
        
        # mémoriser si le nombre est négatif et retirer le signe - du nombre 
        # La méthode str.isdigit() ne gère pas le le symbole '-'
        signe = -1 if note[0]=='-' else 1 
        note = note.replace('-','')
        
        # séparateur décimal : si une virgule est présente, la remplacer par '.'
        note = note.replace(',', '.')
        
        # récupérer la partie entière et la partie décimale au format str
        if '.' in note :
            partie_entier, partie_deci = note.split('.')
        else :
            partie_entier = note[:]
            partie_deci=''
            
        if not len(partie_entier) : # note=".xxxx" => '', 'xxxx'
            partie_entier = '0' 
        
        if not partie_entier.isnumeric() :
            raise ValueError("La partie entière du nombre contient une erreur de saisie !")
        partie_entier = int(partie_entier) # transtypage [ str ] en [ int ]
        
        if len(partie_deci) : # partie décimale non nulle
            if not partie_deci.isnumeric() :
                raise ValueError("La partie décimale du nombre contient une erreur de saisie !")
            div_10 = len(partie_deci) # prévoir le décalage de la partie décimale
            partie_deci = int(partie_deci) # transtypage en [ int ]

            # calcul du float pour le retour
            nombre = float(signe * partie_entier + partie_deci/(10**div_10))
        else :
            # calcul de l'int pour le retour
            nombre = int(signe * partie_entier)
        return True, nombre
    except TypeError :
        print("La fonction isfloat() ne peut pas convertir [", note, "]")
        return False, -1   # erreur type -1     
    except ValueError :
        print("La fonction isfloat() ne peut pas convertir [", note, "].")
        print("Veuillez corriger la saisie du 'nombre' passé en argument.")
        return False, -2   # erreur type -2

# ================================================== Demander une note à l'utilisateur (type float)
"""

"""
def demander_x ( mini:float, maxi:float, question:str ) -> tuple :
    """
    Demander à l'utilisateur un nombre compris entre mini et maxi inclus. Dans le cas d'une
    erreur de saisie, l'utilisateur est informé sur la nature de l'erreur.
    Entrée : la valeur maximum, le texte pour la question
    Sortie : le nombre saisi par l'utilisateur
    Objectif : gérer les erreurs par raise et try / except
    """
    try :
        if type(mini) != int and type(mini) != float : # Provoque un message d'erreur pour l'argument [ mini ]
            raise TypeError("==== Demander_x ( mini, maxi, question ) == [ mini ]") 
        if type(maxi) != int and type(maxi) != float : # Provoque un message d'erreur pour l'argument [ maxi ]
            raise TypeError("==== Demander_x ( mini, maxi, question ) == [ maxi ]")
        if mini >= maxi :
            raise ValueError("==== Demander_x ( mini, maxi, question ) ====")
        if type(question) != str : # Provoque un message d'erreur pour l'argument [ question ]
            raise TypeError("==== Demander_x ( mini, maxi, question ) == [ question ]")  
        test = False # Tant que test == None -> saisie incorrecte
        while test == False :
            reponse = input( question ) # demander une note
            
            test, note = isfloat( reponse ) # Tester si la reponse est un nombre décimal
                                         
            if test and mini <= note <= maxi : # Si note peut être converti en float ? Séparateur '.' ou ',' acceptés
                return True, note
            else : # La réponse ne peut pas être convertie en nombre
                print("\n---- Merci de saisir une valeur comprise entre,", mini," et ", maxi, ". ----\n")
                test = False
    except TypeError :
        print('=== demander_x (mini, maxi, question) ===')
        print('\t-> les arguments [ mini ] et [ maxi ] doivent être de type [ float ] ou [ int ] !')
        print('\t-> question doit être "Le texte de la question ?"')
        return False, -1
    except ValueError :
        print("-> Erreur : l'argument [ mini ] doit être inférieur à [ maxi ] !")
        return False, -2


# ===========================================================================
# ====================================================================== main
if __name__ == "__main__" :
    try :
        nb_note = 0
        test = False
        # ======================== s'il y a un argument en ligne de commande
        if len(sys.argv) > 1 :
            # récupérer l'argument de la ligne de commande du shell
            argument_ligne = sys.argv[1]
            if argument_ligne.isnumeric() :
                nb_note = int(argument_ligne) # Convertir l'argument en entier
                test = True
            else :
                raise TypeError()
            if nb_note < 2 or not test:
                raise ValueError()

        # Si l'argument n'est pas exploitable, demander à l'utilisateur
        test, nb_note = demander_x (0, 100, "Combien de notes à saisir ? (maxi 100) ->  ")
        if type(nb_note) != int or nb_note < 2:
            raise ValueError()
        i=0
        notes=[] # aucune note au départ
        while i < nb_note:
            question = "Entrez la note n°"+str(i+1)+" -> "
            
            test, note = demander_x( 0, 20, question )
            
            if test :
                notes.append(note) # mémoriser la note
                print(note) # affichage de la note pour vérification
                i = i+1 # note suivante
        print("Note minimale : {:>5.02f}".format(min(notes)) )
        print("Note maximale : {:>5.02f}".format(max(notes)) )
        moyenne = 0
        for i in range(len(notes)):
            moyenne = moyenne + notes[i]
        moyenne = moyenne / nb_note
        print("Moyenne :  {:>10.02f}".format(moyenne) )
    except ValueError :
        print("\tErreur de valeur pour l'argument ...")
        print("---- Merci de saisir une valeur entière supérieure à 1 ----\n")
    except TypeError :
        print("\tErreur de typage pour l'argument ...")
        print("---- L'argument doit être une valeur entière supérieure à 1 ----\n")
        
