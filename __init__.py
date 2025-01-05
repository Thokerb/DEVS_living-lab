from pypdevs.simulator import Simulator

from livingLab.lab.room import Room
from livingLab.report import runReport
from livingLab.tracing.customTracer import TracerCustom

# create model
model = Room("living-lab")
# create simulator
sim = Simulator(model)
# classic DEVS simulation
sim.setClassicDEVS()

# Enable Tracing
sim.setVerbose(None)
# terminate after 30 time units
sim.setTerminationTime(24*60)
#sim.setXML("trace.xml")
sim.setCustomTracer("livingLab.tracing.customTracer","TracerCustom",["trace.xml"])
# run simulation
sim.simulate()
runReport()