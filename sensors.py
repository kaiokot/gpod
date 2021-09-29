
# tks to https://github.com/pimoroni/bmp280-python


from bmp280 import BMP280

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus


class Bmp280:
    def __init__(self):
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)
        pass

    def get_temperature(self):
        return self.bmp280.get_temperature()

    def get_pressure(self):
        return self.bmp280.get_pressure()

    def get_data(self):
        return {
            "pressure": self.get_pressure(),
            "temperature": self.get_temperature()
        }
