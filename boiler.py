import queue
import multiprocessing
from heater import Heater
from message import Message
from thermo_couple_amp import TCAmp

class Boiler:
    def __init__(self):
        self.qToWorker = multiprocessing.Queue()
        self.qFromWorker = multiprocessing.Queue()
        self.worker = BoilerWorker(self.qToWorker, self.qFromWorker)
        self.worker.start()

    def setTemperatureC(self, temperatureC):
        if temperatureC > 99:
            raise ValueError('temperature {}°C exeeds limit'.format(temperatureC))
        self.qToWorker.put(Message('setTemperatureC', temperatureC))

    def shutdown(self):
        self.qToWorker.put(Message('shutdown'))
        self.worker.join()

class BoilerWorker(multiprocessing.Process):
    def __init__(self, qToWorker, qFromWorker):
        multiprocessing.Process.__init__(self)
        self.qToWorker = qToWorker
        self.qFromWorker = qFromWorker
        self.setPointC = 0
        self.hysteresis = 2
        self.tempSensor1 = TCAmp(0)
        self.tempSensor2 = TCAmp(1)
        self.heater = Heater()

    def run(self):
        try:
            while True:
                self.controlHeater()
                try:
                    message = self.qToWorker.get(block=True, timeout=0.1)
                except queue.Empty:
                    continue
                if message.command == 'shutdown':
                    break
                elif message.command == 'setTemperatureC':
                    self.setTemperatureC(message.data)
                else:
                    raise ValueError('no command: {}'.format(message))
        finally:
            self.shutdownHeater()

    def controlHeater(self):
        temperature1 = self.tempSensor1.getTemperatureC()
        temperature2 = self.tempSensor2.getTemperatureC()
        maxDelta = 2
        if abs(temperature1 - temperature2) > maxDelta:
            raise RuntimeError(
                'temperatures differ more than {}\n'.format(maxDelta) +
                               'temp1: {}, temp2: {}'.format(
                                   temperature1,
                                   temperature2))
        temperature = (temperature1 + temperature2) / 2
        if ((not self.heater.isOn()) and
            (temperature < self.setPointC - self.hysteresis)):
            self.heater.turnOn()
        if ((self.heater.isOn()) and
            (temperature > self.setPointC + self.hysteresis)):
            self.heater.turnOff()
        self.heater.resetWatchdog()

    def shutdownHeater(self):
        self.heater.turnOff()

    def setTemperatureC(self, temperatureC):
        self.setPointC = temperatureC

if __name__ == '__main__':
    boiler = Boiler()
    boiler.setTemperatureC(50)
    input('shutdown? ')
    boiler.shutdown()
