"""
Méthode de codage à éviter :
A corriger : 
- contrôler la valeur entrée avec des assertions et des try/except
- expliquer le principe retenu pour la répartition des 'X'

-> Voir la version [ Pyramides_d_etoiles_V2.py ]

"""
n = int(input("Combien de lignes faut-il tracer ?"))

for i in range (n) : 
    print((n-i)*' '+'X', end='') # tracer la première 'diagonale'
    if not i : # Tracer la première ligne horizontale      
        print(5*' '+ (n-1)*'X ', end='') 
    elif i < n-1 : # tracer la 2eme diagonale, les espaces, la troisième diagonale
        print((2*i-1)*' '+'X'+5*' '+'X'+(2*(n-i)-3)*' ', end='')
    else : # Tracer la dernière ligne
        print(i*' X'+5*' ', end='') 
    print("*") # tracer la dernière diagonale
