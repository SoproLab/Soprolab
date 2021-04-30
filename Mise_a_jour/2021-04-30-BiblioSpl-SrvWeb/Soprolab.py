""" Soprolab.py - 2021-04-30
Auteur J. Chouteau 
Version 'simplifiée' de la bibliothèque d'utilisation
de la carte soproLab ESP32.

"""
import sys
from os import chdir
from machine import Pin, ADC, I2C, Timer
from neopixel import NeoPixel
from micropython import const
from ustruct import unpack as unp
from time import sleep_ms, sleep_us, ticks_ms, ticks_us
from math import log
from Lcd import Lcd1602

I2C_BUS = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000 )

Pin_J4_4 = const(0) # Connecteur J4
Pin_J4_3 = const(4)

Pin_NEOPIXEL = const(2) # Ruband 8 LED NeoPixel
Nb_NEOPIXEL = const(8) # Nbre de LED sur le ruban

Pin_LED_V = const(12)
Pin_LED_J = const(13)
Pin_LED_R = const(14)

Pin_J5_5 = const(15)
Pin_J5_RX2 = const(16)
Pin_J5_TX2 = const(17)

Pin_SPI_SCK = const(18)
Pin_SPI_MISO = const(19)
Pin_SPI_SS = const(29)
Pin_SPI_MOSI = const(37)

Pin_I2C_SDA = const(21)
Pin_I2C_SCL = const(22)
Pin_I2C_CMD1 = const(26)
Pin_I2C_CMD2 = const(27)


Pin_CTN = const(32)
Pin_LDR = const(33)
Pin_POT = const(34)
Pin_BP = const(35)
Pin_BUZZ = const(25)
# =========================================================
class Console ( ):
    def __init__ ( self ):
        pass
    def afficher ( self, x, y, texte ):
        print(texte)
    def effacer ( self ):
        pass
    def backlight_off ( self ):
        pass    
    def backlight_on ( self ):
        pass    
    def off ( self ):
        pass
    def on ( self ):
        pass
try :
    lcd = Lcd1602( I2C_BUS )      # Utilisation de l'écran LCD 1602
    lcd.on()
    lcd.backlight_on()
    lcd.afficher(0,0,"Lcd OK ...")
    sleep_ms(500)
    lcd.backlight_off()
    lcd.off()
except :
    lcd = Console ( )      # Redirection vers la console de Thonny

# =================================================================== lire_fichier (...)
def lire_fichier ( fichier_source:str ) -> str :
    """
    Permet de lire des fichiers du dossier www pour les charger dans une variable texte
    Entrée : fichier_source -> nom du fichier à ouvrir
    Sortie : chaîne de caractères contenant le fichier html / CSS / JavaScipt
    """
    chdir("www")
    with open(fichier_source,"r") as fichier : # Ouvrir le fichier html
        code = fichier.readlines()
    instructions = "".join(code) # assembler toutes les lignes
    if fichier_source=="index.html" :
        instructions = instructions.replace("\n","") # supprimer les fins de lignes
        instructions = instructions.replace("\r","") # supprimer les retours à la ligne
    chdir("..")
    return instructions


# =========================================================================== Timer_interrupt
fin_rebond = Timer(1) # Délai d'attente (rebond BP)
def Timer_BP_flag (pin): # Le drapeau d'interruption et l'état du BP retombent à False
#    global BP.etat
    bp.impulsion = False
def Set_BP_flag (pin): # Le drapeau d'interruption BP est mis à True, début du timing d'antirebond 
#    global BP.etat
    if bp.impulsion==False or bp.drapeau == False:
        bp.impulsion = True # BP.etat est remis à Flase après 200 ms
        bp.drapeau = True # BP.drapeau doit être remis à False par l'utilisateur
        fin_rebond.init(period=200, mode=Timer.ONE_SHOT, callback=Timer_BP_flag) # 200 ms
class Bp (object):
    def __init__ ( self ):
        self.__etat = False # par défaut
        self.impulsion = False
        self.drapeau = False
        self.broche = Pin ( Pin_BP, Pin.IN )        # Bouton Poussoir géré par interruption
        self.broche.irq ( trigger=Pin.IRQ_RISING, handler=Set_BP_flag ) # Interruption si appui sur le BP
    @property
    def etat( self ):
        self.__etat = self.broche.value()
        return self.__etat
