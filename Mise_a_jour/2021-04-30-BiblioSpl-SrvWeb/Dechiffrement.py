try :
    from Cle import symboles, cle_chiffrage
    cle_ok = True
except :
    cle_ok = False
    

def dechiffrement ( texte:str )->str:
    dechiffrement = [ '' for _ in range(len(texte)) ]
    for i in range(len(texte)) :
        if texte[i] in symboles :         
            index = symboles.index(texte[i])
            cle_lettre = cle_chiffrage[i%len(cle_chiffrage)]
            cle_val = symboles.index(cle_lettre)
            
            index = index - cle_val
            if index < 0 :
                index += len(symboles)
            dechiffrement[i] = symboles[ index ]
        
        else :
            dechiffrement[i] = texte[i] 
            
    dechiffrement = "".join(dechiffrement)
    return dechiffrement 
