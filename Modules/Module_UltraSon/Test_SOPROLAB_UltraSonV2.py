# Test_SOPROLAB_UltraSonV2.py - 2019-12-30 - 12h
from SOPROLAB import *
from SOPROLAB_UltraSonV2 import *

PIV.start()
PIV.direction ( 0, 5 ) # Orientation 0° - vitesse 5
sleep_ms(800)
print("Distance mesurée : ", HCSR.distance_mm() )
for cptr in range(0, 200, 10):
    PIV.direction ( cptr, 8 )
    sleep_ms ( 100 )
    print("Distance mesurée : ", HCSR.distance_mm() )
PIV.direction( 0, 10 )
PIV.stop()

sleep_ms(1500)

PIV.start()
PIV.direction(90, 1)
PIV.stop()
    
    
