"""
=====
Si on veut provoquer une situation d'interblocage, il faut décommenter les lignes 151 et 152
=====

Principe d'utilisation d'un registre d'ordonnancement des tâches dans un processus 
pour exécuter plusieurs processus en même temps, les uns après les autres au cours d'un même cycle

Ce code permet de prendre en charge deux processus "simultanés" (temps partagé) :
    - séquence ouverture puis fermeture d'un toit de maquette de serre
    - séquence de chronométrage (métronome 5s)
    
La gestion de la motorisation n'est pas implémentée, juste
les capteurs de fin de course en ouverture et fermeture.

La routine de gestion des processus prend en charge trois dictionnaires :
    process = {} # Liste des processus enregistrés (clé) : activé ou non (value)
    ressources = {} # Liste des ressources disponibles (clé) : utilisée ou non par un process (value)
    attente = {} # Liste des process suspendus (clé) : [ressources attendues] (value)
    Elle alloue de même un espace mémoire utilisable à chaque cycle
    
jacques@j-chouteau.org
Github : soprolab
"""

from machine import Pin
from time import sleep, ticks_ms

fdc_close = Pin (17, Pin.IN ) # Broches où sont connectés les interrupteurs de fin-de-course
fdc_open = Pin (16, Pin.IN )

capteurs = 0 # Registre d'état des capteurs
capteurs_mem = 0 # Etat des capteurs au cycle précédent
capteurs_chg = 0 # Indicateur de changement d'état


sequence_toit_progress = 0 # progression dans les étapes du processus

# ============================================ mise_a_jour_capteurs
# ============================================
def mise_a_jour_capteurs ( ):
    """
    Cette fonction met à jour les registres qui représentent l'état des capteurs
    Elle permet de plus d'indiquer si un changement d'état a eu lieu (capteurs_chg)
    par rapport au cycle précédent.
    bit 0 -> Capteur fin de course en fermeture
    bit 1 -> Capteur fin de course en ouverture 
    """
    global capteurs
    global capteurs_mem
    global capteurs_chg
    capteurs = (capteurs & 0xFE) | fdc_close.value ( ) # Màj du bit d’index 0
    capteurs = (capteurs & 0xFD) | ( fdc_open.value ( )  << 1 ) # Màj du bit d’index 1
    capteurs_chg = capteurs ^ capteurs_mem # Indicatr de chgmnt d’état
    capteurs_mem = capteurs # Mémoriser l’état pour la proch. boucle
    if capteurs_chg :
        sleep ( 0.3 )  # tempo d’anti-rebond pour les interrupteurs
            
# ========================================================================================     
# ============================================ class tache : embryon de noyau "multitâches"
# ======================================================================================== 
class tache ( ):
    process = {} # Liste des process (clé) : activé ou non (value)
    ressources = { 'Moteur':None, 'Timer':None } # Liste des ressources
    attente = {} # Dict des ressources (clé) : attendues par des [process] (values)
    
    def __init__ (self, nom, fonction, mem:int=0 ):
        tache.process[self] = False # tache non active
        self.nom = nom
        self.etape = None
        self.fonction = fonction # fonction d'exécution du processus
        self.memoire = [ 0 for _ in range(mem) ] # création espace mémoire

    def activer ( self ): # =====================================
        """
        Indiquer que la tâche est active, donc qu'elle doit devenir un processus
        """
        if self.etape == None : # La tâche n'a pas été suspendue auparavant -> commencer à 0
            self.etape = 0
        tache.process[self] = True
        print("----- Process : ", self.nom, " activé ----->")

    def suspendre ( self, ress ): # =====================================
        """
        Mettre un processus en attente si la ressource demandée n'est pas disponible
        """
        print("..... Process : ", self.nom, " suspendu -> en attente .....")
        if ress in tache.attente.keys() :
            tache.attente[ress].append(self) # ajouter le process à la file d'attente
        else :
            tache.attente[ress]=[self] # créer une fille d'attente et y placer le process
        tache.process[self] = False

    def reserver ( self, ress ) : # ===================
        """
        Si la ressource nécessaire est disponible alors la réserver
        Sinon, mettre le processus en attente
        """
        # print("Demande de réservation : ",self.nom," ->", ress)
        if not ress in tache.ressources.keys() : # La ressource n'existe pas
            print("### Ressource NON REPERTORIEE ! ###")
            return None

        if tache.ressources[ress] == self : # La ressource est déjà attribuée à ce process
            return 1
        if tache.ressources[ress] == None : # La ressource est disponible
            tache.ressources[ress] = self # ressource réservée
            return 1
        self.suspendre(ress) # Ressource non disponilbe -> Mettre la tâche en attente
        return None
        
    def liberer ( self, ress ) :  # =====================================
        """ Libérer une ressource devenue inutile """
        if tache.ressources[ress] == self : # Si la ressource était attribuée au process
            tache.ressources[ress] = None # libérer la ressource
            self.mise_a_jour( ress )
        
    def mise_a_jour ( self, ress ): # =====================================
        """
        Vérifier si une tâche peut être réactivée (ressource devenue disponible)
        """
        if ress in tache.attente.keys() : # Un processa attendait la ressource
            tache.attente[ress][0].reserver(ress) # Attribuer la ressource au process en attente
            tache.attente[ress][0].activer() # Activer le process
            tache.attente[ress].pop(0) # retirer le process de la liste des process en attente de la ressoource
            if tache.attente[ress] == [] :
                tache.attente.pop(ress) # retirer la ressource si elle n'est plus attendue

    def desactiver ( self ): # =====================================
        """ Libérer les ressources utilisées """
        self.etape = None # Si la tâche est réactiver plus tard -> recommencer à l'étape 0 lors de l'activation
        tache.process[self] = False
        for une_ress in tache.ressources.keys( ): # Libérer les ressources attribuées au process
            if tache.ressources[une_ress] == self :
                tache.ressources[une_ress] = None
        print("##### Désactivation du process : ",self.nom," #####")

    def executer ( self ): # =====================================
        """ Effectuer un cycle dans une tache """
        if tache.process[self] == True:
            self.fonction ( self )
            
