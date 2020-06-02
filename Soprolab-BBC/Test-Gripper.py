"""
test gripper avec servo moteur continu
-> Port 0 -> Connecteur vert sur l'adaptateur XH4P - 4 pin labtech
"""
from microbit import pin13, Image, display
from time import sleep_ms
image_ouvrir = Image( "00000\n"
                      "09090\n"
                      "95559\n"
                      "09090\n"
                      "00000")
image_fermer = Image( "00000\n"
                      "90009\n"
                      "09590\n"
                      "90009\n"
                      "00000")

display.on()
display.show(Image.HAPPY)
sleep_ms(1000)

display.show(image_fermer)
pin13.write_analog(80)
sleep_ms(1200)
pin13.write_analog(0)
sleep_ms(2500)

display.show(image_ouvrir)
pin13.set_analog_period(20)
pin13.write_analog(70)
sleep_ms(400)
pin13.write_analog(0)
sleep_ms(2500)


pin13.write_analog(0)
display.show(Image.HAPPY)
sleep_ms(1000)
display.off()