# ===========================================================================================
class Bmp180():
    '''
    bmp180 is a micropython module for the Bosch BMP180 sensor. It measures
    temperature as well as pressure, with a high enough resolution to calculate
    altitude.
    Breakoutboard: http://www.adafruit.com/products/1603  
    data-sheet: http://ae-bst.resource.bosch.com/media/products/dokumente/
    bmp180/BST-BMP180-DS000-09.pdf

    The MIT License (MIT)
    Copyright (c) 2014 Sebastian Plamauer, oeplse@gmail.com
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    '''
    _bmp_addr = 119             # adress of BMP180 is hardcoded on the sensor

    # init
    def __init__(self, i2c_bus):

        # create i2c obect
        _bmp_addr = self._bmp_addr
        self._bmp_i2c = i2c_bus
#        self._bmp_i2c.start()
        self.chip_id = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xD0, 2)
        # read calibration data from EEPROM
        self._AC1 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xAA, 2))[0]
        self._AC2 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xAC, 2))[0]
        self._AC3 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xAE, 2))[0]
        self._AC4 = unp('>H', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xB0, 2))[0]
        self._AC5 = unp('>H', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xB2, 2))[0]
        self._AC6 = unp('>H', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xB4, 2))[0]
        self._B1 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xB6, 2))[0]
        self._B2 = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xB8, 2))[0]
        self._MB = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xBA, 2))[0]
        self._MC = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xBC, 2))[0]
        self._MD = unp('>h', self._bmp_i2c.readfrom_mem(_bmp_addr, 0xBE, 2))[0]

        # settings to be adjusted by user
        self.oversample_setting = 3
        self.baseline = 101325.0

        # output raw
        self.UT_raw = None
        self.B5_raw = None
        self.MSB_raw = None
        self.LSB_raw = None
        self.XLSB_raw = None
        self.gauge = self.makegauge() # Generator instance
        for _ in range(128):
            next(self.gauge)
            sleep_ms(1)

    def compvaldump(self):
        '''
        Returns a list of all compensation values
        '''
        return [self._AC1, self._AC2, self._AC3, self._AC4, self._AC5, self._AC6, 
                self._B1, self._B2, self._MB, self._MC, self._MD, self.oversample_setting]

    # gauge raw
    def makegauge(self):
        '''
        Generator refreshing the raw measurments.
        '''
        delays = (5, 8, 14, 25)
        while True:
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x2E]))
            t_start = ticks_ms()
            while (ticks_ms() - t_start) <= 5: # 5mS delay
                yield None
            try:
                self.UT_raw = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF6, 2)
            except:
                yield None
            self._bmp_i2c.writeto_mem(self._bmp_addr, 0xF4, bytearray([0x34+(self.oversample_setting << 6)]))
            t_pressure_ready = delays[self.oversample_setting]
            t_start = ticks_ms()
            while (ticks_ms() - t_start) <= t_pressure_ready:
                yield None
            try:
                self.MSB_raw = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF6, 1)
                self.LSB_raw = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF7, 1)
                self.XLSB_raw = self._bmp_i2c.readfrom_mem(self._bmp_addr, 0xF8, 1)
            except:
                yield None
            yield True

    def blocking_read(self):
        if next(self.gauge) is not None: # Discard old data
            pass
        while next(self.gauge) is None:
            pass

    @property
    def oversample_sett(self):
        return self.oversample_setting

    @oversample_sett.setter
    def oversample_sett(self, value):
        if value in range(4):
            self.oversample_setting = value
        else:
            print('oversample_sett can only be 0, 1, 2 or 3, using 3 instead')
            self.oversample_setting = 3

    @property
    def temperature(self):
        '''
        Temperature in degree C.
        '''
        next(self.gauge)
        try:
            UT = unp('>H', self.UT_raw)[0]
        except:
            return 0.0
        X1 = (UT-self._AC6)*self._AC5/2**15
        X2 = self._MC*2**11/(X1+self._MD)
        self.B5_raw = X1+X2
        val = int((((X1+X2)+8)/2**4))
        return val/10

    @property
    def pression(self):
        '''
        Pressure in hPa.
        '''
        next(self.gauge)
        self.temperature  # Populate self.B5_raw
        try:
            MSB = unp('B', self.MSB_raw)[0]
            LSB = unp('B', self.LSB_raw)[0]
            XLSB = unp('B', self.XLSB_raw)[0]
        except:
            return 0.0
        UP = ((MSB << 16)+(LSB << 8)+XLSB) >> (8-self.oversample_setting)
        B6 = self.B5_raw-4000
        X1 = (self._B2*(B6**2/2**12))/2**11
        X2 = self._AC2*B6/2**11
        X3 = X1+X2
        B3 = ((int((self._AC1*4+X3)) << self.oversample_setting)+2)/4
        X1 = self._AC3*B6/2**13
        X2 = (self._B1*(B6**2/2**12))/2**16
        X3 = ((X1+X2)+2)/2**2
        B4 = abs(self._AC4)*(X3+32768)/2**15
        B7 = (abs(UP)-B3) * (50000 >> self.oversample_setting)
        if B7 < 0x80000000:
            pressure = (B7*2)/B4
        else:
            pressure = (B7/B4)*2
        X1 = (pressure/2**8)**2
        X1 = (X1*3038)/2**16
        X2 = (-7357*pressure)/2**16
        return int((pressure+(X1+X2+3791)/2**4)/100)

    @property
    def altitude(self):
        '''
        Altitude in m.
        '''
        try:
            p = -7990.0*log(self.pression/self.baseline)
        except:
            p = 0.0
        return p
