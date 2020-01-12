# from machine import Pin
# from time import ticks_us, sleep, sleep_us

# Déclaration des broches
buzzer = Pin(4, Pin.OUT)

def Set_Micro_flag ( ):
    microphone.impulsion = True 

class Microphone ( object ):
    impulsion = False
    self.broche = Pin(0, Pin.IN)
    def __init__ ( self ):
        self.broche.irq ( trigger=Pin.IRQ_RISING, handler=Set_Micro_flag ) # Interruption si appui sur le BP
        self.impulsion = False
        
def Chrono_µs_on ( ):
    return ticks_us()
    
def Chrono_µs_off( ):
    end_time = tick_us()
    microphone.impulsion = False
    return end_time

microphone = Microphone()

    