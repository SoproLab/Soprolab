import RPi.GPIO as io
from gpiozero import TonalBuzzer
from time import sleep, time
import Adafruit_ADS1x15
from bmp280 import BMP280
from piHat import My_Servo, My_NeoPixel

io.setmode(io.BCM) # Using GPIO mode, not the connector mode
io.setwarnings(False)
adc = Adafruit_ADS1x15.ADS1015()
b=TonalBuzzer(13)


#b.play(220.0)
#sleep(0.3)
#b.stop()

ledv = 17
ledj = 22
ledr = 27
bp = 5
xh1_1 = 24
xh1_2 = 4
sil_1 = 25
sil_3 = 26
xh2_1 = 18
xh2_2 = 15
xh2_3 = 14

io.setup(ledv, io.OUT)
io.setup(ledj, io.OUT)
io.setup(ledr, io.OUT)
io.setup(bp, io.IN)
io.setup(xh1_1, io.OUT)
io.setup(xh1_2, io.OUT)
io.setup(sil_1, io.OUT)
io.setup(sil_3, io.OUT)
io.setup(xh2_1, io.OUT)
io.setup(xh2_2, io.OUT)
io.setup(xh2_3, io.OUT)

io.output(ledv,1)
io.output(ledj,1)
io.output(ledr,1)
sleep(0.3)

my_servo = My_Servo ( 19 )
strip = My_NeoPixel( )

print("### Test BMP280 ### \n Suite : BP ....")
while not io.input(bp) :
    pass
io.output(ledv,0)
io.output(ledj,0)
io.output(ledr,0)
"""
captr=BMP280()
for _ in range ( 3 ):
    print("Temperature :", captr.get_temperature(), "°C")
    print("Pression : ",captr.get_pressure(), "hPa")
    print("Altitude : ",captr.get_altitude()," m\n")
    captr.update_sensor()
    sleep(0.3)

print("### Test ADC ### \n Suite : BP ....")
while not io.input(bp) :
    pass
adc.start_adc(3, gain=1)
start = time()
sleep(0.3)
while not io.input(bp) :
    value = adc.get_last_result()
    print('Channel 0: {0}'.format(value))
    sleep(0.3)
adc.stop_adc()
sleep(0.3)
"""
print("### Test NeoPixel ### \n Suite : BP ....")

strip.arc_en_ciel()

print("### Test ServoMoteur ### \n Suite : BP ....")
while not io.input(bp) :
    pass
sleep(0.3)

my_servo.start( 0 )
sleep(0.5)

for i in range(0, 180) :
    my_servo.pos_angle(i)
    sleep(0.01)
sleep(0.5)
for i in range(180,0,-1):
    my_servo.pos_angle(i)
    sleep(0.01)
my_servo.stop()

print("### Test GPIO 24, 4, 25, 26, 18,  ### \n Suite : BP ....")
while not io.input(bp) :
    pass
sleep(0.5)

gpio = (xh1_1, xh1_2, sil_1, sil_3, xh2_1, xh2_2, xh2_3)
nb_gpio = len(gpio)
cptr = 0
while not io.input(bp) :
    io.output(gpio[cptr-1], 0) # éviter la rémanence du tour précédent
    io.output(gpio[cptr], 1) # mettre un gpio à 1
    for i in range(1, nb_gpio-1) : # mettre les autres à 0
        io.output(gpio[(cptr+i)%nb_gpio], 0)
    if cptr<nb_gpio-1 :
        cptr += 1
    else :
        cptr = 0
    sleep(0.3)

io.cleanup()


