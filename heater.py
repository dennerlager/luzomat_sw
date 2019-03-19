class Heater:
    def __init__(self):
        self.coil = Gpio(1)
        self.watchdog = Gpio(2)

    def turnOn(self):
        pass

    def turnOff(self):
        pass

    def isTurnedOn(self):
        pass

    def resetWatchdog(self):
        pass
