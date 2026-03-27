from bmp280 import BMP280

s=BMP280()

print("Temperature :", s.get_temperature(), "°C")

print("Pression : ",s.get_pressure(), "hPa")

print("Altitude : ",s.get_altitude()," m")