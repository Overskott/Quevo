import math
import random
from typing import Union, Any

from qiskit import *


class CircuitString(list):

    def __init__(self):
        super().__init__()
        self.theta_list = []

    def check_duplicate_qubit_assignment(self):
        for i in range(0, int(len(self)/3)):
            int_index = i * 3

            if ((self[int_index] in [0, 4, 5]) and
                    self[int_index + 1] == self[int_index + 2]):

                if self[int_index + 1] == 0:
                    self[int_index + 1] = random.randrange(1, 3)

                elif self[int_index + 1] == 1:
                    self[int_index + 2] = 0  # TODO - hardcoded

                elif self[int_index + 1] == 2:
                    self[int_index + 2] = random.randrange(0, 2)

    def generate_gate_string(self, length):
        # Returns a randomly generated string representation of given number of qbits

        for i in range(length):
            if i % 3 == 0:
                self.append(random.randrange(0, 6))
            else:
                self.append(random.randrange(0, 3))

        self.check_duplicate_qubit_assignment()

        return self

    def mutate_gate_string(self):

        random_index = random.randrange(0, int(len(self)/3)) * 3

        self[random_index] = random.randrange(0, 6)
        self[random_index + 1] = random.randrange(0, 3)
        self[random_index + 2] = random.randrange(0, 3)

        self.check_duplicate_qubit_assignment()

    def set_gate_string(self, string_list):
        self.clear()
        for string in string_list:
            self.append(string)

    def get_gates_string(self):
        return self

    def clear_string(self):
        self.clear()


def create_mutated_generation(chromosomes: int, parent: list) -> list:
    mutated_gen = [parent]
    for i in range(chromosomes):
        mutated_string = CircuitString()
        mutated_string.set_gate_string(parent)
        mutated_string.mutate_gate_string()
        mutated_gen.append(mutated_string)
    return mutated_gen


class CircuitGenerator(object):
    """ Generates a string of 3*number_of_gates length number representing gate types and position in a quantum
    circuit """

    def __init__(self, number_of_gates):
        self.gate_list = []
        self.theta_list = []
        self.number_of_gates = number_of_gates
        self.string_length = number_of_gates * 3
        self.circuit = QuantumCircuit(3, 1)
        self.shots = 1024
        self.STARTING_STATES = [[0, 0, 0],
                                [0, 0, 1],
                                [0, 1, 0],
                                [0, 1, 1],
                                [1, 0, 0],
                                [1, 0, 1],
                                [1, 1, 0],
                                [1, 1, 1]]
        self.desired_chance_of_one = [0.5, 0.3, 0.4, 0, 0.5, 0.2, 0, 0.9]

    def __repr__(self):
        return str(self.gate_list) + '\n'

    def generate_circuit(self):
        # Parsing integer string and converting it to gates
        self.clear_circuit()
        for i in range(0, self.number_of_gates):
            gate_index = i * 3

            a = self.gate_list[gate_index]
            b = self.gate_list[gate_index + 1]
            c = self.gate_list[gate_index + 2]

            # theta = random.uniform(0, 2 * math.pi)
            theta = 5 * math.pi / 2

            if a == 0:
                self.circuit.cx(b, c)
            elif a == 1:
                self.circuit.x(b)
            elif a == 2:
                self.circuit.h(b)
            elif a == 3:
                self.circuit.z(b)
            elif a == 4:
                self.circuit.rzz(theta=theta, qubit1=b, qubit2=c)
            elif a == 5:
                self.circuit.rxx(theta=theta, qubit1=b, qubit2=c)

        self.circuit.measure(0, 0)

    def initialize_initial_states(self, triplet: list):
        if triplet[0] == 1:
            self.circuit.x(0)
        if triplet[1] == 1:
            self.circuit.x(1)
        if triplet[2] == 1:
            self.circuit.x(2)

    def create_initial_generation(self, chromosomes: int) -> list:
        circuit_list = []
        for i in range(chromosomes):
            circuit_string = CircuitString()
            circuit_string.generate_gate_string(self.string_length)
            circuit_list.append(circuit_string)

        return circuit_list



    def run_generation(self, circuit_string_list) -> list:
        fitness_list = []
        for circ_str in circuit_string_list:
            chromosome_fitness = self.find_chromosome_fitness(circ_str)
            fitness_list.append(chromosome_fitness)
        return fitness_list

    def calculate_error(self, desired_outcome):
        counts = self.run_circuit()
        if '0' in counts:
            chance_of_one = (self.shots - counts['0']) / self.shots
            error = abs(desired_outcome - chance_of_one)
        else:
            error = 1
        return error

    def run_circuit(self):
        aer_sim = Aer.get_backend('aer_simulator')
        # aer_sim = Aer.get_backend('statevector_simulator')
        qobj = assemble(self.circuit, shots=self.shots)
        job = aer_sim.run(qobj)
        return job.result().get_counts()

    def find_chromosome_fitness(self, circuit_string: CircuitString) -> float:
        fitness = 0
        for i in range(0, len(self.STARTING_STATES)):
            self.clear_circuit()
            self.clear_string()
            self.initialize_initial_states(self.STARTING_STATES[i])
            self.set_gate_string(circuit_string)
            self.generate_circuit()
            error: float = self.calculate_error(self.desired_chance_of_one[i])
            fitness = fitness + error
        return fitness

    def clear_string(self):
        self.gate_list = []

    def draw_circuit(self):
        print(self.circuit.draw(output='text'))

    def set_gate_string(self, string_list: list):
        self.gate_list = string_list

    def get_gates_string(self):
        return self.gate_list

    def clear_circuit(self):
        self.circuit.data.clear()
