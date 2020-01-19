from machine import Pin
LED_v = Pin ( 12, Pin.OUT )
LED_r = Pin ( 14, Pin.OUT )
Bouton = Pin ( 35, Pin.IN )

while True :
    etat = Bouton.value ( )
    if etat==1 :
        LED_v.on()
        LED_r.off()
    else:
        LED_v.off()
        LED_r.on()
            