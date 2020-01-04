from machine import Pin
from time import ticks_us, sleep, sleep_us

# Déclaration des broches
buzzer = Pin(4, Pin.OUT)
microphone = Pin(0, Pin.IN)
start_time=0
end_time=0

def Chrono_µs_on ( ):
    global start_time
    start_time = ticks_us()

def Chrono_µs_off( ):
    global end_time
    end_time = ticks_us()
    return end_time - start_time
    