import RPi.GPIO as io
from rpi_ws281x import *
from time import sleep, time


class My_Servo ( io.PWM ) :
    def __init__ ( self, servoPin:int ,angle=90) :
        self.__pin = servoPin
        io.setup(servoPin, io.OUT)
        super().__init__(servoPin, 50 )
    def __new__ ( self, pin ):
        io.setup(pin, io.OUT)
        instance = super().__new__(self)
        return instance
    # ======================================================== start
    def start ( self, pos_angle ):
        assert 0 <= pos_angle <= 180, 'object.start ( angle ) : angle [0, 180 ]'
        duty = self.__duty_angle ( pos_angle ) 
        self.ChangeFrequency ( 50 )
        super().start(duty)
    # ======================================================== __duty_angle
    def __duty_angle ( self, angle:int ) -> float :
        """
        Conversion de l'angle de positionnement du servo moteur
        en DutyCycle [ 2.5 ; 12.5 ]
        """
        return (angle/180)*10+2.5
    # ======================================================== pos_angle
    def pos_angle ( self, angle:int ) :
        """
        Conversion de l'angle de positionnement du servo moteur
        en DutyCycle à appliquer pour le servo [ 2.5 ; 12.5 ]
        """
        duty = self.__duty_angle ( angle )
        self.ChangeDutyCycle ( duty )
    # ======================================================== stop ( )
    def stop ( self ) :
        """
        fin du positionnement
        """
        super().stop()

# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
class My_NeoPixel ( Adafruit_NeoPixel ): # La classe My_NEOPIXEL hérite de la classe NeoPixel
    def __init__ ( self ): # LED strip configuration:
        self.LED_COUNT      = 8      # Number of LED pixels.
        self.LED_PIN        = 12     # GPIO 12 -> pin connected to the pixels
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        super().__init__( self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        super().begin()
    def arc_en_ciel ( self ): # Permet de déclarer de nouvelles méthodes
        niv = [ 0, 0, 0, 35, 65, 35, 0, 0, 0 ]
        for i in range ( 6 ):
            self.setPixelColor(i,  Color(niv[i], niv[(i+2)%6], niv[(i+4)%6] ))
        self.setPixelColor( 6, Color(5,  5,  5))
        self.setPixelColor( 7, Color(125, 125, 125))
        self.show()
        sleep(1.5)
        self.setPixelColor (7, Color(0, 0, 0)) # Eteindre la dernière LED
        for cptr in range(8): # décaler 8 fois les LED
            for cptr in range(7): # décaler chaque LED d'un cran
                buff = super().getPixelColor(cptr+1)
                self.setPixelColor(cptr, buff)
            self.show()
            sleep(0.075)
    def eteindre ( self ):
        for i in range ( self.LED_COUNT ) :
            self.setPixelColor(i, Color(0,0,0))
        self.show()
    def setPixelColor (self, i, couleurRGB ):
        super().setPixelColor(i, couleurRGB)
    def show ( self ) :
        super().show()
