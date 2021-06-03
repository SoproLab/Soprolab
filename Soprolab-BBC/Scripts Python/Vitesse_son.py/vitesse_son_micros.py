from microbit import pin15, pin16, pin3, display
from time import ticks_us
display.off()
while pin16.read_digital():
    pass
t0=ticks_us()
while pin15.read_digital():
    pass
t1=ticks_us()
delta_t = t1 - t0

d = (352)*(delta_t/10**6)
print("La distance est de {:3.2f} m ".format(d))

while pin3.read_digital() :
    pass
