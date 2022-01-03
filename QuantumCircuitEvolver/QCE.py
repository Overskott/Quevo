
import quantum_circuit_evolver as qce

if __name__ == '__main__':
    number_of_gates = 10
    chromosomes = 10
    generations = 20
    desired_chance_of_one = [0.5, 0.3, 0.4, 0, 0.5, 0.2, 0, 0.9]

    circuit_list = []
    circuit_string = qce.CircuitString(number_of_gates * 3)


    """ def init_first_gen():"""
    for i in range(chromosomes):
        circuit_string.clear_string()
        circuit_string.generate_gate_string()
        circuit_list.append(circuit_string)
    """ *----------------------------* """

    generated_circuit = qce.CircuitGenerator(number_of_gates)

    fitness_list = generated_circuit.run_generation(circuit_list)

    min_string = min(fitness_list)
    min_index = fitness_list.index(min_string)
    best_circuit = circuit_list[min_index].get_gates_string()

    print(str(min_string) + "\n" + str(best_circuit))
    print("\n\n\n")
    mutated_list = []
    mutated_string = qce.CircuitString(number_of_gates*3)

    for i in range(chromosomes):
        print(best_circuit)
        mutated_string.set_gate_string(best_circuit)
        mutated_string.mutate_gate_string()
        mutated_list.append(circuit_string)

    generated_circuit = qce.CircuitGenerator(number_of_gates)

    fitness_list = generated_circuit.run_generation(mutated_list)

    min_string = min(fitness_list)
    min_index = fitness_list.index(min_string)
    best_circuit = circuit_list[min_index]
    print("\n\n\n")
    print(str(min_string) + "\n" + str(best_circuit))



















    input()

    for i in range(chromosomes):
        print('Run ' + str(i) + ': ')
        print("---------")
        sum_of_runs = 0

        generated_circuit = qce.CircuitGenerator(number_of_gates)
        generated_circuit.generate_gate_string()

        index = 0

        for triplet in starting_states:

            generated_circuit.initialize_initial_states(triplet)
            generated_circuit.generate_circuit()
            error = generated_circuit.calculate_error(desired_chance_of_one[index])

            sum_of_runs = sum_of_runs + error
            index = index + 1

        print("Total error on run " + str(i) + ": " + str(sum_of_runs))
        print("---------")
        print(" ")

        if sum_of_runs < best_outcome:
            best_outcome = sum_of_runs
            best_circuit = generated_circuit.get_gates_string()

    print("best result: " + str(best_outcome))
    print(best_circuit)
    print()

    final_outcome = best_outcome

    for c_num in range(0, generations):
        best_mutated = best_circuit
        print("generation: " + str(c_num+1))
        for i in range(0, chromosomes):
            sum_of_runs = 0

            index = 0

            next_gen_circuit = qce.CircuitGenerator(number_of_gates)
            next_gen_circuit.set_gate_string(best_circuit)
            next_gen_circuit.mutate_gate_string()

            print('Run mutated ' + str(i) + ': ')
            print("---------")

            for triplet in starting_states:
                next_gen_circuit.initialize_initial_states(triplet)
                next_gen_circuit.generate_circuit_from_string()
                error = next_gen_circuit.calculate_error(desired_chance_of_one[index])

                sum_of_runs = sum_of_runs + error
                index = index + 1

            print("Total error on run " + str(i) + ": " + str(sum_of_runs))
            print("---------")
            print(" ")

            if sum_of_runs < best_outcome:
                best_outcome = sum_of_runs
                print(best_circuit)
                print(next_gen_circuit.get_gates_string())
                best_circuit = next_gen_circuit.get_gates_string()

        if best_outcome < final_outcome:
            final_outcome = best_outcome
            best_mutated = best_circuit

    print("Final result: " + str(final_outcome))
    print(best_mutated)
    best_result = qce.CircuitGenerator(number_of_gates)
    best_result.set_gate_string(best_mutated)
    best_result.generate_circuit_from_string()
    best_result.draw_circuit()










