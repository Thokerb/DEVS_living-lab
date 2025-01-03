from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from pypdevs.util import DEVSException

from livingLab.util.pipes import INTERACT_AL, ARTIFICIAL_LUMINANCE_PIPE


# for simplicity, we assume that the light is a point light source even for windows
class LightState:
    def __init__(self, positionX, positionY, luminance_output):
        self.positionX = positionX
        self.positionY = positionY
        self.luminance_output = luminance_output


class ArtificialLight(AtomicDEVS):
    def __init__(self, name, positionX, positionY, luminance):
        self.positionX = positionX
        self.positionY = positionY
        self.luminance = luminance
        AtomicDEVS.__init__(self, name)
        self.state = "off" # off, on


        self.in_activity = self.addInPort(name=INTERACT_AL)
        self.out_luminance = self.addOutPort(name=ARTIFICIAL_LUMINANCE_PIPE)

    def intTransition(self):
        return self.state

    def extTransition(self, inputs):
        # there is only one input
        lastInput = inputs[self.in_activity][0]
        state = self.state
        if state == "off" and lastInput == "increaseLight":
            return "on"
        if state == "on" and lastInput == "reduceLight":
            return "off"
        return state

    def outputFnc(self):
        if self.state == "on":
            return {self.out_luminance: [LightState(self.positionX, self.positionY, self.luminance)]}
        if self.state == "off":
            return {self.out_luminance: [LightState(self.positionX, self.positionY, 0)]}
        raise DEVSException("Unknown state")

    def timeAdvance(self):
        if self.state == "off":
            return INFINITY
        if self.state == "on":
            return 1