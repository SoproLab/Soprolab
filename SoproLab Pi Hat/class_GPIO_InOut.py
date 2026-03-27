"""
Essai de création d'une classe rpi pour la déclaration des broches
a faire :
prendre en comppte la propriété __dict__ d'une broche plutôt
que de créer des propriétés supplémentaires
>>> print(bp.__dict__)
    {'_rpi__pin': 5, '_rpi__conf': 'IN', '_rpi__state': 0}
"""
from time import sleep
import RPi.GPIO as io

io.setmode( io.BCM )
io.setwarnings(False)

class rpi ( ) :
    def __init__ ( self, num_pin:int, conf:str ) :
        try :
            assert conf=="IN" or conf=="OUT", 'conf = "IN" ou "OUT"'
            assert type(num_pin)==int, 'num_pin : n° de broche'
            self.__pin = num_pin
            self.__conf = conf
            if conf=="IN" :
                io.setup ( self.__pin, io.IN )
                self.__state = io.input (self.__pin)
            else :
                io.setup ( self.__pin, io.OUT )
                io.output ( self.__pin, 0 )
                self.__state = False
        except :
            print("Syntaxe : broche = rpi ( n°de broche, 'IN' ou 'OUT' )")
    def on ( self ) :
        """
        Permet de mettre une broche "OUT" à l'état 1
        """
        try :
            assert self.__conf == "OUT", 'La brohe est configurée en "OUT"'
            io.output(self.__pin, 1)
            self.__state = True
        except :
            pass
    def off ( self ) :
        """
        Permet de mettre une broche "OUT" à l'état 0
        """
        try :
            assert self.__conf == "OUT", 'La brohe est configurée en "OUT"'
            io.output(self.__pin, 0)
            self.__state = False
        except :
            pass
    def state ( self ) :
        """
        Retourne l'état d'une broche
        """
        if self.__conf == "IN" :            
            self.__state = io.input(self.__pin)
        return self.__state
        

ledv = rpi ( 17, "OUT")
bp = rpi ( 5, "IN")
ledv.on()
while not bp.state() :
    sleep(0.2)
ledv.off()