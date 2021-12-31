import math
import random
from qiskit import *


class CircuitGenerator(object):
    """ Generates a string of 3*number_of_gates length number representing gate types and position in a quantum
    circuit """

    def __init__(self, number_of_gates):
        self.gate_string = []
        self.number_of_gates = number_of_gates
        self.string_length = number_of_gates * 3
        self.circuit = QuantumCircuit(3, 1)
        self.shots = 2048

    def set_gate_string(self, string_list):
        self.gate_string = string_list

    def generate_gate_string(self):
        # Returns a randomly generated string representation of given number of qbits

        for i in range(self.string_length):
            if i % 3 == 0:
                self.gate_string.append(random.randrange(0, 6))
            else:
                self.gate_string.append(random.randrange(0, 3))

        for i in range(0, int(self.string_length / 3)):
            int_index = i * 3

            if ((self.gate_string[int_index] in [0, 4, 5]) and
                    self.gate_string[int_index + 1] == self.gate_string[int_index + 2]):

                if self.gate_string[int_index + 1] == 0:
                    self.gate_string[int_index + 1] = random.randrange(1, 3)

                elif self.gate_string[int_index + 1] == 1:
                    self.gate_string[int_index + 2] = 0  # TODO - hardcoded

                elif self.gate_string[int_index + 1] == 2:
                    self.gate_string[int_index + 2] = random.randrange(0, 2)

        return self.gate_string

    def generate_circuit_from_string(self):
        # Parsing integer string and converting it to gates
        self.circuit = QuantumCircuit(3, 1)

        for i in range(0, self.number_of_gates):
            gate_index = i * 3

            a = self.gate_string[gate_index]
            b = self.gate_string[gate_index + 1]
            c = self.gate_string[gate_index + 2]

            if a == 0:
                self.circuit.cx(b, c)
            elif a == 1:
                self.circuit.x(b)
            elif a == 2:
                self.circuit.h(b)
            elif a == 3:
                self.circuit.z(b)
            elif a == 4:
                # theta = random.uniform(0, 2 * math.pi)
                theta = 3*math.pi/2
                self.circuit.rzz(theta=theta, qubit1=b, qubit2=c)
            elif a == 5:
                # theta = random.uniform(0, 2 * math.pi)
                theta = 3 * math.pi / 2
                self.circuit.rxx(theta=theta, qubit1=b, qubit2=c)

        self.circuit.measure(0, 0)

    def get_gates_string(self):
        return self.gate_string

    def initialize_initial_states(self, triplet):
        if triplet[0] == 1:
            self.circuit.x(0)
        if triplet[1] == 1:
            self.circuit.x(1)
        if triplet[2] == 1:
            self.circuit.x(2)

    def run_circuit(self):
        pass

    def calculate_error(self, desired_outcome):

        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(self.circuit, shots=self.shots)
        job = aer_sim.run(qobj)
        counts = job.result().get_counts()

       # print("Desired outcome for one: " + str(desired_outcome))

        if '0' in counts:
            chance_of_one = (self.shots - counts['0']) / self.shots
            #print("Outcome: " + str(counts))
            error = abs(desired_outcome - chance_of_one)
        else:
            chance_of_one = 1
            #print("Outcome: " + str(1 - desired_outcome))
            error = 1
        print("error: " + str(error))
        #print()
        return error

    def draw_circuit(self):
        print(self.circuit.draw(output='text'))

    def mutate_gate_string(self):

        random_index = random.randrange(0, self.number_of_gates) * 3

        self.gate_string[random_index] = random.randrange(0, 6)
        self.gate_string[random_index + 1] = random.randrange(0, 3)
        self.gate_string[random_index + 2] = random.randrange(0, 3)

        if ((self.gate_string[random_index] in [0, 4, 5]) and self.gate_string[random_index + 1] == self.gate_string[
            random_index + 2]):

            if self.gate_string[random_index + 1] == 0:
                self.gate_string[random_index + 1] = random.randrange(1, 3)

            elif self.gate_string[random_index + 1] == 1:
                self.gate_string[random_index + 2] = 0  # TODO - hardcoded

            elif self.gate_string[random_index + 1] == 2:
                self.gate_string[random_index + 2] = random.randrange(0, 2)
