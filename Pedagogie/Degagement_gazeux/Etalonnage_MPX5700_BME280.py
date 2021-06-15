"""
Etalonnge du capteur MPX5700 avec un BME280

Contexte :
Le BMP180 de la carte SoproLab perpet un étalonnage sur une valeur
afin de permettre l'utilisation du capteur MPX5700 comme pressiomètre.

Pour obtenir une courbe d'étalonnage, il est nécessaire d'effectuer
plusieurs meusures de pression et de relever les valeurs obtenues
avec le MPX5700 afin de vérifier la linéarité et l'étalonnage.

Or, il est difficile de placer la carte SoproLab à différentes pressions !!!
On a donc recours à un deuxième capteur numérique : BME280 branché sur connecteur
RJ11 : BUS I2C. Ce capteur est placé dans un tube à essais étanche avec
un T en sortie -> seringue pour variation de pression et -> MPX5700

Ce script reprend l'intégralité de la bibliothèque du BME280.

"""
from micropython import const
from machine import Pin, I2C, ADC
from time import sleep_ms, sleep_us

Pin_MPX = const(39)

# BME280 default address.
BME280_I2CADDR = 0x76

# Operating Modes
BME280_OSAMPLE_1 = 1
BME280_OSAMPLE_2 = 2
BME280_OSAMPLE_4 = 3
BME280_OSAMPLE_8 = 4
BME280_OSAMPLE_16 = 5

# BME280 Registers

BME280_REGISTER_DIG_T1 = 0x88  # Trimming parameter registers
BME280_REGISTER_DIG_T2 = 0x8A
BME280_REGISTER_DIG_T3 = 0x8C

BME280_REGISTER_DIG_P1 = 0x8E
BME280_REGISTER_DIG_P2 = 0x90
BME280_REGISTER_DIG_P3 = 0x92
BME280_REGISTER_DIG_P4 = 0x94
BME280_REGISTER_DIG_P5 = 0x96
BME280_REGISTER_DIG_P6 = 0x98
BME280_REGISTER_DIG_P7 = 0x9A
BME280_REGISTER_DIG_P8 = 0x9C
BME280_REGISTER_DIG_P9 = 0x9E

BME280_REGISTER_DIG_H1 = 0xA1
BME280_REGISTER_DIG_H2 = 0xE1
BME280_REGISTER_DIG_H3 = 0xE3
BME280_REGISTER_DIG_H4 = 0xE4
BME280_REGISTER_DIG_H5 = 0xE5
BME280_REGISTER_DIG_H6 = 0xE6
BME280_REGISTER_DIG_H7 = 0xE7

BME280_REGISTER_CHIPID = 0xD0
BME280_REGISTER_VERSION = 0xD1
BME280_REGISTER_SOFTRESET = 0xE0

BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_CONTROL = 0xF4
BME280_REGISTER_CONFIG = 0xF5
BME280_REGISTER_PRESSURE_DATA = 0xF7
BME280_REGISTER_TEMP_DATA = 0xFA
BME280_REGISTER_HUMIDITY_DATA = 0xFD


class Device:
  """Class for communicating with an I2C device.

  Allows reading and writing 8-bit, 16-bit, and byte array values to
  registers on the device."""

  def __init__(self, address, i2c):
    """Create an instance of the I2C device at the specified address using
    the specified I2C interface object."""
    self._address = address
    self._i2c = i2c

  def writeRaw8(self, value):
    """Write an 8-bit value on the bus (without register)."""
    value = value & 0xFF
    self._i2c.writeto(self._address, value)

  def write8(self, register, value):
    """Write an 8-bit value to the specified register."""
    b=bytearray(1)
    b[0]=value & 0xFF
    self._i2c.writeto_mem(self._address, register, b)

  def write16(self, register, value):
    """Write a 16-bit value to the specified register."""
    value = value & 0xFFFF
    b=bytearray(2)
    b[0]= value & 0xFF
    b[1]= (value>>8) & 0xFF
    self.i2c.writeto_mem(self._address, register, value)

  def readRaw8(self):
    """Read an 8-bit value on the bus (without register)."""
    return int.from_bytes(self._i2c.readfrom(self._address, 1),'little') & 0xFF

  def readU8(self, register):
    """Read an unsigned byte from the specified register."""
    return int.from_bytes(
        self._i2c.readfrom_mem(self._address, register, 1),'little') & 0xFF

  def readS8(self, register):
    """Read a signed byte from the specified register."""
    result = self.readU8(register)
    if result > 127:
      result -= 256
    return result

  def readU16(self, register, little_endian=True):
    """Read an unsigned 16-bit value from the specified register, with the
    specified endianness (default little endian, or least significant byte
    first)."""
    result = int.from_bytes(
        self._i2c.readfrom_mem(self._address, register, 2),'little') & 0xFFFF
    if not little_endian:
      result = ((result << 8) & 0xFF00) + (result >> 8)
    return result

  def readS16(self, register, little_endian=True):
    """Read a signed 16-bit value from the specified register, with the
    specified endianness (default little endian, or least significant byte
    first)."""
    result = self.readU16(register, little_endian)
    if result > 32767:
      result -= 65536
    return result

  def readU16LE(self, register):
    """Read an unsigned 16-bit value from the specified register, in little
    endian byte order."""
    return self.readU16(register, little_endian=True)

  def readU16BE(self, register):
    """Read an unsigned 16-bit value from the specified register, in big
    endian byte order."""
    return self.readU16(register, little_endian=False)

  def readS16LE(self, register):
    """Read a signed 16-bit value from the specified register, in little
    endian byte order."""
    return self.readS16(register, little_endian=True)

  def readS16BE(self, register):
    """Read a signed 16-bit value from the specified register, in big
    endian byte order."""
    return self.readS16(register, little_endian=False)


