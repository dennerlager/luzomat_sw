import time
import queue
import signal
import multiprocessing
from gpio import Output
from message import Message

class AirValve:
    def __init__(self):
        self.qToWorker = multiprocessing.Queue()
        self.worker = AirValveWorker(self.qToWorker)
        self.worker.start()

    def open(self):
        self.qToWorker.put(Message('open'))

    def close(self):
        self.qToWorker.put(Message('close'))

    def shutdown(self):
        self.qToWorker.put(Message('shutdown'))
        self.worker.join()

class AirValveWorker(multiprocessing.Process):
    def __init__(self, qToWorker):
        multiprocessing.Process.__init__(self)
        self.qToWorker = qToWorker
        self.valve = Output(37)
        self.keepValveOpenUntil = 0

    def run(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        try:
            while True:
                self.controlValve()
                try:
                    message = self.qToWorker.get(block=True, timeout=0.1)
                except queue.Empty:
                    continue
                if message.command == 'shutdown':
                    break
                elif message.command == 'open':
                    self.triggerAirValve()
                elif message.command == 'close':
                    self.closeAirValve()
                else:
                    raise ValueError('no command: {}'.format(message))
        finally:
            self.shutdownAirValve()

    def controlValve(self):
        if time.time() < self.keepValveOpenUntil:
            self.openAirValve()
        else:
            self.closeAirValve()

    def openAirValve(self):
        self.valve.set()

    def closeAirValve(self):
        self.valve.clear()
        self.keepValveOpenUntil = 0

    def triggerAirValve(self):
        self.keepValveOpenUntil = time.time() + 30

    def shutdownAirValve(self):
        self.closeAirValve()

if __name__ == '__main__':
    airValve = AirValve()
    airValve.open()
    input('trigger? ')
    airValve.open()
    input('shutdown? ')
    airValve.shutdown()
