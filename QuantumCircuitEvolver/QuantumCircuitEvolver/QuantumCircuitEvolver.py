import EQC

if __name__ == '__main__':
    number_of_gates = 10
    number_of_chromosomes = 10
    starting_states_CA = [[0, 0, 0],
                          [0, 0, 1],
                          [0, 1, 0],
                          [0, 1, 1],
                          [1, 0, 0],
                          [1, 0, 1],
                          [1, 1, 0],
                          [1, 1, 1]]

    desired_outcome = [1, 0, 1, 0, 0, 1, 0, 1]

    for i in range(number_of_chromosomes):
        print("---------")
        print('run' + str(i) + ': ')
        sum_of_runs = 0

        generated_circuit = EQC.CircuitGenerator(number_of_gates)
        generated_circuit.generate_gate_string()
        index = 0

        for triplet in starting_states_CA:

            generated_circuit.generate_gate_string()
            generated_circuit.initialize_initial_states(triplet)
            generated_circuit.generate_circuit_from_string()
            error = generated_circuit.calculate_error(desired_outcome[index])

            sum_of_runs = sum_of_runs + error
            index = index + 1

        print("Total run " + str(i) + " : " + str(sum_of_runs))
        print("---------")
        print(" ")


