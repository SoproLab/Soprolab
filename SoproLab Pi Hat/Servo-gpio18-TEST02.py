"""
Gestion d'un servo moteur type MG996R
Connecteur XH5p, vcc / gnd / GPIO18
"""
from gpiozero import Servo
from time import sleep

# s = Servo(18, min_pulse_width=1/2000, max_pulse_width=1/450, frame_width=4/1000)
s = Servo(19, min_pulse_width=1/1550, max_pulse_width=1/500, frame_width=1/400)
s.value = -0.35
sleep(1)
for i in range(-35,75) : # de 0 à 180 °
    s.value = i/100
    sleep(0.01)
sleep(1)
s.value=None
s.detach()