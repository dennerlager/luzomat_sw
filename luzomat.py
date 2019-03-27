import abc
import time
from board import Board
from boiler import Boiler

class Luzomat:
    def __init__(self):
        self.currentState = IdleState()
        self.boiler = Boiler()
        self.boiler.setTemperatureC(95)
        self.board = Board()

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

    def mainloop(self):
        try:
            while True:
                if self.board.isCoffeeButtonPressed():
                    self.coffeeButton()
                if self.board.wasTeaButtonPressed():
                    self.teaButtonPressed()
                if self.board.wasTeaButtonReleased():
                    self.teaButtonReleased()
                if self.board.isPaid():
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
        luzomat.board.openAirValve()
        luzomat.board.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.board.closeWaterValve()
        luzomat.board.closeAirValve()

    def coin(self, luzomat):
        self.changeState(luzomat, CoinAccepted())

class CoinAccepted(State):
    def coffeeButton(self, luzomat):
        luzomat.board.openAirValve()
        luzomat.board.dropCoin()
        luzomat.board.openWaterValve()
        luzomat.board.closeUpperSchnapsValve()
        luzomat.board.openLowerSchnapsValve()
        time.sleep(3)
        luzomat.board.closeWaterValve()
        luzomat.board.closerLowerSchnapsValve()
        luzomat.board.openUpperSchnapsValve()
        self.changeState(luzomat, IdleState())

    def teaButtonPressed(self, luzomat):
        luzomat.board.openAirValve()
        luzomat.board.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.board.closeWaterValve()
        luzomat.board.closeAirValve()

    def coin(self, luzomat):
        pass

if __name__ == '__main__':
    luzomat = Luzomat()
    luzomat.mainloop()
