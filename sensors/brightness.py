import xmltodict
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY
from pypdevs.util import DEVSException

from livingLab.interactive.lightbulb import LightState
from livingLab.util.LuxCalculator import LuxCalculator
from livingLab.util.pipes import WINDOW_LUMINANCE_PIPE, ARTIFICIAL_LUMINANCE_PIPE


class BrightnessState:
    def __init__(self):
        self.time = 0
        self.state = "idle" # idle
        self.luminance = 0.0
        self.window_light_state = LightState(0,0,0)
        self.artificial_light_state = LightState(0,0,0)

    def toXML(self):
        return xmltodict.unparse({
            "BrightnessState": {
                "luminance": self.luminance,
                "time": self.time,
            }
        })


class BrightnessSensor(AtomicDEVS):
    def __init__(self, name, positionX, positionY):
        AtomicDEVS.__init__(self, name)
        self.state = BrightnessState()
        self.positionX = positionX
        self.positionY = positionY

        # io
        self.in_window_luminance = self.addInPort(name=WINDOW_LUMINANCE_PIPE)
        self.in_artificial_luminance = self.addInPort(name=ARTIFICIAL_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        if self.in_window_luminance in inputs:
            self.state.window_light_state = inputs[self.in_window_luminance][0]
        if self.in_artificial_luminance in inputs:
            self.state.artificial_light_state = inputs[self.in_artificial_luminance][0]

        self.state.luminance = (
            LuxCalculator.calculateLux(self.state.window_light_state,self.positionX, self.positionY) +
            LuxCalculator.calculateLux(self.state.artificial_light_state,self.positionX, self.positionY)
        )
        return self.state

    def intTransition(self):
        self.state.time += self.timeAdvance()
        return self.state

    def outputFnc(self):
        return {}

    def timeAdvance(self):
        return 1
