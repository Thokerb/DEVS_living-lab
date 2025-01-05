class TracerCustom(object):
    def __init__(self, uid, server, filename):
        """
        Both uid and server can be ignored, as these are only required for distributed simulation
        filename contains the name of the file in which we should write the trace
        """
        # create xml file
        self.file = None
        self.filename = filename

    def startTracer(self, recover):
        """
        Recover is a boolean representing whether or not this is a recovered call (e.g., should the file be overwritten or appended to?)
        """
        self.file = open(self.filename, "w")
        self.file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        self.file.write("<trace>\n")


    def stopTracer(self):
        """
        Stops the tracer (e.g., flush the file)
        """
        self.file.write("</trace>\n")
        self.file.close()
        pass

    def traceInternal(self, aDEVS):
        # check if adevs is Human
        if aDEVS.state.__class__.__name__ in ["HumanState","BrightnessState"]  and aDEVS.state.toXML:
            trace = aDEVS.state.toXML()
            if trace:
                self.file.write(trace)
                self.file.write("\n")


        """
        Called for each atomic DEVS model that does an internal transition.
        """
    def traceExternal(self, aDEVS):
        """
        Called for each atomic DEVS model that does an external transition.
        """
        pass

    def traceConfluent(self, aDEVS):
        """
        Called for each atomic DEVS model that does a confluent transition.
        """
        pass

    def traceInit(self, aDEVS, t):
        """
        Called upon initialization of a model.
        The parameter *t* contains the time at which the model commences (likely 0).
        """
        pass

    def traceUser(self, time, aDEVS, variable, value):
        """
        Called upon so called *god events* during debuggin, where a user manually alters the state of an atomic DEVS instance.
        """
        pass