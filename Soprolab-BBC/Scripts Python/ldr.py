from microbit import pin0, button_a
from utime import sleep_ms

while button_a.is_pressed() == False :
    
    val = pin0.read_analog()
    
    print("Lumière mesurée : ",val)
    
    sleep_ms(200)
