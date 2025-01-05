import xmltodict
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

    def toXML(self):
        return xmltodict.unparse({
            "LightState": {
                "positionX": self.positionX,
                "positionY": self.positionY,
                "luminance_output": self.luminance_output
            }
        })


class ArtificialLightState:
    def __init__(self):
        self.state = "off" # off, on, switchingOn, switchingOff


    def toXML(self):
        return xmltodict.unparse({
            "ArtificialLightState": {
                "state": self.state,
            }
        })

class ArtificialLight(AtomicDEVS):
    def __init__(self, name, positionX, positionY, luminance):
        self.positionX = positionX
        self.positionY = positionY
        self.luminance = luminance
        AtomicDEVS.__init__(self, name)
        self.state = ArtificialLightState()


        self.in_activity = self.addInPort(name=INTERACT_AL)
        self.out_luminance = self.addOutPort(name=ARTIFICIAL_LUMINANCE_PIPE)

    def intTransition(self):
        state = self.state.state
        if state == "switchingOn":
            self.state.state = "on"
        elif state == "switchingOff":
            self.state.state = "off"
        return self.state

    def extTransition(self, inputs):
        # there is only one input
        lastInput = inputs[self.in_activity][0]
        state = self.state.state
        if state == "off" and lastInput == "increaseLight":
            self.state.state = "switchingOn"
        elif state == "on" and lastInput == "reduceLight":
            self.state.state = "switchingOff"
        return self.state

    def outputFnc(self):
        state = self.state.state
        if state == "switchingOn":
            return {self.out_luminance: [LightState(self.positionX, self.positionY, self.luminance)]}
        if state == "switchingOff":
            return {self.out_luminance: [LightState(self.positionX, self.positionY, 0)]}
        raise DEVSException("Unknown state")

    def timeAdvance(self):
        if self.state.state == "off":
            return INFINITY
        if self.state.state == "on":
            return INFINITY
        if self.state.state == "switchingOn":
            return 0
        if self.state.state == "switchingOff":
            return 0
        raise DEVSException("Unknown state")