import xmltodict
from pypdevs.DEVS import AtomicDEVS
from pypdevs.infinity import INFINITY

from livingLab.generators.data_gen import simulate_dni
from livingLab.util.experiment_constants import SUNRISE, SUNSET
from livingLab.util.pipes import SUN_LUMINANCE_PIPE

class SunState:
    def __init__(self):
        self.dni = simulate_dni(SUNRISE, SUNSET)
        self.elapsed = 0

    def toXML(self):
        return xmltodict.unparse({"SunState": {
            "dni": self.dni,
            "elapsed": self.elapsed
        }})


class Sun(AtomicDEVS):
    def __init__(self, name):
        AtomicDEVS.__init__(self, name)

        self.state = SunState()
        self.out_luminance = self.addOutPort(name=SUN_LUMINANCE_PIPE)

    def extTransition(self, inputs):
        state = self.state
        return state

    def intTransition(self):
        self.state.elapsed += self.timeAdvance()
        return self.state

    def outputFnc(self):
        minuteOfDay = self.state.elapsed % 1440 # 24 * 60
        return {self.out_luminance: [self.state.dni[minuteOfDay]]}

    def timeAdvance(self):
        return 1