class BME280:
  def __init__(self, mode=BME280_OSAMPLE_1, address=BME280_I2CADDR, i2c=None,
               **kwargs):
    # Check that mode is valid.
    if mode not in [BME280_OSAMPLE_1, BME280_OSAMPLE_2, BME280_OSAMPLE_4,
                    BME280_OSAMPLE_8, BME280_OSAMPLE_16]:
        raise ValueError(
            'Unexpected mode value {0}. Set mode to one of '
            'BME280_ULTRALOWPOWER, BME280_STANDARD, BME280_HIGHRES, or '
            'BME280_ULTRAHIGHRES'.format(mode))
    self._mode = mode
    # Create I2C device.
    if i2c is None:
      raise ValueError('An I2C object is required.')
    self._device = Device(address, i2c)
    # Load calibration values.
    self._load_calibration()
    self._device.write8(BME280_REGISTER_CONTROL, 0x3F)
    self.t_fine = 0

  def _load_calibration(self):

    self.dig_T1 = self._device.readU16LE(BME280_REGISTER_DIG_T1)
    self.dig_T2 = self._device.readS16LE(BME280_REGISTER_DIG_T2)
    self.dig_T3 = self._device.readS16LE(BME280_REGISTER_DIG_T3)

    self.dig_P1 = self._device.readU16LE(BME280_REGISTER_DIG_P1)
    self.dig_P2 = self._device.readS16LE(BME280_REGISTER_DIG_P2)
    self.dig_P3 = self._device.readS16LE(BME280_REGISTER_DIG_P3)
    self.dig_P4 = self._device.readS16LE(BME280_REGISTER_DIG_P4)
    self.dig_P5 = self._device.readS16LE(BME280_REGISTER_DIG_P5)
    self.dig_P6 = self._device.readS16LE(BME280_REGISTER_DIG_P6)
    self.dig_P7 = self._device.readS16LE(BME280_REGISTER_DIG_P7)
    self.dig_P8 = self._device.readS16LE(BME280_REGISTER_DIG_P8)
    self.dig_P9 = self._device.readS16LE(BME280_REGISTER_DIG_P9)

    self.dig_H1 = self._device.readU8(BME280_REGISTER_DIG_H1)
    self.dig_H2 = self._device.readS16LE(BME280_REGISTER_DIG_H2)
    self.dig_H3 = self._device.readU8(BME280_REGISTER_DIG_H3)
    self.dig_H6 = self._device.readS8(BME280_REGISTER_DIG_H7)

    h4 = self._device.readS8(BME280_REGISTER_DIG_H4)
    h4 = (h4 << 24) >> 20
    self.dig_H4 = h4 | (self._device.readU8(BME280_REGISTER_DIG_H5) & 0x0F)

    h5 = self._device.readS8(BME280_REGISTER_DIG_H6)
    h5 = (h5 << 24) >> 20
    self.dig_H5 = h5 | (
        self._device.readU8(BME280_REGISTER_DIG_H5) >> 4 & 0x0F)

  def read_raw_temp(self):
    """Reads the raw (uncompensated) temperature from the sensor."""
    meas = self._mode
    self._device.write8(BME280_REGISTER_CONTROL_HUM, meas)
    meas = self._mode << 5 | self._mode << 2 | 1
    self._device.write8(BME280_REGISTER_CONTROL, meas)
    sleep_time = 1250 + 2300 * (1 << self._mode)

    sleep_time = sleep_time + 2300 * (1 << self._mode) + 575
    sleep_time = sleep_time + 2300 * (1 << self._mode) + 575
    sleep_us(sleep_time)  # Wait the required time
    msb = self._device.readU8(BME280_REGISTER_TEMP_DATA)
    lsb = self._device.readU8(BME280_REGISTER_TEMP_DATA + 1)
    xlsb = self._device.readU8(BME280_REGISTER_TEMP_DATA + 2)
    raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
    return raw

  def read_raw_pressure(self):
    """Reads the raw (uncompensated) pressure level from the sensor."""
    """Assumes that the temperature has already been read """
    """i.e. that enough delay has been provided"""
    msb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA)
    lsb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA + 1)
    xlsb = self._device.readU8(BME280_REGISTER_PRESSURE_DATA + 2)
    raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
    return raw

  def read_raw_humidity(self):
    """Assumes that the temperature has already been read """
    """i.e. that enough delay has been provided"""
    msb = self._device.readU8(BME280_REGISTER_HUMIDITY_DATA)
    lsb = self._device.readU8(BME280_REGISTER_HUMIDITY_DATA + 1)
    raw = (msb << 8) | lsb
    return raw

  def read_temperature(self):
    """Get the compensated temperature in 0.01 of a degree celsius."""
    adc = self.read_raw_temp()
    var1 = ((adc >> 3) - (self.dig_T1 << 1)) * (self.dig_T2 >> 11)
    var2 = ((
        (((adc >> 4) - self.dig_T1) * ((adc >> 4) - self.dig_T1)) >> 12) *
        self.dig_T3) >> 14
    self.t_fine = var1 + var2
    return (self.t_fine * 5 + 128) >> 8

  def read_pressure(self):
    """Gets the compensated pressure in Pascals."""
    adc = self.read_raw_pressure()
    var1 = self.t_fine - 128000
    var2 = var1 * var1 * self.dig_P6
    var2 = var2 + ((var1 * self.dig_P5) << 17)
    var2 = var2 + (self.dig_P4 << 35)
    var1 = (((var1 * var1 * self.dig_P3) >> 8) +
            ((var1 * self.dig_P2) >> 12))
    var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
    if var1 == 0:
      return 0
    p = 1048576 - adc
    p = (((p << 31) - var2) * 3125) // var1
    var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
    var2 = (self.dig_P8 * p) >> 19
    return ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)

  def read_humidity(self):
    adc = self.read_raw_humidity()
    # print 'Raw humidity = {0:d}'.format (adc)
    h = self.t_fine - 76800
    h = (((((adc << 14) - (self.dig_H4 << 20) - (self.dig_H5 * h)) +
         16384) >> 15) * (((((((h * self.dig_H6) >> 10) * (((h *
                          self.dig_H3) >> 11) + 32768)) >> 10) + 2097152) *
                          self.dig_H2 + 8192) >> 14))
    h = h - (((((h >> 15) * (h >> 15)) >> 7) * self.dig_H1) >> 4)
    h = 0 if h < 0 else h
    h = 419430400 if h > 419430400 else h
    return h >> 12

  @property
  def temperature(self):
    "Return the temperature in degrees."
    t = self.read_temperature()
    ti = t // 100
    td = t - ti * 100
    return "{}.{:02d}C".format(ti, td)

  @property
  def pressure(self):
    "Return the temperature in hPa."
    p = self.read_pressure() // 256
    pi = p // 100
    pd = p - pi * 100
    return "{}.{:02d}hPa".format(pi, pd)

  @property
  def humidity(self):
    "Return the humidity in percent."
    h = self.read_humidity()
    hi = h // 1024
    hd = h * 100 // 1024 - hi * 100
    return "{}.{:02d}%".format(hi, hd)
