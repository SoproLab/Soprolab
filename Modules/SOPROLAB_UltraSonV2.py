# SOPROLAB_UltraSonV2.py - 2019-12-30 - 12h00 -
from machine import Pin, PWM, time_pulse_us
from micropython import const
from time import sleep_ms, sleep_us

Pin_Trig = const(17)
Pin_Echo = const(16)
Pin_Pivot = const(15) # Connexion du servomoteur

class SoproLab_Pivot ( object ):
    def __init__ ( self ):
        self.angle = 90
        self.duty = 80
        self.start ( )
        self.direction ( 90, 1 )
    def direction ( self, angle=90, speed=4 ):
        """ La méthode direction permet de contrôler le déplacement du servo moteur sur lequel est fixé
            le capteur de distance à ultrason.
            Deux arguments sont nécessaires : l'angle de positionnement compris entre [ 0 et 180 ]
            et la vitesse de rotation comprise entre [ 1 et 10 ]
            Le servo moteur ne se déplace que si la variation d'angle est au moins de 5° """
        if speed > 10:# limiter la valeur de la vitesse de rotation à l'intervalle [ 1 ; 10 ]
            speed = 10
        elif speed < 1:
            speed = 1
        if angle>=0 and angle<=180:
            delta_angle = angle-self.angle # nbre de pas pour la variation angulaire par rapport à la position actuelle
            if delta_angle>0:                   # => delta_angle peut être >0 ou <0
                nb_pas = delta_angle // 5
                pas = 5
            else:
                nb_pas = ( delta_angle // 5 ) * ( -1 )
                pas = -5
            for n in range ( nb_pas ):
                self.angle = self.angle + pas
                self.duty = self.angle//2 + 35 # conversion ° angulaire <-> duty du PWM
                self.broche.duty(self.duty)
                sleep_ms(10*(11-speed)+20) # temporisation pour variation de la vitesse de rotation
    def start( self ):
        self.broche = PWM(Pin(Pin_Pivot), freq=50)
        self.broche.duty(self.duty)
        
    def stop ( self ):
        self.broche.deinit()

__author__ = 'Roberto S鐠嬶箯chez'
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

class HCSR04:
    """
    Driver to use the untrasonic sensor HC-SR04.
    The sensor range is between 2cm and 4m.
    The timeouts received listening to echo pin are converted to OSError('Out of range')
    """
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__( self ):
        """
        Version 0.2.0
        trigger_pin: Output pin to send pulses
        echo_pin: Readonly pin to measure the distance. The pin should be protected with 1k resistor
        echo_timeout_us: Timeout in microseconds to listen to echo pin. 
        By default is based in sensor limit range (4m)
        """
        self.echo_timeout_us = 500*2*30
        self.trigger = Pin(Pin_Trig, mode=Pin.OUT, pull=None)         # Init trigger pin (out)
        self.trigger.value(0)
        self.echo = Pin(Pin_Echo, mode=Pin.IN, pull=None) # Init echo pin (in)

    def _send_pulse_and_wait(self):
        """
        Send the pulse to trigger and listen on echo pin.
        We use the method `machine.time_pulse_us()` to get the microseconds until the echo is received.
        """
        self.trigger.value(0) # Stabilize the sensor
        sleep_us(5)
        self.trigger.value(1)
        sleep_us(10)         # Send a 10us pulse.
        self.trigger.value(0)
        try:
            pulse_time = time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms       

PIV = SoproLab_Pivot()
HCSR = HCSR04()            
        
