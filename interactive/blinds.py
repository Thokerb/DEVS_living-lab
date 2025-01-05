import xmltodict
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.util.devs_constants import OMEGA
from livingLab.util.pipes import WINDOW_CONCEALMENT_PIPE, INTERACT_BLINDS

class BlindsState:
    def __init__(self):
        self.concealment = 0.0 # 0..1
        self.state = "halt" # moveUp, moveDown, Halt

    def toXML(self):
        return xmltodict.unparse({"BlindsState": {
            "concealment": self.concealment,
            "state": self.state
        }})

class Blinds(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = BlindsState()
        self.concealmentChange = 0.1

        # i/o ports
        self.out_concealment = self.addOutPort(WINDOW_CONCEALMENT_PIPE)
        self.in_activity = self.addInPort(INTERACT_BLINDS)


    def extTransition(self, inputs):
        lastInput = inputs[self.in_activity][0]
        state = self.state
        if lastInput == "increaseLight":
            self.state = "moveUp"
        if lastInput == "reduceLight":
            self.state = "moveDown"
        if lastInput == "halt":
            self.state = "halt"
        return state

    def intTransition(self):
        state = self.state.state
        if state == "moveUp":
            self.state.concealment += self.concealmentChange
            if self.state.concealment >= 1.0:
                self.state.state = "halt"
                self.state.concealment = 1.0
        if state == "moveDown":
            self.state.concealment -= self.concealmentChange
            if self.state.concealment <= 0.0:
                self.state.state = "halt"
                self.state.concealment = 0.0
        return self.state

    def outputFnc(self):
        return {self.out_concealment: [self.state.concealment]}

    def timeAdvance(self):
        state = self.state.state
        if state == "halt":
            return INFINITY
        if state == "moveUp":
            return OMEGA
        if state == "moveDown":
            return OMEGA