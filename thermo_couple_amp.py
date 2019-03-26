import spi
import time
import bitstruct
import unittest
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

    def setBitInRegister(self, registername, bit):
        if not 0 <= bit <= 7:
            raise ValueError('{} not valid'.format(bit))
        self.writeRegister(registername,
                           self.readRegister(registername) | 2**bit)

    def configure(self):
        self.writeRegister('configuration_0_register', 0x01)

    def getTemperatureC(self):
        self.triggerOneShot()
        values = self.readRegisters('linearised_tc_temperature_2', 3)
        return self.convert(values)

    def triggerOneShot(self):
        self.setBitInRegister('configuration_0_register', 6)
        self.waitForMeasurement()

    def waitForMeasurement(self):
        time.sleep(0.2)

    def convert(self, values):
        return bitstruct.unpack('>s19p5', values)[0] / 2**7

class TCAmpTest(unittest.TestCase):
    def setUp(self):
        self.tcamp = TCAmp(0)

    def test_convert(self):
        self.assertEqual(self.tcamp.convert(bytes([0, 1, 0])), 0.0625)
        self.assertEqual(self.tcamp.convert(bytes([0xff, 0xff, 0])), -0.0625)
        self.assertEqual(self.tcamp.convert(bytes([6, 0x4f, 0])), 100.9375)

    def test_getTemp(self):
        self.assertAlmostEqual(self.tcamp.getTemperatureC(), 25, delta=10)

    def test_readRegister(self):
        self.assertEqual(self.tcamp.readRegister('cold_junction_high_fault_threshold'), 0x7f)

    def test_writeRegister(self):
        backup = self.tcamp.readRegister('cold_junction_high_fault_threshold')
        self.tcamp.writeRegister('cold_junction_high_fault_threshold', backup + 1)
        self.assertEqual(self.tcamp.readRegister('cold_junction_high_fault_threshold'), backup + 1)
        self.tcamp.writeRegister('cold_junction_high_fault_threshold', backup)

    def test_setBitInRegister(self):
        backup = self.tcamp.readRegister('configuration_0_register')
        self.tcamp.setBitInRegister('configuration_0_register', 3)
        self.assertEqual(self.tcamp.readRegister('configuration_0_register'), backup | 8)
        self.tcamp.writeRegister('configuration_0_register', backup)

    def test_setBitInRegisterRaises(self):
        self.assertRaises(ValueError, self.tcamp.setBitInRegister,
                          'configuration_0_register', 8)
        self.assertRaises(ValueError, self.tcamp.setBitInRegister,
                          'configuration_0_register', -1)

if __name__ == '__main__':
    unittest.main()
    t = TCAmp(0)
    for registername in t.memory.registermap.keys():
        print('{}: 0x{:02x}'.format(registername,
                                    t.readRegister(registername)))
