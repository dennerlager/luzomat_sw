import bitstruct
import unittest
import spi
import thermo_couple_amp_memory

class TCAmp:
    def __init__(self, devicenumber):
        self.memory = thermo_couple_amp_memory.Memory()
        self.spi = spi.Spi(devicenumber)
        self.configure()

    def readRegister(self, registername):
        return self.readRegisters(registername, 1)[0]

    def readRegisters(self, registername, count):
        address = self.memory.getAddress(registername)
        return self.spi.transceive([address] + [0 for i in range(count)])[1:]

    def writeRegister(self, registername, value):
        address = self.memory.getAddress(registername)
        address = self.setWriteBit(address)
        self.spi.transceive([address, value])
        if not self.readRegister(registername) == value:
            raise RuntimeError('failed to write {} to 0x{:02x}'
                               .format(registername, value))

    def setWriteBit(self, address):
        return address | 0x80

    def configure(self):
        self.writeRegister('configuration_0_register', 0x01)
        self.writeRegister('configuration_0_register', 0x11)

    def getTemperatureC(self):
        values = self.readRegisters('linearised_tc_temperature_2', 3)
        return self.convert(values)

    def convert(self, values):
        return bitstruct.unpack('>s19p5', values)[0] / 2**7

class TCAmpTest(unittest.TestCase):
    def setUp(self):
        self.tcamp = TCAmp(0)

    def test_convert(self):
        self.assertEqual(self.tcamp.convert(bytes([0, 1, 0])), 0.0625)
        self.assertEqual(self.tcamp.convert(bytes([0xff, 0xff, 0])), -0.0625)
        self.assertEqual(self.tcamp.convert(bytes([6, 0x4f, 0])), 100.9375)

if __name__ == '__main__':
    unittest.main()
