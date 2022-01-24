# Written by Sebastian T. Overskott Jan. 2022. Github link: https://github.com/Overskott/Evolving-quantum-circuits

from typing import List

from qiskit import QuantumCircuit, Aer, assemble
from scipy.special import rel_entr

from Quevo.Chromosome import Chromosome


class Circuit(object):
    """
    A qiskit QuantumCircuit made from a chromosome.

    Attributes
    ----------
    chromosome (Chromosome):
        The integer string representation of the circuit.
    circuit (Qiskit.QuantumCircuit):
        Qiskit representation of the chromosome. A circuit that can be run and simulated.
    shots (int):
        Number of runs in the qiskit quantum circuit simulator.
    STARTING_STATES (List[list]):
        Possible cellular automata initial conditions for the 1D Von Neumann neighborhood.
    """

    def __init__(self, chromosome: Chromosome):
        """
        Circuit constructor. Takes a chromosome as parameter, and creates a Qiskit
        QuantumCircuit object form it.

        Parameters
        ----------
        chromosome: (Chromosome)
            The chromosome that describes the QuantumCircuit.
        """
        self.chromosome = chromosome
        self.circuit = QuantumCircuit(3, 1)
        self.shots = 1000
        self.STARTING_STATES = [[0, 0, 0],
                                [0, 0, 1],
                                [0, 1, 0],
                                [0, 1, 1],
                                [1, 0, 0],
                                [1, 0, 1],
                                [1, 1, 0],
                                [1, 1, 1]]
        self.results = {}

    def __repr__(self):
        """Returns a string visualizing the quantum circuit"""
        return self.draw()

    def generate_circuit(self) -> None:
        """
        Parses the chromosome, and generates a Qiskit QuantumCircuit from it.
        """
        gates = int(self.chromosome.get_length() / 3)

        gate_dict = self.chromosome.get_gate_dict()

        for i in range(0, gates):
            gate_index = i * 3

            a = self.chromosome.get_integer_list()[gate_index]
            b = self.chromosome.get_integer_list()[gate_index + 1]
            c = self.chromosome.get_integer_list()[gate_index + 2]

            gate = gate_dict[str(a)]

            if gate == 'h':
                self.circuit.h(b)
            elif gate == 'cx':
                self.circuit.cx(b, c)
            elif gate == 'x':
                self.circuit.x(b)
            elif gate == 'swap':
                self.circuit.swap(b, c)
            elif gate == 'rzz':
                theta = self.chromosome.get_theta_list()[i]
                self.circuit.rzz(theta=theta, qubit1=b, qubit2=c)
            elif gate == 'rxx':
                theta = self.chromosome.get_theta_list()[i]
                self.circuit.rxx(theta=theta, qubit1=b, qubit2=c)
            elif gate == 'toffoli':
                target = b
                if target == 1:
                    self.circuit.toffoli(0, 2, target)
                else:
                    self.circuit.toffoli(abs(target - 1), abs(target - 2), target)
            elif gate == 'y':
                self.circuit.y(b)
            elif gate == 'z':
                self.circuit.z(b)
            else:
                print(gate + " is not a valid gate!")

        self.circuit.measure(0, 0)

    def calculate_probability_of_one(self) -> float:
        """Returns the measured chance of one after simulation"""
        counts = self.run_simulator()
        if '1' in counts:
            chance_of_one = counts['1'] / self.shots
        else:
            chance_of_one = 0.0

        return chance_of_one

    def find_chromosome_fitness(self, desired_chance_of_one: List[float]) -> float:
        """
        Calculates and return the fitness for the chromosome i.e.
        the sum of differences in all initial states.

        Parameters
        ----------
        desired_chance_of_one: List[float]
            A list of desired probabilities for all the CA initial states.

        Returns
        -------
        fitness: (float)
            The chromosome fitness.
        """
        fitness = 0
        for i in range(0, len(self.STARTING_STATES)):

            state = self.STARTING_STATES[i]
            probability = desired_chance_of_one[i]
            found_probability = self.find_init_state_probability(state)
            difference = abs(probability - found_probability)
            fitness = fitness + difference

        return fitness

    def find_kullback_liebler_fitness(self, desired_chance_of_one: List[float]) -> float:
        """
        Calculates and return the fitness for the chromosome with relative entropy (Kullback-Liebler).

        Parameters
        ----------
        desired_chance_of_one: List[float]
            A list of desired probabilities for all the CA initial states.

        Returns
        -------
        fitness: (float)
            The chromosome fitness.

        """
        fitness = 0
        probabilities = []
        found_probabilities = []
        for i in range(0, len(self.STARTING_STATES)):

            state = self.STARTING_STATES[i]
            found_probabilities.append(self.find_init_state_probability(state))
            probabilities.append(desired_chance_of_one[i])

        p = found_probabilities
        q = probabilities

        if p == 0:
            p = 0.00001
        if q == 0:
            q = 0.00001

        d = sum(rel_entr(p, q))

        fitness = fitness + d
        return fitness

    def find_init_state_probability(self, state: List[int]) -> float:
        """
        Finds the difference between the desired probability and measured probability for given state.

        Parameters
        ---------
        state: (List[int])
            A list with a binary triplet describing the initial state.

        Returns
        -------
        difference: (float)
            The difference between the desired probability and measured probability for given state.
        """
        self.clear_circuit()
        self.initialize_initial_states(state)
        self.generate_circuit()

        chance_of_one = self.calculate_probability_of_one()
        return chance_of_one

    def print_ca_outcomes(self, desired_chance_of_one: List[float]):
        """Prints a table of the results from a run of the chromosome"""
        print("Initial State | Desired outcome | Actual outcome  | Difference")
        total_diff = 0
        for i in range(0, len(self.STARTING_STATES)):
            state = self.STARTING_STATES[i]
            probability = desired_chance_of_one[i]

            found_probability = self.find_init_state_probability(state)
            # found_probability = self.find_kullback_liebler_fitness(state)
            difference = abs(found_probability - probability)
            total_diff = total_diff + difference
            desired_format = "{:.4f}".format(desired_chance_of_one[i])
            chance_format = "{:.4f}".format(found_probability)
            diff_format = "{:.4f}".format(difference)

            print(str(self.STARTING_STATES[i]) + "           "
                  + desired_format + "           "
                  + chance_format + "           "
                  + diff_format)
            self.clear_circuit()
        print("Total difference: " + str(total_diff))

    def get_total_difference(self, desired_chance_of_one: List[float]):
        total_diff = 0
        for i in range(0, len(self.STARTING_STATES)):
            state = self.STARTING_STATES[i]
            probability = desired_chance_of_one[i]

            found_probability = self.find_init_state_probability(state)
            difference = abs(found_probability - probability)
            total_diff = total_diff + difference

        return total_diff

    def print_counts(self):
        """Prints the counts result from simulation"""
        index = 0
        for triplet in self.STARTING_STATES:
            self.clear_circuit()
            self.initialize_initial_states(triplet)
            self.generate_circuit()
            print(self.run_simulator())
            index = index + 1

    def initialize_initial_states(self, triplet: List[int]) -> None:
        """
        Initializes a Cellular Automata (CA) state in the circuit.

        Parameters
        ----------
        triplet: List[int]
            A list of three integer in {0,1} representing the one of the
            eight starting possibilities in 1D Von Neumann CA.
        """

        if triplet[0] == 1:
            self.circuit.x(0)
        if triplet[1] == 1:
            self.circuit.x(1)
        if triplet[2] == 1:
            self.circuit.x(2)

    def run_simulator(self) -> dict:
        """
        Runs the circuit on the Qiskit AER simulator and returns the results as a dictionary.

        Returns
        -------
        counts: dict
            The results from the AER simulation.
        """
        aer_sim = Aer.get_backend('aer_simulator')
        # aer_sim = Aer.get_backend('aer_simulator_density_matrix')
        # aer_sim = Aer.get_backend('aer_simulator_stabilizer')
        quantum_circuit = assemble(self.circuit, shots=self.shots)
        job = aer_sim.run(quantum_circuit)
        counts = job.result().get_counts()
        return counts

    def draw(self) -> None:
        """Prints a visual representation of the circuit"""
        print(self.circuit.draw(output='text'))

    def clear_circuit(self) -> None:
        """Clears the Qiskit QuantumCircuit for all gates"""
        self.circuit.data.clear()