# ============================================================== SoproLab_BUZZER
class Buzzer ( object ):
    def __init__ ( self ):
        self.T = int(0) # Durée d'une période
        self.nbT = int(0) # nombre de périodes
        self.Pin = Pin(Pin_BUZZ, Pin.OUT)
    def son ( self, freq=440, duree=200 ):
        self.T = int(1000000/freq) # Durée d'une période en µs
        self.nbT = int((duree*1000)/self.T) # Nombre de périodes
        for cptr in range(self.nbT):
            self.Pin.on()
            sleep_us( int( self.T/2 ))
            self.Pin.off()
            sleep_us( int( self.T/2))
    def beep ( self ):
        self.son(880, 100)
# ============================================================== SoproLab_CTN
class Ctn (object):
    valeur = 0
    def __init__ ( self ) :
        self.broche = ADC(Pin(Pin_CTN))
        self.broche.atten(ADC.ATTN_11DB)
    @property
    def valeur ( self ):
        self.valeur = self.broche.read()
        return self.valeur
# ============================================================== SoproLab_POT
class Pot (object):
    def __init__ ( self ) :
        self.__broche = ADC(Pin(Pin_POT))
        self.__broche.atten(ADC.ATTN_11DB)
        self.__valeur = self.valeur
        self.__tension = self.tension
    @property
    def valeur ( self ):
        self.__valeur = 4095 - self.__broche.read()
        return self.__valeur # potentiomètre monté à l'envers !
    @property
    def tension ( self ):
        self.__tension = ( self.__valeur / 4095*3.3 )
        return self.__tension
# ============================================================== SoproLab_LDR
class Ldr (object):
    valeur = 0
    def __init__ ( self ) :
        self.broche = ADC (Pin(Pin_LDR))
        self.broche.atten( ADC.ATTN_11DB )
        self.__valeur = self.valeur
    @property
    def valeur ( self ):
        self.__valeur = self.broche.read()
        return self.__valeur
# =====================================================
class Neopixel ( NeoPixel ):
    def __init__ ( self ):
        NeoPixel.__init__ ( self, Pin(Pin_NEOPIXEL), Nb_NEOPIXEL )
        self.__nb_led = Nb_NEOPIXEL
    def eteindre( self ):
        for i in range(self.__nb_led):
            self[i]=(0, 0, 0)
            self.write()
# ===================================================== Déclaration des instances
neopixel = Neopixel ( )  # Commande des LED Neopixel
ledv = Pin(Pin_LED_V, Pin.OUT) # Commande de la LED Verte / Jaune / Rouge
ledj = Pin(Pin_LED_J, Pin.OUT) 
ledr = Pin(Pin_LED_R, Pin.OUT) 
bp  = Bp()
ctn = Ctn()            # Capteur température CTN
pot = Pot()            # Potentiomètre
ldr = Ldr()            # Capteur lumière LDR
bmp = Bmp180( I2C_BUS )# Capteur Pression / température ambiantes
buz = Buzzer()         # Commande du Buzzer