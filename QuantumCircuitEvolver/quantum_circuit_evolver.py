import copy
import math
import random
from typing import List
from qiskit import *


class Chromosome(object):
    """
    A class used to represent a quantum computer circuit as a list of integers.

    ...

    Attributes
    ----------
    _integer_list: List[int]
        List of integers representing quantum gates. 3 successive integers for one gate.
    _theta_list: List[float]
        A list of angular values for the gates.

    Methods
    -------
    generate_gate_string(length) : None
        Generates a list of random quantum gate integer representations
        of length = length.
    mutate_gate_string() : None
        Randomly changes/replaces one of the gates in the gate representation
    check_duplicate_qubit_assignment() : None
        Checks if the randomly generated or mutated circuit is valid. Fixes it
        if not.
    set_gate_string(string_list) : None
        Sets the gate representation from input list.
    get_gates_string() : list
        Returns the gate representation as a list
    clear_string() : None
        clears the gate representation list
    """

    def __init__(self):
        self._integer_list: List[int] = []
        self._theta_list: List[float] = []
        self._length: int = 0

    def __repr__(self):
        return str(self._integer_list)

    def __len__(self):
        return self._length

    def __iter__(self):
        yield from self._integer_list

    def set_integer_list(self, integer_list: List[int]):
        self.clear()
        # self._length = len(integer_list)
        for integer in integer_list:
            self._integer_list.append(integer)
        self._update_length()
        self._update_theta_list()

    def get_integer_list(self) -> List[int]:
        return self._integer_list

    def get_length(self):
        return self._length

    def _update_length(self):
        self._length = len(self._integer_list)

    def _generate_theta_list(self):
        self._theta_list.clear()

        gates = int(self._length / 3)

        for i in range(0, gates):
            int_index = i * 3

            if self._integer_list[int_index] in [4, 5]:
                theta = random.uniform(0, 2 * math.pi)
                self._theta_list.append(theta)
            else:
                self._theta_list.append(0)

    def get_theta_list(self) -> List[float]:
        return self._theta_list

    def _update_theta_list(self, old, new):
        gates = int(self._length / 3)
        change_list = self.change_in_theta(old, new)

        for i in range(0, gates):
            int_index = i * 3

            if change_list[int_index] == 1 and \
                    self._integer_list[int_index] in [4, 5]:
                theta = random.uniform(0, 2 * math.pi)
                self._theta_list[i] = theta
            elif self._integer_list[int_index] in [4, 5]:
                continue
            else:
                self._theta_list[i] = 0

    def change_in_theta(self, old, new):
        binary_list = []
        for i in range(0, self._length):
            if old[i] == new[i]:
                binary_list.append(0)
            else:
                binary_list.append(1)
        return binary_list

    def clear(self):
        self._integer_list.clear()
        self._theta_list.clear()
        self._length = 0

    def generate_random_chromosome(self, gates):
        # Returns a randomly generated string representation of given number of qubits
        for i in range(gates * 3):
            if i % 3 == 0:
                self._integer_list.append(random.randrange(0, 6))
            else:
                self._integer_list.append(random.randrange(0, 3))

        self._update_length()
        self.fix_duplicate_qubit_assignment()
        self._generate_theta_list()

    def mutate_chromosome(self):
        gates = int(self._length / 3)
        old_integer_list = copy.copy(self._integer_list)
        random_index = random.randrange(0, gates) * 3

        self._integer_list[random_index] = random.randrange(0, 6)
        self._integer_list[random_index + 1] = random.randrange(0, 3)
        self._integer_list[random_index + 2] = random.randrange(0, 3)

        self.fix_duplicate_qubit_assignment()
        self._update_theta_list(old_integer_list, self._integer_list)

    def fix_duplicate_qubit_assignment(self):
        gates = int(self._length / 3)

        for i in range(0, gates):
            int_index = i * 3

            if ((self._integer_list[int_index] in [0, 4, 5]) and
                    self._integer_list[int_index + 1] == self._integer_list[int_index + 2]):

                if self._integer_list[int_index + 1] == 0:
                    self._integer_list[int_index + 1] = random.randrange(1, 3)

                elif self._integer_list[int_index + 1] == 1:
                    self._integer_list[int_index + 2] = 0  # TODO - hardcoded, make random

                elif self._integer_list[int_index + 1] == 2:
                    self._integer_list[int_index + 2] = random.randrange(0, 2)


