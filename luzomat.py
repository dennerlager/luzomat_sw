import abc
import time
from board import Board
from boiler import Boiler
from counter import Counter
from air_valve import AirValve

class Luzomat:
    def __init__(self):
        self.currentState = IdleState()
        self.boiler = Boiler()
        self.boiler.setTemperatureC(95)
        self.airValve = AirValve()
        self.board = Board()
        self.luzcounter = Counter('luz')

    def getTemperatures(self):
        return self.boiler.getTemperatures()

    def getCurrentState(self):
        currentState = {'current state': self.currentState,
                        'luz counter': self.luzcounter.getCount()}
        currentState.update(self.board.getCurrentState())
        return currentState

    def coffeeButton(self):
        self.currentState.coffeeButton(self)

    def teaButtonPressed(self):
        self.currentState.teaButtonPressed(self)

    def teaButtonReleased(self):
        self.currentState.teaButtonReleased(self)

    def coin(self):
        self.currentState.coin(self)

    def changeState(self, newState):
        self.currentState = newState

    def shutdown(self):
        self.boiler.shutdown()
        self.airValve.shutdown()

    def increaseLuzCounter(self):
        self.luzcounter.increase()

    def mainloop(self):
        try:
            while True:
                if self.board.isCoffeeButtonPressed():
                    self.coffeeButton()
                if self.board.wasTeaButtonPressed():
                    self.teaButtonPressed()
                if self.board.wasTeaButtonReleased():
                    self.teaButtonReleased()
                if self.board.isCoinPresent():
                    self.coin()
        finally:
            self.shutdown()

class State(abc.ABC):
    @abc.abstractmethod
    def coffeeButton(self, luzomat):
        pass

    @abc.abstractmethod
    def teaButtonPressed(self, luzomat):
        pass

    @abc.abstractmethod
    def teaButtonReleased(self, luzomat):
        pass

    @abc.abstractmethod
    def coin(self, luzomat):
        pass

    def changeState(self, luzomat, newState):
        luzomat.changeState(newState)

class IdleState(State):
    def coffeeButton(self, luzomat):
        pass

    def teaButtonPressed(self, luzomat):
        luzomat.airValve.open()
        luzomat.board.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.board.closeWaterValve()

    def coin(self, luzomat):
        luzomat.board.turnLedReadyOn()
        self.changeState(luzomat, CoinAccepted())

class CoinAccepted(State):
    def coffeeButton(self, luzomat):
        luzomat.increaseLuzCounter()
        luzomat.airValve.open()
        luzomat.board.closeUpperSchnapsValve()
        luzomat.board.openLowerSchnapsValve()
        time.sleep(7)
        luzomat.board.openWaterValve()
        time.sleep(6)
        luzomat.board.closeWaterValve()
        luzomat.board.closeLowerSchnapsValve()
        luzomat.board.openUpperSchnapsValve()
        luzomat.board.turnLedReadyOff()
        self.changeState(luzomat, IdleState())

    def teaButtonPressed(self, luzomat):
        luzomat.airValve.open()
        luzomat.board.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.board.closeWaterValve()

    def coin(self, luzomat):
        pass

if __name__ == '__main__':
    luzomat = Luzomat()
    luzomat.mainloop()
