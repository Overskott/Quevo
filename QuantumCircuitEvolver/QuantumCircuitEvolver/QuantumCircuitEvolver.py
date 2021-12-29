import numpy as np
import random
from qiskit import *
from qiskit.visualization import plot_histogram
from qiskit.providers.aer import AerSimulator
import EQC

#def generateCircuitFromString(integer_string):
#    # Parsing integer string and converting it to gates
#    string_length = number_of_gates*3

#    for i in range (0, int(string_length/3)):
#        gate_index = i*3

#        a=integer_string[gate_index]
#        b=integer_string[gate_index+1]
#        c=integer_string[gate_index+2]

#        if (a==0):
#            circuit.cx(b,c)
#        elif (a==1):
#            circuit.x(b)
#        elif (a==2):
#            circuit.h(b)
#        elif (a==3):
#            circuit.y(b)
#        elif (a==4):
#            circuit.z(b)
            

#    circuit.measure(0,0)

def initializeCAstates(triplet):
    
    if (triplet[0]==1):
        circuit.x(0)
    if (triplet[1]==1):
        circuit.x(1)
    if (triplet[2]==1):
        circuit.x(2)

def runCircuit(circuit, number_of_shots):
    aer_sim = Aer.get_backend('aer_simulator')
    qobj = assemble(circuit, shots=number_of_shots)
    job = aer_sim.run(qobj)
    counts = job.result().get_counts()

    print(counts)

# Main
qubits = 3
number_of_gates = 14
number_of_shots = 1024
starting_states_CA= [[0,0,0],
                     [0,0,1],
                     [0,1,0],
                     [0,1,1],
                     [1,0,0],
                     [1,0,1],
                     [1,1,0],
                     [1,1,1]]

randomStringGenerator = EQC.CircuitGenerator(number_of_gates)

gateStringRepresentation = randomStringGenerator.generateGateString()

for triplet in starting_states_CA:
    # Initialize circuit
    circuit = QuantumCircuit(qubits,1)
    
    initializeCAstates(triplet)
    
    randomStringGenerator.generateCircuitFromString(circuit)
    
    runCircuit(circuit, number_of_shots)

#Draw circuit
circuit.draw()