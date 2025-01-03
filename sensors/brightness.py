from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.util.pipes import WINDOW_LUMINANCE_PIPE, ARTIFICIAL_LUMINANCE_PIPE


class BrightnessSensor(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = "todo" # night, day

        # io
        self.in_window_luminance = self.addInPort(name=WINDOW_LUMINANCE_PIPE)
        self.in_artificial_luminance = self.addInPort(name=ARTIFICIAL_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        lastInput = inputs[self.in_artificial_luminance][0]
        state = self.state
        return state

    def intTransition(self):
        return self.state

    def outputFnc(self):
        return {}

    def timeAdvance(self):
        return INFINITY