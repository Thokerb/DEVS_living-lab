from pypdevs.simulator import Simulator

from livingLab.lab.room import Room

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
# run simulation
sim.simulate()
