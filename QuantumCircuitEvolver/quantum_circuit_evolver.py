# Written by Sebastian T. Overskott 2022. Github link: https://github.com/Overskott/Evolving-quantum-circuits

import copy
import math
import random
from typing import List
from qiskit import *


class Chromosome(object):
    """
    A class used to represent a quantum computer circuit as a list of integers.

    The circuit is represented as a list
    of integers, where each gate is three successive integers i.e.:

    Three gates as list:
    [2, 0, 1, 3, 1 ,1, 4, 0, 2]

    Gate number:               1  |  2  |  3
    Gate int representation:  201 | 311 | 402

    The first int is what kind of gate it is (i.e. X-gate, CNOT, Hadamard).
    The second int is what qubit is this assigned to (0 -> qubit 0, 1 -> qubit 1, ...)
    The third int is what qubit is controlling the gate. in cases where gates do not have an
    external controller, this int is ignored.

    The table describing int, corresponding gate and if it uses control qubit, yes or no (Y/N):

    Int |  Gate   | Control
    ----------------------
     0  | C-NOT   |   Y
     1  | X       |   N
     2  | Hadamard|   N
     3  | Z       |   N
     4  | RZZ     |   Y
     5  | RXX     |   Y
     6  | Swap    |   Y
     7  | Y       |   N

    Some gates (RZZ, RXX) also need an angle value (theta) stored in a separate list.

    Attributes
    ----------
    _integer_list: List[int]
        List of integers representing the quantum circuit.
    _theta_list: List[float]
        A list of angle values for the gates. This list is the same length as number of gates (len(_integer_list) / 3).
    _length: int
        The number of integers in the integer representation
    _.GATES: int
        Experimental. Use to adjust how many types of quantum gates to include in the circuit during generation.
    """

    def __init__(self):
        """The Chromosome constructor"""

        self._integer_list: List[int] = []
        self._theta_list: List[float] = []
        self._length: int = 0
        self._GATES = 8

    def __repr__(self):
        """Returns desired for printing == print(_integer_list)"""
        return str(self._integer_list)

    def __len__(self):
        """Returns the number of int in _integer_list"""
        return self._length

    def __iter__(self):
        """Returns iterateable _integer_list"""
        yield from self._integer_list

    def set_integer_list(self, integer_list: List[int]):
        """


        Parameters:
           integer_list (List[int]): Quantum circuit integer representation.

        """

        old_integer_list = copy.copy(self._integer_list)
        self.clear()
        # self._length = len(integer_list)
        for integer in integer_list:
            self._integer_list.append(integer)
        self._update_length()
        self._update_theta_list(old_integer_list, self._integer_list)

    def get_integer_list(self) -> List[int]:
        """Do X and return a list."""
        """Gets and prints the spreadsheet's header columns

        Parameters
        ----------
        file_loc : str
            The file location of the spreadsheet
        print_cols : bool, optional
            A flag used to print the columns to the console (default is False)

        Returns
        -------
        list
            a list of strings representing the header columns
        """

        return self._integer_list

    def _update_length(self):
        """Do X and return a list."""

        self._length = len(self._integer_list)

    def get_length(self) -> int:
        """Returns the number of integers in _integer_list."""
        return self._length

    def get_theta_list(self) -> List[float]:
        """Do X and return a list."""
        return self._theta_list

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

    def _update_theta_list(self, old, new):
        gates = int(self._length / 3)
        change_list = self._change_in_theta(old, new)

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

    def _change_in_theta(self, old, new):
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
        """Gets and prints the spreadsheet's header columns

                Parameters
                ----------
                file_loc : str
                    The file location of the spreadsheet
                print_cols : bool, optional
                    A flag used to print the columns to the console (default is False)

                Returns
                -------
                list
                    a list of strings representing the header columns
                """
        # Returns a randomly generated string representation of given number of qubits
        for i in range(gates * 3):
            if i % 3 == 0:
                self._integer_list.append(random.randrange(0, self._GATES))
            else:
                self._integer_list.append(random.randrange(0, 3))

        self._update_length()
        self._fix_duplicate_qubit_assignment()
        self._generate_theta_list()

    def mutate_chromosome(self):
        gates = int(self._length / 3)
        old_integer_list = copy.copy(self._integer_list)
        random_index = random.randrange(0, gates) * 3

        self._integer_list[random_index] = random.randrange(0, self._GATES)
        self._integer_list[random_index + 1] = random.randrange(0, 3)
        self._integer_list[random_index + 2] = random.randrange(0, 3)

        self._fix_duplicate_qubit_assignment()
        self._update_theta_list(old_integer_list, self._integer_list)

    def mutate_chromosome(self):
        gates = int(self._length / 3)
        old_integer_list = copy.copy(self._integer_list)

        self._replace_gate_with_random_gate()

        self._fix_duplicate_qubit_assignment()
        self._update_theta_list(old_integer_list, self._integer_list)

    def _replace_gate_with_random_gate(self):
        random_index = random.randrange(0, int(self._length/3)) * 3

        self._integer_list[random_index] = random.randrange(0, self._GATES)
        self._integer_list[random_index + 1] = random.randrange(0, 3)
        self._integer_list[random_index + 2] = random.randrange(0, 3)

    def _fix_duplicate_qubit_assignment(self):
        gates = int(self._length / 3)

        for i in range(0, gates):
            int_index = i * 3

            if ((self._integer_list[int_index] in [0, 4, 5, 6]) and
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
        self.chromosome_list.append(parent)
        for i in range(self._chromosomes-1):
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
            elif a == 6:
                self.circuit.swap(b, c)
            elif a == 7:
                self.circuit.y(b)

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

    def print_ca_outcomes(self):
        for i in range(0, len(self.STARTING_STATES)):
            self.clear_circuit()
            # self.chromosome.clear()
            self.initialize_initial_states(self.STARTING_STATES[i])
            # self.chromosome = chromosome
            self.generate_circuit()
            print(str(self.STARTING_STATES[i]) + "| " + str(self.run_simulator()))

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
