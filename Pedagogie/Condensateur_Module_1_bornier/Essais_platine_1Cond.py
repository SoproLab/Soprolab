from machine import Pin, ADC
from time import sleep_us, sleep_ms, ticks_ms

broche = ADC(Pin(36))
broche.atten(ADC.ATTN_11DB)

tps_val = [[0,0] for i in range(200) ]
t0 = ticks_ms()
for n in range (200):
    tps_val[n][0] = ticks_ms()-t0
    tps_val[n][1] = broche.read()
    sleep_ms(15)
print("tps(ms), val(0->4095)")
for n in range (200):
    print("{:d},{:d}".format(tps_val[n][0],tps_val[n][1]))
    sleep_ms(2)
