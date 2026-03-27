from gpiozero import TonalBuzzer
from time import sleep
from gpiozero.tones import Tone

b=TonalBuzzer(13)
b.play(880.0)
sleep(0.5)
b.stop()