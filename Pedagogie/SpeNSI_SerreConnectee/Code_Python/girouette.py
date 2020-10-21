"""
Girouette numérique
Composée de 8 capteurs à effet Hall 49E reliés à des LM339 (quadruple comparateurs
de tension) dont les sorties sont reliées à un PCF8574 -> 8 In/Out sur bus i2c.

"""
from machine import I2C, Pin
from time import sleep
import pcf8574

class Girouette ( ) :
    """
    La classe Girouette reçoit comme argument une instance de classe bus i2c.
    Ce bus i2c permet de communiquer avec le PCF8574 lequel permet d'obtenir
    une "image" des capteurs de position de la girouette.   
    """
    __pt_cardinal = { 0:"Indéterminée", 1:"Nord", 2:"Nord-Ouest", 4:"Est",8:"Nord-Est",
                 16:"Sud-Est", 32:"Sud", 64:"Sud-Ouest", 128:"Ouest" }
    def __init__ ( self, i2c ):
        self.__bus = i2c
        self.__sensor = pcf8574.PCF8574(self.__bus, 0x20) # 8 In / Out via bus i2c
        self.__valeur = 0
        self.__position = [0 for _ in range(8)]
        self.position()
    # ================================================== position
    def position ( self )->tuple :
        """ Retourne un tuple : valeur et décomposition binaire d'un octet """
        lecture_pcf = self.__sensor.port # Lecture du pcf8574
        for i in range(8): # Comparaison des 8 entrées du pcf8574
            if not (1<<i & lecture_pcf) : # INVERSION : bit à 0 lorsque l'aimant est devant
                self.__position[7-i]=1
                self.__valeur = 1<<i
            else :
                self.__position[7-i]=0
        return self.__valeur, self.__position
    # ================================================= cardinal
    @property
    def pt_cardinal ( self )-> str :
        """ retourne la direction cardinale ou ordinale """
        return self.__pt_cardinal[self.__valeur]
# ============================================================== main -> test
if __name__=="__main__":
    i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000) # Port I2C
    memo_position = 0
    ma_girouette = Girouette ( i2c )
    while True:
        valeur_position, position = ma_girouette.position()
        if memo_position != valeur_position and valeur_position :
            print(" {:10s} ".format(ma_girouette.pt_cardinal), end='')
            print(" {:3d} ".format( valeur_position ), end='')
            print("->", position)
            memo_position = valeur_position    
        sleep(0.5)
