from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.util.pipes import WINDOW_CONCEALMENT_PIPE, SUN_LUMINANCE_PIPE, WINDOW_LUMINANCE_PIPE


class Window(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)
        self.state = "todo" # night, day

        # io
        self.in_concealment = self.addInPort(name=WINDOW_CONCEALMENT_PIPE)
        self.in_sun_luminance = self.addInPort(name=SUN_LUMINANCE_PIPE)
        self.out_luminance = self.addOutPort(name=WINDOW_LUMINANCE_PIPE)

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