"""
A slow object-oriented implementation of spiking neural networks.
"""
import math
from collections import namedtuple



Coordinate = namedtuple("Coordinate", "x y z")

class Axon:
    def __init__(self):
        self.target_dendrite = None
        self.trace = 0
        self.stored_transmitter = 0
        self.gap_transmitter = 0

    def __str__(self):
        return f"Axon(target_dendrite_coordinate={self.target_dendrite_coordinate}, trace={self.trace}, stored_transmitter={self.stored_transmitter}, synaptic_transmitter={self.synaptic_transmitter})"


    def produce(self):
        """Produces a signal."""
        self.trace = 0
        self.target_dendrite.signal()
        self.gap_transmitter += self.stored_transmitter


    def tick(self):
        """Updates the axon's state."""
        self.trace += 1
        self.gap_transmitter *= 0.93
        self.stored_transmitter = min(self.stored_transmitter + .05, 1)


class Dendrite:
    def __init__(self):
        self.trace = 0
        self.value = 0.0

    def signal(self, value):
        self.value = value


class Synapse:
    def __init__(self, weight=0.05):
        self.weight = weight
        self.axon_trace = 0
        self.dendrite_trace = 0
        self.value = 0.0
        self.last_stimulus = -math.inf
        self.ISI_threshold = 20
        self.ISI_trace = 0

    def __str__(self):
        return f"Synapse(weight={self.weight}, axon_trace={self.axon_trace}, dendrite_trace={self.dendrite_trace}, value={self.value})"

    def produce(self):
        """Produces a signal."""
        self.value = self.weight
        self.axon_trace = 0

    def consume(self):
        """Consumes a signal."""
        self.dendrite_trace = 0
        self.value = 0.0

    def tick(self):
        """Updates the synapse's state."""
        self.axon_trace += 1
        self.dendrite_trace += 1
        self.ISI_trace += 1
        # if self.axon_trace > 10:
        #     self.value = 0.0
        # if self.dendrite_trace > 10:
        #     self.value = 0.0


class Neuron:
    def __init__(self, coordinate, threshold=1.0, leak=0.99):
        self.coordinate = coordinate
        self.threshold = threshold
        self.leak = leak
        self.potential = 0.0
        self.trace = 0
        self.dendrites = []
        self.axons = []

    def __str__(self):
        return f"Neuron(potential={self.potential}, output={self.output})"

    def add_dendritic_connection(self, synapse):
        """Connects a dendrite to the axon of another neuron."""
        self.dendrites.append(synapse)

    def add_axonic_connection(self, synapse):
        """Connects an axon to the dendrite of another neuron."""
        self.axons.append(synapse)

    def spike(self):
        # print(f"Neuron {self.coordinate} spiked!")
        for synapse in self.axons:
            synapse.produce()
        self.potential = 0.0
        self.trace = 0


    def tick(self):
        """Updates the neuron's state."""
        for synapse in self.dendrites:
            self.potential += synapse.value
            synapse.consume()
        if self.potential >= self.threshold:
            self.spike()
        else:
            self.potential *= self.leak
            self.trace += 1

class Brain:
    def __init__(self):
        self.neurons = {}
        self.synapses = []
        self.input_neurons = []
        self.output_neurons = []

    def __str__(self):
        return f"Brain(neurons={[str(neuron) for neuron in self.neurons]}, synapses={self.synapses})"

    def connect(self, neuron_one, neuron_two):
        """Connects two neurons together. neuron_one will have a dendrite connected to neuron_two's
         axon."""
        synapse = Synapse()
        neuron_one.add_axonic_connection(synapse)
        neuron_two.add_dendritic_connection(synapse)
        self.add_synapse(synapse)

    def add_neuron(self, coordinate):
        self.neurons[coordinate] = Neuron(coordinate)

    def add_synapse(self, synapse):
        self.synapses.append(synapse)

    def tick(self):
        for neuron in self.neurons.values():
            neuron.tick()
        for synapse in self.synapses:
            synapse.tick()