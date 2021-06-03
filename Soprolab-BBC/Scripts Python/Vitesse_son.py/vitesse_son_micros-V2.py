from microbit import *
from time import ticks_us, sleep_ms, sleep
# distance entre les deux microphones : 1,19m
d = 1.79
pin15.set_pull(0)
pin16.set_pull(0)
while True:
  print("Clap !")
  sleep_ms(500)
  while pin16.read_digital():
    pass
  t0 = ticks_us()
  while pin15.read_digital():
    pass
  # 203µs : temps de traitement des instructions : ticks_us et test de la boucle while
  delta_t = ticks_us() - t0 - 203 
  if delta_t :
      print("delta_t : {:3.2} µs".format(delta_t))
      vitesse = (d/delta_t)*(10**6) # *(10**6) => conversion µs -> s
      print("Vitesse : {:3.2f} m/s".format(vitesse))
      sleep(2)
