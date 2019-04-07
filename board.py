import time
from gpio import Input, Output

class Board:
    def __init__(self):
        self.coffeeButton = Input(10)
        self.teaButton = Input(8)
        self.coinSlotRx = Input(13)
        self.coinSlotTx = Output(15)
        self.coinMotor = Output(40)
        self.led1 = Output(22)
        self.led2 = Output(18)
        self.schnapsTop = Output(36)
        self.schnapsBottom = Output(35)
        self.water = Output(38)
        self.air = Output(37)
        self.teaButtonLastState = self.isTeaButtonPressed()
        self.coinLastState = self.isCoinPresent()

    def getCurrentState(self):
        return {'tea button': self.isTeaButtonPressed(),
                'luz button': self.isCoffeeButtonPressed(),
                'coin present': self.isCoinPresent(),
                'coin motor': self.coinMotor.read(),
                'led 1': self.led1.read(),
                'led 2': self.led2.read(),
                'schnaps top': self.schnapsTop.read(),
                'schnaps bottom': self.schnapsBottom.read(),
                'water': self.water.read(),
                'air': self.air.read()}

    def openAirValve(self):
        self.air.set()

    def closeAirValve(self):
        self.air.clear()

    def openWaterValve(self):
        self.water.set()

    def closeWaterValve(self):
        self.water.clear()

    def openUpperSchnapsValve(self):
        self.schnapsTop.set()

    def closeUpperSchnapsValve(self):
        self.schnapsTop.clear()

    def openLowerSchnapsValve(self):
        self.schnapsBottom.set()

    def closeLowerSchnapsValve(self):
        self.schnapsBottom.clear()

    def turnLed1On(self):
        self.led1.set()

    def turnLed1Off(self):
        self.led1.clear()

    def turnLed2On(self):
        self.led2.set()

    def turnLed2Off(self):
        self.led2.clear()

    def isCoffeeButtonPressed(self):
        return self.coffeeButton.read()

    def isTeaButtonPressed(self):
        return self.teaButton.read()

    def wasTeaButtonPressed(self):
        if ((not self.teaButtonLastState) and
            self.isTeaButtonPressed()):
            self.teaButtonLastState = True
            return True
        else:
            return False

    def wasTeaButtonReleased(self):
        if (self.teaButtonLastState and
            (not self.isTeaButtonPressed())):
            self.teaButtonLastState = False
            return True
        else:
            return False

    def isPaid(self):
        if ((not self.coinLastState) and
            self.isCoinPresent()):
            self.coinLastState = True
            return True
        else:
            return False

    def isCoinPresent(self):
        self.turnCoinSlotTxOn()
        isCoinPresent = self.coinSlotRx.read()
        self.turnCoinSlotTxOff()
        return isCoinPresent

    def turnCoinSlotTxOn(self):
        self.coinSlotTx.set()

    def turnCoinSlotTxOff(self):
        self.coinSlotTx.clear()

    def dropCoin(self):
        self.coinMotor.set()
        time.sleep(1)
        self.coinMotor.clear()
        self.coinLastState = False

if __name__ == '__main__':
    board = Board()

    input('air valve ')
    board.openAirValve()
    input('close ')
    board.closeAirValve()

    input('water valve ')
    board.openWaterValve()
    input('close ')
    board.closeWaterValve()

    input('upper schnaps valve ')
    board.openUpperSchnapsValve()
    input('close ')
    board.closeUpperSchnapsValve()

    input('lower schnaps valve ')
    board.openLowerSchnapsValve()
    input('close ')
    board.closeLowerSchnapsValve()

    input('drop coin')
    board.dropCoin()

    input('led1 ')
    board.turnLed1On()
    input('turn off ')
    board.turnLed1Off()

    input('led2 ')
    board.turnLed2On()
    input('turn off ')
    board.turnLed2Off()

    input('coin slot tx ')
    board.turnCoinSlotTxOn()
    input('turn off ')
    board.turnCoinSlotTxOff()

    print('coffee botton:')
    print(board.isCoffeeButtonPressed())
    input('pressed? ')
    print(board.isCoffeeButtonPressed())

    print('tea botton:')
    print(board.isTeaButtonPressed())
    input('pressed? ')
    print(board.isTeaButtonPressed())

    print('is coin present')
    print(board.isCoinPresent())
    input('present')
    print(board.isCoinPresent())
