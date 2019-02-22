import abc
import time

class Luzomat:
    def __init__(self):
        self.currentState = IdleState()

    def coffeeButton(self):
        self.currentState.coffeeButton(self)

    def teaButtonPushed(self):
        self.currentState.teaButtonPushed(self)

    def teaButtonReleased(self):
        self.currentState.teaButtonReleased(self)

    def coin(self):
        self.currentState.coin(self)

    def changeState(self, newState):
        self.currentState = newState

class State(abc.ABC):
    @abc.abstractmethod
    def coffeeButton(self, luzomat):
        pass

    @abc.abstractmethod
    def teaButtonPushed(self, luzomat):
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

    def teaButtonPushed(self, luzomat):
        luzomat.openAirValve()
        luzomat.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.closeWaterValve()
        luzomat.closeAirValve()

    def coin(self, luzomat):
        self.changeState(luzomat, CoinAccepted())

class CoinAccepted(State):
    def coffeeButton(self, luzomat):
        luzomat.openAirValve()
        luzomat.openWaterValve()
        luzomat.closeUpperSchnapsValve()
        luzomat.openLowerSchnapsValve()
        time.sleep(3)
        luzomat.closeWaterValve()
        luzomat.closerLowerSchnapsValve()
        luzomat.openUpperSchnapsValve()
        self.changeState(luzomat, IdleState())

    def teaButtonPushed(self, luzomat):
        luzomat.openAirValve()
        luzomat.openWaterValve()

    def teaButtonReleased(self, luzomat):
        luzomat.closeWaterValve()
        luzomat.closeAirValve()

    def coin(self, luzomat):
        pass
