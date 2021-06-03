from microbit import pin1, button_a
from utime import sleep_ms

while button_a.is_pressed() == False :
    
    val = pin1.read_analog()
    
    print("Pression mesurée : ",val)
    
    sleep_ms(200)
