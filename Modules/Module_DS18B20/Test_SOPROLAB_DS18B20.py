from SOPROLAB import *
from SOPROLAB_DS18B20 import *

DS.mesure()
print("La température est de {:5.2f} °C".format(DS.temperature) )