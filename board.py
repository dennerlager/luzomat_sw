from gpio import Input, Output

class Board:
    def __init__(self):
        self.coffeeButton = Input(10)
        self.teaButton = Input(8)
        self.coinSlotRx = Input(13)
        self.coinSlotTx = Output(15)
        self.led1 = Output(22)
        self.led2 = Output(18)
        self.schnapsTop = Output(36)
        self.schnapsBottom = Output(35)
        self.water = Output(38)
        self.air = Output(37)

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

    def turnCoinSlotTxOn(self):
        self.coinSlotTx.set()

    def turnCoinSlotTxOff(self):
        self.coinSlotTx.clear()

    def isPaid(self):
        self.turnCoinSlotTxOn()
        isPaid = self.coinSlotRx.read()
        self.turnCoinSlotTxOff()
        return isPaid

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

    print('is paid')
    print(board.isPaid())
    input('paid')
    print(board.isPaid())
