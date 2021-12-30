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
        self.shots = 1000

    def set_gate_string(self, string_list):
        self.gate_string = string_list

    def generate_gate_string(self):
        # Returns a randomly generated string representation of given number of qbits

        for i in range(self.string_length):
            if i % 3 == 0:
                self.gate_string.append(random.randrange(0, 5))
            else:
                self.gate_string.append(random.randrange(0, 3))

        for i in range(0, int(self.string_length / 3)):
            int_index = i * 3

            if ((self.gate_string[int_index] == 0 or self.gate_string[int_index] == 4) and
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
                self.circuit.y(b)
            elif a == 4:
                theta = random.uniform(0, 2*math.pi)
                self.circuit.rzz(theta=theta, qubit1=b, qubit2=c)

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

        print("Desired outcome: " + str(desired_outcome))

        if str(desired_outcome) in counts:
            # error = (counts[str(desired_outcome)] / self.shots) * 100
            error = (self.shots - counts[str(desired_outcome)]) / self.shots * 100
            print("Outcome: " + str(counts))
            print(error)

        else:
            error = 100
            print("Outcome: " + str(1 - desired_outcome))
            print(error)
        return error

    def draw_circuit(self):
        print(self.circuit.draw(output='text'))
