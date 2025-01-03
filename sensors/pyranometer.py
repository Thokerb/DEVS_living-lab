from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.util.pipes import SUN_LUMINANCE_PIPE


class PyranometerSensor(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = "todo" # night, day

        self.in_sun_luminance = self.addInPort(name=SUN_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        lastInput = inputs[self.inport][0]
        state = self.state
        return state

    def intTransition(self):
        return self.state

    def outputFnc(self):
        return {}

    def timeAdvance(self):
        return INFINITY