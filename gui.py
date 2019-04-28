import tkinter as tk
from luzomat import Luzomat

class Gui(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent)
        self.pack(**options)
        self.luzomat = Luzomat()
        self.makeWidgets()
        self.master.bind('<Escape>', lambda e: self.quit())
        self.updateViews()

    def quit(self):
        self.luzomat.shutdown()
        tk.Frame.quit(self)

    def makeWidgets(self):
        self.temperatureSensor1 = TempSensor(
            self, tempSensorAddress=1, side=tk.TOP,
            padx=10, pady=0, ipadx=5, ipady=5)
        self.temperatureSensor2 = TempSensor(
            self, tempSensorAddress=2, side=tk.TOP,
            padx=10, pady=0, ipadx=5, ipady=5)
        self.ios = {}
        for name in self.luzomat.getCurrentState().keys():
            self.ios[name] = IO(
            self, name, side=tk.TOP,
            padx=10, pady=0, ipadx=5, ipady=5)

    def updateViews(self):
        temperatures = self.luzomat.getTemperatures()
        self.temperatureSensor1.setValue(temperatures[0])
        self.temperatureSensor2.setValue(temperatures[1])
        for name, value in self.luzomat.getCurrentState().items():
            self.ios[name].setValue(value)
        self.after(500, self.updateViews)

class TempSensor(tk.Frame):
    def __init__(self, parent=None, tempSensorAddress=None, **options):
        tk.Frame.__init__(self, parent)
        self.tempSensorAddress = tempSensorAddress
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.tempSensorNameLabel = TempSensorNameLabel(
            self, self.tempSensorAddress, side=tk.LEFT,
            padx=10, pady=0, ipadx=5, ipady=5)
        self.tempSensorValue = TempSensorValueLabel(
            self, -1, side=tk.LEFT,
            padx=10, pady=5, ipadx=5, ipady=5)

    def setValue(self, value):
        self.tempSensorValue.setValue(value)

class TempSensorNameLabel(tk.Label):
    def __init__(self, parent=None, tempSensorAddress=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='temperature sensor {}'.format(tempSensorAddress))

class TempSensorValueLabel(tk.Label):
    def __init__(self, parent=None, value=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.setValue(value)

    def setValue(self, value):
        self.config(text='{:.1f}°C'.format(value))

class IO(tk.Frame):
    def __init__(self, parent=None, name=None, **options):
        tk.Frame.__init__(self, parent)
        self.name = name
        self.pack(**options)
        self.makeWidgets()

    def makeWidgets(self):
        self.ioNameLabel = IONameLabel(
            self, self.name, side=tk.LEFT,
            padx=10, pady=0, ipadx=5, ipady=5)
        self.ioValueLabel = IOValueLabel(
            self, -1, side=tk.LEFT,
            padx=10, pady=5, ipadx=5, ipady=5)

    def setValue(self, value):
        self.ioValueLabel.setValue(value)

class IONameLabel(tk.Label):
    def __init__(self, parent=None, name=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.config(text='{}'.format(name))

class IOValueLabel(tk.Label):
    def __init__(self, parent=None, value=None, **options):
        tk.Label.__init__(self, parent)
        self.pack(**options)
        self.setValue(value)

    def setValue(self, value):
        self.config(text='{}'.format(value))

if __name__ == '__main__':
    root = tk.Tk()
    icon = tk.Image('photo', file='icon.png')
    root.tk.call('wm', 'iconphoto', root._w, icon)
    root.option_add('*Font', 'DejaVuSans 20')
    myapp = Gui(root)
    root.mainloop()
    root.destroy()
