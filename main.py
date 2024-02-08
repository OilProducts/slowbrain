import random

from components import Neuron, Synapse, Coordinate, Brain


def simple_brain():
    brain = Brain()
    brain.add_neuron(Coordinate(0, 0, 0))
    brain.add_neuron(Coordinate(1, 0, 0))
    brain.add_neuron(Coordinate(2, 0, 0))
    brain.connect(brain.neurons[Coordinate(0, 0, 0)], brain.neurons[Coordinate(1, 0, 0)])
    brain.connect(brain.neurons[Coordinate(1, 0, 0)], brain.neurons[Coordinate(2, 0, 0)])
    brain.input_neurons.append(brain.neurons[Coordinate(0, 0, 0)])
    brain.output_neurons.append(brain.neurons[Coordinate(2, 0, 0)])
    return brain


def dimensional_brain():
    brain = Brain()
    for z in range(10):
        for y in range(10):
            for x in range(10):
                brain.add_neuron(Coordinate(x, y, z))
                if z == 4:
                    brain.output_neurons.append(brain.neurons[Coordinate(x, y, z)])
                if z == 0:
                    brain.input_neurons.append(brain.neurons[Coordinate(x, y, z)])

    print("Connecting neurons...")
    for neuron in brain.neurons.values():
        for x in range(neuron.coordinate.x - 1, neuron.coordinate.x + 2):
            for y in range(neuron.coordinate.y - 1, neuron.coordinate.y + 2):
                for z in range(neuron.coordinate.z - 1, neuron.coordinate.z + 2):
                    if Coordinate(x, y, z) in brain.neurons:
                        brain.connect(neuron, brain.neurons[Coordinate(x, y, z)])

    print("Done connecting neurons.")
    print(f"Number of synapses: {len(brain.synapses)}")
    print("Number of neurons: ", len(brain.neurons))
    print("Number of input neurons: ", len(brain.input_neurons))
    print("Number of output neurons: ", len(brain.output_neurons))
    return brain


def main():
    brain = dimensional_brain()
    print("Running brain...")
    for t in range(5000):
        for neuron in brain.input_neurons:
            if random.random() < 0.5:
                neuron.spike()
        brain.tick()
        for z in range(10):
            layer = []
            for y in range(10):
                for x in range(10):
                    layer.append(brain.neurons[Coordinate(x, y, z)].potential)
            print(['%.2f' % elem for elem in layer])
        print(f"Tick: {t}")
        # print([int(neuron.output) for neuron in brain.input_neurons])
        # print([int(neuron.output) for neuron in brain.output_neurons])


if __name__ == '__main__':
    main()