# ================================================================ FONCTION de gestion du
# ================================================================ processus de métronome
def sequence_metronome_execute ( process ) :
    t0 = process.memoire[0] # Charger la mémoire allouée dans les variables de travail
    t1 = process.memoire[1]
    cptr = process.memoire[2]

    if process.etape == 3 : # 15s au total -> fin du process
#        if process.reserver('Moteur') :
#            process.liberer('Moteur')
            process.liberer ('Timer')
            process.desactiver()
            process.etape = None

    if process.etape == 2 : # Afficher le métronome retour étape 1
        print("\n\t\tMétronome => ", cptr, "s")
        t0 = t1
        cptr += 1
        if cptr == 5 :
            process.etape = 3
        else :
            process.etape = 1

    if process.etape == 1 : # 1s s'est écoulée, passer à l'étape 2
        t1 = ticks_ms()
        if t1 >= t0 + 1000:
            process.etape = 2

    if process.etape == 0 : # Initialisation du process métronome
        if process.reserver('Timer'):
            t0 = ticks_ms()
            cptr = 0
            process.etape = 1
        
    process.memoire[0] = t0 # Stocker les variables de travail dans la mémoire allouée
    process.memoire[1] = t1
    process.memoire[2] = cptr


# ============================================================== FONCTION de gestion de la
# ============================================================== sequence_toit
def sequence_toit_execute ( process ):

    if process.etape == 4 : # première étape le toit est-il fermé
        if capteurs_chg & 1 and capteurs_mem & 1 :
            print("-> Toit fermé")
            # Le code est sensé ici arrêter la rotation du moteur en fermeture
            process.liberer('Moteur')
            process.desactiver()
            process.etape = None 

    if process.etape == 3 : # activer l'ouverture du toit
        print("\nFERMETURE -> MOTEUR ON (sens horaire)")
        # Le code est sensé ici mettre le moteur en marche pour FERMER le toit de la mini_serre
        process.etape = 4 # passer à l'étape 4

    if process.etape == 2 : # activer l'ouverture du toit
        if capteurs_chg & 2 and capteurs_mem & 2 :
            print("-> Toit ouvert")
            # Le code est sensé ici arrêter la rotation du moteur en ouverture
            process.etape = 3 # passer à l'étape 3
    
    if process.etape == 1 : # activer l'ouverture du toit
        if process.reserver('Moteur') and process.reserver('Timer'):
            print("\nOUVERTURE -> MOTEUR ON (sens antihoraire)")
            # Le code est sensé ici mettre le moteur en marche pour OUVRIR le toit de la mini_serre
            process.etape = 2 # passer à l'étape 2
        
    if process.etape == 0 : # première étape le toit est-il fermé ?
        if capteurs_mem & 1 :
            print("--- Toit fermé ---")
            process.etape = 1 # passer à l'étape 1

# ======================================================================
# ====================================================================== OUVERTURE / FERMETURE TOIT
"""
Déclaration du processus sequence_toit :
    - vérifier que le toit est fermé
    -> ouvrir le toit
    - lorsque le toit est ouvert
    -> fermer le toit
    - lorsque le toit est fermé
    -> fin du processus
Mémoire allouée -> Aucune
Ressource necéssaire -> 'Moteur' et 'Timer' => interblocage
"""
sequence_toit = tache ( "Toit", sequence_toit_execute ) 
if sequence_toit :
    sequence_toit.activer( ) # activation du processus
else :
    print("========= Ouverture / Fermeture -> Non activé =========")

# ======================================================================
# ====================================================================== METRONOME
"""
Déclaration du processus metronome :
    1- relever t0
    2- attendre qu'une seconde se soit écoulée
    3-> afficher un message et étape 2
    4- Si 5s écoulées, fin du processus
Mémoire allouée : 3 int (-> 3 x 4 octets)
Ressource necéssaire -> 'Timer' et 'Moteur' => interblocage
"""
sequence_metronome = tache ( "Metronome", sequence_metronome_execute, mem=3 )
if sequence_metronome :
    sequence_metronome.activer( )
else :
    print("========= Métronome -> Non activé =========")


# ======================================================================
# ====================================================================== BOUCLAGE des cycles
while True:
    
    mise_a_jour_capteurs ( )
    
    for une_tache in tache.process.keys() :
        une_tache.executer ( ) # exécuter une étape pour chaque process activé