import numpy as np
from qiskit import *
from qiskit.providers.aer import AerSimulator
import EQC

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
qubits = 3 # Do not change
number_of_gates = 10
number_of_shots = 1024
starting_states_CA = [[0,0,0],
                     [0,0,1],
                     [0,1,0],
                     [0,1,1],
                     [1,0,0],
                     [1,0,1],
                     [1,1,0],
                     [1,1,1]]


desired_outcome = [0, 0, 1, 1 ,0 ,1 , 0, 1]

for i in range(100):
    print('run' + str(i) + ': ')
    index = 0

    sum_of_runs= 0

    randomStringGenerator = EQC.CircuitGenerator(number_of_gates)

    gateStringRepresentation = randomStringGenerator.generateGateString()

    for triplet in starting_states_CA:
        # Initialize circuit
        circuit = QuantumCircuit(qubits,1)
    
        initializeCAstates(triplet)
    
        randomStringGenerator.generateCircuitFromString(circuit)
    
        #runCircuit(circuit, number_of_shots)

        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(circuit, shots=number_of_shots)
        job = aer_sim.run(qobj)
        counts = job.result().get_counts()

        #print(counts)
        #print(index)
        do = desired_outcome[index]
    
        if(str(do) in counts):
            point=(counts[str(do)]/number_of_shots)*100
            #print(point)
        else:
            point= 100
            #print(100)


        index = index + 1
        sum_of_runs = sum_of_runs + point
    
    print(sum_of_runs)