# ============================================================== SoproLab_MPX
class SoproLab_MPX ( ):
    etalon = None
    def __init__ ( self, broche_MPX, capteur ) :
        SoproLab_MPX.etalon = capteur
        self.broche = ADC (Pin(broche_MPX))
        self.broche.atten( ADC.ATTN_11DB )
        self.__delta_p = self.etalonnage ( )
        self.__pression = self.pression
        
    def etalonnage ( self ):
        if SoproLab_MPX.etalon.__qualname__ == 'BME280' :
            val_temp = SoproLab_MPX.etalon.temperature # Mise à jour -> lecture température
            pression_bme = SoproLab_MPX.etalon.pressure # format str avec 'hPa' en fin de chaîne
            val_press = float(pression_bme[:len(pression_bme)-3])
            
        if SoproLab_MPX.etalon.__qualname__ == 'BMP180' :
            val_temp = SoproLab_MPX.etalon.temperature # Mise à jour -> lecture température
            val_press = SoproLab_MPX.etalon.pression
        print("valeur -> ", self.valeur*2)
        print("etalonnage ->", val_press)
        print("======> delta_p > ",int(self.valeur*2-val_press))
        return int(self.valeur*2-val_press)
        
    @property
    def valeur ( self ):
        val = 0
        for _ in range(3):
            val += self.broche.read()
            sleep_ms(200)
        return int(val/3)
    
    @property
    def pression ( self ):
        return self.valeur*2 - self.__delta_p

# ======================================================= main
if __name__=="__main__":
    bus_i2c = I2C ( 1, scl=Pin(22), sda=Pin(21), freq=400000)
    etalon = BME280(i2c=bus_i2c)
    print("Pression : ", etalon.pressure)
    print("Temperature : ", etalon.temperature)
    print("Humidité :", etalon.humidity)

    capteur_MPX = SoproLab_MPX ( Pin_MPX, etalon )
    print("MPX5700 : {:4d}".format(capteur_MPX.pression ))
    
    n=0
    while n<40 :
        etalon.temperature
        mesure_bme = etalon.pressure # format str avec unité hPa
        mesure_mpx = "{:4d}".format(capteur_MPX.pression)
        print(mesure_bme[:len(mesure_bme)-3],",",mesure_mpx)
        sleep_ms(500)
        n+=1

