# Bank, 1 clerk.py
import salabim as sim


class PlacasGenerator(sim.Component):
    def process(self):
        while True:
            Placa()
            yield self.hold(sim.Uniform(5, 15).sample())


class RodaGenerator(sim.Component):
    def process(self):
        while True:
            Roda()
            yield self.hold(sim.Uniform(5, 15).sample())

# Etapas da placa


class Placa(sim.Component):
    def process(self):
        self.enter(waitingline)
        for pressing in pressings:
            if pressing.ispassive():
                pressing.activate()

        for cutting in cuttings:
            if cutting.ispassive():
                pressing.activate()

        if finishing.ispassive:
            finishing.activate

        if painting.ispassive():
            painting.activate()

        yield self.passivate()


class Pressing(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                yield self.passivate()
            self.placa = waitingline.pop()
            yield self.hold(100)
            self.placa.activate()


class Cutting(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                yield self.passivate()
            self.placa = waitingline.pop()
            yield self.hold(60)
            self.placa.activate()


class Finishing(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                yield self.passivate()
            self.placa = waitingline.pop()
            yield self.hold(15)
            self.placa.activate()


class Painting(sim.Component):
    def process(self):
        while True:
            while len(waitingline) == 0:
                yield self.passivate()
            self.placa = waitingline.pop()
            yield self.hold(20)
            self.placa.activate()


# Etapas da roda
class Roda(sim.Component):
    def process(self):
        self.enter(waitingline)
        if foundry.ispassive():
            foundry.activate
        for machine in machining:
            if machine.ispassive():
                machine.activate()
        if printing.ispassive():
            printing.activate()

        yield self.passivate()


class Foundry(sim.Component):
    def process(self):
        while True:
            while len(waitingline_roda) == 0:
                yield self.passivate()
            self.roda = waitingline_roda.pop()
            yield self.hold(55)
            self.roda.activate()


class Machining(sim.Component):
    def process(self):
        while True:
            while len(waitingline_roda) == 0:
                yield self.passivate()
            self.roda = waitingline_roda.pop()
            yield self.hold(60)
            self.roda.activate()


class Printing(sim.Component):
    def process(self):
        while True:
            while len(waitingline_roda) == 0:
                yield self.passivate()
            self.roda = waitingline_roda.pop()
            yield self.hold(20)
            self.roda.activate()


env = sim.Environment(trace=True)
PlacasGenerator()
RodaGenerator()

foundry = Foundry()
machining = [Machining() for _ in range(2)]
printing = Printing()
pressings = [Pressing() for _ in range(4)]
cuttings = [Cutting() for _ in range(3)]
painting = Painting()
finishing = Finishing()
waitingline = sim.Queue("waitingline")
waitingline_roda = sim.Queue("waitingline")

env.run(till=50)
print()
waitingline.print_statistics()
