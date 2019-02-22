""" create udev rule:
SUBSYSTEM=="spidev", GROUP="spiuser", MODE="0660"
"""
import spidev

class Spi:
    def __init__(self, device):
        bus = 0
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 5000000
        print(self.spi.cshigh)
        print(self.spi.bits_per_word)
        print(self.spi.lsbfirst)
        print(self.spi.mode)
        self.spi.mode = 1

    def __del__(self):
        self.spi.close()

    def transceive(self, data):
        return self.spi.xfer2(data)
