import random
from qiskit import *


class CircuitGenerator(object):
    """ Generates a string of 3*number_of_gates length number representing gate types and position in a quantum
    circuit """

    def __init__(self, number_of_gates):
        self.integer_string = []
        self.number_of_gates = number_of_gates
        self.string_length = number_of_gates * 3
        self.circuit = QuantumCircuit(3, 1)
        self.shots = 1024

    def generate_gate_string(self):
        # Returns a randomly generated string representation of given number of qbits

        for i in range(self.string_length):
            if i % 3 == 0:
                self.integer_string.append(random.randrange(0, 5))
            else:
                self.integer_string.append(random.randrange(0, 3))

        for i in range(0, int(self.string_length / 3)):
            int_index = i * 3

            if (self.integer_string[int_index] == 0 and self.integer_string[int_index + 1] == self.integer_string[
                int_index + 2]):
                if self.integer_string[int_index + 1] == 0:
                    self.integer_string[int_index + 1] = random.randrange(1, 3)
                elif self.integer_string[int_index + 1] == 1:
                    self.integer_string[int_index + 2] = 0  # TODO - hardcoded
                elif self.integer_string[int_index + 1] == 2:
                    self.integer_string[int_index + 2] = random.randrange(0, 2)
        # print(self.integer_string)

        return self.integer_string

    def generate_circuit_from_string(self):
        # Parsing integer string and converting it to gates

        for i in range(0, int(self.string_length / 3)):
            gate_index = i * 3

            a = self.integer_string[gate_index]
            b = self.integer_string[gate_index + 1]
            c = self.integer_string[gate_index + 2]

            if a == 0:
                self.circuit.cx(b, c)
            elif a == 1:
                self.circuit.x(b)
            elif a == 2:
                self.circuit.h(b)
            elif a == 3:
                self.circuit.y(b)
            elif a == 4:
                self.circuit.z(b)

        self.circuit.measure(0, 0)

    def get_gates_String(self):
        return self.integer_string

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

        if str(desired_outcome) in counts:
            error = (counts[str(desired_outcome)] / self.shots) * 100
        else:
            error = 100

        return error
