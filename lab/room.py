from pypdevs.DEVS import CoupledDEVS

from livingLab.generators.human import Human
from livingLab.generators.sun import Sun
from livingLab.interactive.blinds import Blinds
from livingLab.interactive.lightbulb import ArtificialLight
from livingLab.queues.window import Window
from livingLab.sensors.brightness import BrightnessSensor
from livingLab.sensors.pyranometer import PyranometerSensor


class Room(CoupledDEVS):
    def __init__(self, name):
        CoupledDEVS.__init__(self, name)
        self.human = self.addSubModel(Human("human",100,300))
        self.artificialLight = self.addSubModel(ArtificialLight("artificialLight",200,200, 700))
        self.blinds = self.addSubModel(Blinds("blinds"))
        self.brightnessSensor = self.addSubModel(BrightnessSensor("brightnessSensor1"))
        self.window = self.addSubModel(Window("window"))
        self.sun = self.addSubModel(Sun("sun"))
        self.pyranometerSensor = self.addSubModel(PyranometerSensor("pyranometerSensor"))

        # connect submodels
        # window luminance
        self.connectPorts(self.window.out_luminance, self.brightnessSensor.in_window_luminance)
        self.connectPorts(self.window.out_luminance, self.human.in_window_luminance)
        # artificial luminance
        self.connectPorts(self.artificialLight.out_luminance, self.brightnessSensor.in_artificial_luminance)
        self.connectPorts(self.artificialLight.out_luminance, self.human.in_artificial_luminance)
        # sun luminance
        self.connectPorts(self.sun.out_luminance, self.pyranometerSensor.in_sun_luminance)
        self.connectPorts(self.sun.out_luminance, self.window.in_sun_luminance)
        # window concealment
        self.connectPorts(self.blinds.out_concealment, self.window.in_concealment)
        self.connectPorts(self.blinds.out_concealment, self.human.in_concealment)
        # human activity
        self.connectPorts(self.human.out_al_activity, self.artificialLight.in_activity)
        self.connectPorts(self.human.out_blinds_activity, self.blinds.in_activity)

