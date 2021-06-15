"""
Note : Hors programme de terminale mais bon à savoir ...

Principe d'héritage de classes
    les classes Garcon / Fille héritent de la classe Humain
Principe de jonction de classes
    la classe Mariage utilise les classes Fille et Garcon -> naissance( )
"""
# ============================================ Humain
class Humain ( ):
    nombre = 0
    def __init__ ( self, nom:str, prenom:str, age:int=0 ):
        self.nom = nom
        self.prenom = prenom
        self.__age = age
        self.parents = None
        Humain.nombre += 1
        self.annoncer ( )
        
    @property # principe d'un assesceur ( getter )
    def age ( self ):
        return self.__age
    
    @age.setter # principe d'un mutateur ( setter )
    def age ( self, value:int ):
        if value < 0 :
            print("\n\t=============== Age : ",value,"-> Il doit y avoir une erreur !\n")
        else :
            self.__age = value
            
    def annoncer ( self ):
        print("\n=== Souhaitons la bienvenue à ",self.prenom)
        print("Il y a maintenant {:d} instance(s) de classe Humain.".format(Humain.nombre))
        
    def anniversaire ( self ): # méthode publique
        self.age += 1
        self.__annoncer ( ) # Appliquer une méthode sur une instance de classe
        
    def __annoncer ( self ): # méthode privée
        print("\n ### *==== Joyeux anniversaire ",self.prenom.upper()," ====* ###")
        
# ============= Humain -> Garcon
class Garcon ( Humain ):
    def __init__ ( self, nom:str, prenom:str, age:int=0  ):
        Humain.__init__ ( self, nom, prenom, age)
        self.gene = 'XY'
# ============= Humain -> Fille        
class Fille ( Humain ):
    def __init__ ( self, nom:str, prenom:str, age:int=0 ):
        Humain.__init__ ( self, nom, prenom, age)
        self.gene = 'XX'
# ============================================ Mariage
class Mariage ( ) :
    def __init__ ( self, conj1:object, conj2:object ):
        self.conjoint1 = conj1
        self.conjoint2 = conj2
        print("\n ====!! VIVE LES MARIÉS !!====")
        
    def naissance ( self, genre:str, prenom:str )->object:
        nom = self.conjoint1.nom + "-" + self.conjoint2.nom
        enfant = Fille( nom, prenom ) if genre=='F' else Garcon( nom, prenom )
        enfant.parents = self.conjoint1, self.conjoint2
        return enfant
        
# ===========================================================================
print("Début. Nombre d'Humain ->", Humain.nombre)

paul = Garcon ( "Dupont", "Paul" )
paul.age = -2
paul.age = 25
print("Paul ->", paul.nom, paul.prenom, paul.age,"an(s) ", paul.gene)

sarah = Fille ( "Durand", "Sarah", 26 )
print("Sarah ->", sarah.nom, sarah.prenom, sarah.age,"an(s) ", sarah.gene)

paul.anniversaire ( )
print("Paul ->", paul.nom, paul.prenom, paul.age, paul.gene)

"""
try :
    paul.__annoncer() # class privée -> erreur d'exécution
except :
    print("\n======= Erreur d'exécution =======")
    print("\tSi le nom d'un attribut ou méthode commence par __ alors il ou elle est privé.e")
    print("\tVous ne pouvez donc pas y accéder directement !\n")
finally :
"""
famille = Mariage ( paul, sarah )
print(famille.conjoint1.prenom," et ", famille.conjoint2.prenom,"ont la joie de vous annoncer leur mariage !")

camille = famille.naissance ( "F", "Camille" )
print("Identité de Camille : ")
print("\t Prenom : ", camille.prenom)
print("\t Nom : ", camille.nom)
print("\t Fille de : ", camille.parents[0].prenom, "et ", camille.parents[1].prenom)
    
