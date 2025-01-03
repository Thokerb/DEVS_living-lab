from pypdevs.DEVS import AtomicDEVS
from pypdevs.util import DEVSException

from livingLab.interactive.lightbulb import LightState
from livingLab.util.LuxCalculator import LuxCalculator
from livingLab.util.experiment_constants import MIN_LUX, MAX_LUX
from livingLab.util.pipes import ARTIFICIAL_LUMINANCE_PIPE, WINDOW_LUMINANCE_PIPE, \
    WINDOW_CONCEALMENT_PIPE, INTERACT_BLINDS, INTERACT_AL


class HumanState():
    def __init__(self):

        self.artificial_light_state = LightState(0, 0, 0)
        self.window_light_state = LightState(0, 0, 0)
        self.luminance = 0.0
        self.blinds_closed = False
        self.artificial_light_on = False
        self.current_time = 0.0
        self.startMorningWork = 8*60 # 8:00
        self.finishMorningWork = 12*60 # 12:00
        self.startAfternoonWork = 13*60 # 13:00
        self.finishAfternoonWork = 17*60 # 17:00


class Human(AtomicDEVS):
    def __init__(self, name, positionX, positionY):
        AtomicDEVS.__init__(self, name)
        self.state = HumanState()
        self.X = positionX
        self.Y = positionY

        self.out_blinds_activity = self.addOutPort(name=INTERACT_BLINDS)
        self.out_al_activity = self.addOutPort(name=INTERACT_AL)
        self.in_artificial_luminance = self.addInPort(name=ARTIFICIAL_LUMINANCE_PIPE)
        self.in_window_luminance = self.addInPort(name=WINDOW_LUMINANCE_PIPE)
        self.in_concealment = self.addInPort(name=WINDOW_CONCEALMENT_PIPE)

    def extTransition(self, inputs):
        self.state.current_time += self.elapsed

        if self.in_concealment in inputs:
            self.state.blinds_closed = inputs[self.in_concealment][0] == 1.0
        if self.in_artificial_luminance in inputs:
            self.state.artificial_light_on = inputs[self.in_artificial_luminance][0] > 0.0
            self.state.artificial_light_state = inputs[self.in_artificial_luminance][0]
        if self.in_window_luminance in inputs:
            window_luminance = inputs[self.in_window_luminance][0]
            self.state.window_light_state = window_luminance


        self.updateLuminance()


        return self.state


    def intTransition(self):
        self.updateLuminance()
        self.state.current_time += self.timeAdvance()
        # print time
        print("HumanAtomic: intTransition: %s" % self.state.current_time)
        return self.state

    def outputFnc(self):
        # print elapsed time
        action = "Idle"

        if self.inOffice():
            if self.state.luminance < MIN_LUX:
                action = "increaseLight"
            if self.state.luminance > MAX_LUX:
                action = "reduceLight"

        print("Next Action: %s" % action)

        if action == "increaseLight":
            if self.state.blinds_closed:
                return {self.out_blinds_activity: ["increaseLight"]}
            if not self.state.artificial_light_on:
                return {self.out_al_activity: ["increaseLight"]}
            raise DEVSException("HumanAtomic: increaseLight, but no action possible. Blinds: %s, AL: %s" % (self.state.blinds_closed, self.state.artificial_light_on))
        if action == "reduceLight":
            if self.state.artificial_light_on:
                return {self.out_al_activity: ["reduceLight"]}
            if not self.state:
                return {self.out_blinds_activity: ["reduceLight"]}
            raise DEVSException("HumanAtomic: reduceLight, but no action possible. Blinds: %s, AL: %s" % (self.state.blinds_closed, self.state.artificial_light_on))

        return {}


    def timeAdvance(self):
        return 1

    def updateLuminance(self):
        window_lux = LuxCalculator.calculateLux(self.state.window_light_state, self.X, self.Y)
        al_lux = LuxCalculator.calculateLux(self.state.artificial_light_state, self.X, self.Y)
        print("HumanAtomic: updateLuminance: al_lux: %s, window_lux: %s" % (al_lux, window_lux))

        self.state.luminance = al_lux + window_lux
        print("HumanAtomic: updateLuminance: %s" % self.state.luminance)

    def inOffice(self):
        timeOfDay = self.state.current_time % 1440
        isInMorningWork = self.state.startMorningWork <= timeOfDay <= self.state.finishMorningWork
        isInAfternoonWork = self.state.startAfternoonWork <= timeOfDay <= self.state.finishAfternoonWork
        return isInMorningWork or isInAfternoonWork
