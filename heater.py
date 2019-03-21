from gpio import Output

class Heater:
    def __init__(self):
        self.asyncResetActiveLow = Output(12)
        self.watchdog = Output(11)
        self.on = False

    def turnOn(self):
        self.asyncResetActiveLow.set()
        self.watchdog.set()
        self.on = True

    def turnOff(self):
        self.asyncResetActiveLow.clear()
        self.watchdog.clear()
        self.on = False

    def isOn(self):
        return self.on

    def resetWatchdog(self):
        self.watchdog.clear()
        self.watchdog.set()
