import xmltodict
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from pypdevs.util import DEVSException

from livingLab.interactive.lightbulb import LightState
from livingLab.util.LuxCalculator import LuxCalculator
from livingLab.util.pipes import WINDOW_CONCEALMENT_PIPE, SUN_LUMINANCE_PIPE, WINDOW_LUMINANCE_PIPE


class WindowState:
    def __init__(self):
        self.concealment = 0.0 # 0..1
        self.window_luminance = 0.0
        self.state = "idle" # idle, updating

    def toXML(self):
        return xmltodict.unparse({
            "WindowState": {
                "concealment": self.concealment,
                "window_luminance": self.window_luminance,
                "state": self.state
            }
        })

class Window(AtomicDEVS):
    def __init__(self, name, positionX, positionY):
        AtomicDEVS.__init__(self, name)
        self.state = WindowState()
        self.positionX = positionX
        self.positionY = positionY

        # io
        self.out_luminance = self.addOutPort(name=WINDOW_LUMINANCE_PIPE)
        self.in_concealment = self.addInPort(name=WINDOW_CONCEALMENT_PIPE)
        self.in_sun_luminance = self.addInPort(name=SUN_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        if self.in_concealment in inputs:
            self.state.concealment = inputs[self.in_concealment][0]
        if self.in_sun_luminance in inputs:
            sunDni = inputs[self.in_sun_luminance][0]
            self.state.window_luminance = LuxCalculator.calculateWindowLumen(sunDni)
        self.state.state = "updating"
        return self.state

    def intTransition(self):
        state = self.state
        if state.state == "updating":
            state.state = "idle"
        return self.state

    def outputFnc(self):
        if self.state.state == "updating":
            luminance = self.state.window_luminance * (1-self.state.concealment)
            return {self.out_luminance: [LightState(self.positionX, self.positionY, luminance)]}
        return {}

    def timeAdvance(self):
        if self.state.state == "idle":
            return INFINITY
        if self.state.state == "updating":
            return 0
        raise DEVSException("Invalid state")