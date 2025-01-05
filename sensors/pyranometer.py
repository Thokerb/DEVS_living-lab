import xmltodict
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.util.pipes import SUN_LUMINANCE_PIPE


class PyranometerState:
    def __init__(self):
        self.state = "todo" # night, day

    def toXML(self):
        return xmltodict.unparse({
            "PyranometerState": {
                "state": self.state
            }
        })


class PyranometerSensor(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = PyranometerState()

        self.in_sun_luminance = self.addInPort(name=SUN_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        lastInput = inputs[self.in_sun_luminance][0]
        state = self.state
        return state

    def intTransition(self):
        return self.state

    def outputFnc(self):
        return {}

    def timeAdvance(self):
        return INFINITY