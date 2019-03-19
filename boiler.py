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
        self.tempSensor1 = TCAmp(1)
        self.tempSensor2 = TCAmp(2)
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
        pass

    def shutdownHeater(self):
        pass

    def setTemperatureC(self, temperatureC):
        self.setPointC = temperatureC
        print(f'worker sets temp to {temperatureC}C')

if __name__ == '__main__':
    boiler = Boiler()
    boiler.setTemperatureC(20)
    boiler.shutdown()
