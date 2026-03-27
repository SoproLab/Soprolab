"""
Utiliser une LED en mode PWM
"""
import RPi.GPIO as io
from RPi.GPIO import PWM
from time import sleep

io.setmode( io.BCM )
io.setwarnings(False)

io.setup ( 17, io.OUT) # Broche 17 -> Led Verte
myled = io.PWM(17, 100) # Broche / fréquence
myled.start(5) # dutyCycle [0.0 ; 100.0 ]
sleep(2)
for i in range(100):
    myled.ChangeDutyCycle(i)
    sleep(0.1)
myled.ChangeDutyCycle(50)
myled.ChangeFrequency(2)
sleep(3)
myled.stop()

