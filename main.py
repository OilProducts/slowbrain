import random
from tqdm import tqdm

import utils
from utils import get_mnist_dataloaders
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


def add_brain_layer(brain, z_index, x_start, x_stop, y_start, y_stop, in_out=""):
    for y in range(y_start, y_stop):
        for x in range(x_start, x_stop):
            if in_out == "in":
                brain.add_neuron(Coordinate(x, y, z_index))
                brain.input_neurons.append(brain.neurons[Coordinate(x, y, z_index)])
            elif in_out == "out":
                brain.add_neuron(Coordinate(x, y, z_index))
                brain.output_neurons.append(brain.neurons[Coordinate(x, y, z_index)])
            else:
                brain.add_neuron(Coordinate(x, y, z_index))
    return brain


def dimensional_brain():
    brain = Brain()
    add_brain_layer(brain, 0, 0, 28, 0, 28, in_out="in")
    add_brain_layer(brain, 1, 2, 26, 2, 26)
    add_brain_layer(brain, 2, 4, 24, 4, 24)
    add_brain_layer(brain, 3, 6, 22, 6, 22)
    add_brain_layer(brain, 4, 8, 20, 8, 20, in_out="out")
    # add_brain_layer(brain, 5, 10, 18, 10, 18, in_out="out")

    print("Connecting neurons...")
    for neuron in brain.neurons.values():
        for x in range(neuron.coordinate.x - 2, neuron.coordinate.x + 2):
            for y in range(neuron.coordinate.y - 2, neuron.coordinate.y + 2):
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
    train_loader, test_loader = utils.get_mnist_dataloaders(shrink_factor=10, batch_size=1, shuffle=True, num_workers=0)

    progress_bar = tqdm(train_loader, total=len(train_loader))
    for t in range(50):
        for neuron in brain.input_neurons:
            if random.random() < 0.9:
                neuron.spike()
        brain.tick()
        print(f"Tick: {t}")
        # print([int(neuron.output) for neuron in brain.input_neurons])
        # print([int(neuron.output) for neuron in brain.output_neurons])


if __name__ == '__main__':
    main()
