def doubler ( n : int ) -> int :
    return n**2

def cuber ( n : int ) -> int :
    return n**3

fonctions = [ doubler, cuber ]

def calculer ( fonction, n : int ) -> int :
    return fonction ( n )

for i in range (len(fonctions)):
    print (calculer ( fonctions[i], 2 ))