class Generation(object):

    def __init__(self, chromosomes, gates):
        self.chromosome_list: List[Chromosome] = []
        self.fitness_list: List[float] = []
        self._chromosomes: int = chromosomes
        self._gates: int = gates

    def create_initial_generation(self) -> None:
        self.chromosome_list.clear()
        for i in range(self._chromosomes):
            chromosome = Chromosome()
            chromosome.generate_random_chromosome(self._gates)
            self.chromosome_list.append(chromosome)

    def create_mutated_generation(self, parent: Chromosome) -> None:
        self.chromosome_list.clear()
        for i in range(self._chromosomes):
            mutated_chromosome = copy.deepcopy(parent)
            mutated_chromosome.mutate_chromosome()
            self.chromosome_list.append(mutated_chromosome)

    def run_generation(self, desired_outcome: List[float]) -> None:

        for chromosome in self.chromosome_list:
            circuit = Circuit(chromosome)
            chromosome_fitness = circuit.find_chromosome_fitness(desired_outcome)
            self.fitness_list.append(chromosome_fitness)


class Circuit(object):
    """ Generates a string of 3 * number_of_gates length number representing gate types and position in a quantum
    circuit """

    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome
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
        # self.desired_chance_of_one = [0.5, 0.3, 0.4, 0, 0.5, 0.2, 0, 0.9]

    def __repr__(self):
        # return str(self.gate_list) + '\n'
        return self.draw()

    def generate_circuit(self):
        # Parsing integer string and converting it to gates
        self.clear_circuit()
        gates = int(self.chromosome.get_length() / 3)

        for i in range(0, gates):
            gate_index = i * 3

            a = self.chromosome.get_integer_list()[gate_index]
            b = self.chromosome.get_integer_list()[gate_index + 1]
            c = self.chromosome.get_integer_list()[gate_index + 2]

            if a == 0:
                self.circuit.cx(b, c)
            elif a == 1:
                self.circuit.x(b)
            elif a == 2:
                self.circuit.h(b)
            elif a == 3:
                self.circuit.z(b)
            elif a == 4:
                theta = self.chromosome.get_theta_list()[i]
                self.circuit.rzz(theta=theta, qubit1=b, qubit2=c)
            elif a == 5:
                theta = self.chromosome.get_theta_list()[i]
                self.circuit.rxx(theta=theta, qubit1=b, qubit2=c)

        self.circuit.measure(0, 0)

    def calculate_error(self, desired_outcome):
        counts = self.run_simulator()
        if '0' in counts:
            chance_of_one = (self.shots - counts['0']) / self.shots
            error = abs(desired_outcome - chance_of_one)
        else:
            error = 1
        return error

    def run_simulator(self):
        aer_sim = Aer.get_backend('aer_simulator')
        # aer_sim = Aer.get_backend('statevector_simulator')
        quantum_circuit = assemble(self.circuit, shots=self.shots)
        job = aer_sim.run(quantum_circuit)
        return job.result().get_counts()

    def find_chromosome_fitness(self, desired_chance_of_one: List[float]) -> float:
        fitness = 0
        for i in range(0, len(self.STARTING_STATES)):
            self.clear_circuit()
            # self.chromosome.clear()
            self.initialize_initial_states(self.STARTING_STATES[i])
            # self.chromosome = chromosome
            self.generate_circuit()
            error = self.calculate_error(desired_chance_of_one[i])
            fitness = fitness + error
        return fitness

    def initialize_initial_states(self, triplet: list):
        if triplet[0] == 1:
            self.circuit.x(0)
        if triplet[1] == 1:
            self.circuit.x(1)
        if triplet[2] == 1:
            self.circuit.x(2)

    def draw(self):
        print(self.circuit.draw(output='text'))

    def clear_circuit(self):
        self.circuit.data.clear()
