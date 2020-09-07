n = int(input("Combien de lignes faut-il tracer ?"))
print(n*' '+'* '+4*' '+(n+1)*'* ') # Tracer la première ligne
for i in range (n-1) : # Tracer les lignes dans la boucle
    print((n-1-i)*' '+'*'+(2*i+1)*' '+'*'+5*' '+'* '+2*(n-2-i)*' '+'*')
print((n+1)*'* '+4*' '+'*') # Tracer la dernière ligne
