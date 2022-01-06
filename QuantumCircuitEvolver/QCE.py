from quantum_circuit_evolver import *

# TODO: Setting up unit testing
# TODO: Documentation and comments
# TODO: Error and exception handling

if __name__ == '__main__':
    gates = 5
    chromosomes = 10
    # genes = gates * 3
    generations = 20
    desired_chance_of_one = [0.5, 0.7, 0.4, 0, 0.2, 0.7, 0.1, 0.9]
    # desired_chance_of_one = [1, 1, 1, 1, 1, 1, 1, 1]
    # desired_chance_of_one = [1, 0, 1, 0, 0, 1, 0, 1]
    # Generate initial generation of chromosomes

    init_gen = Generation(gates, chromosomes)
    init_gen.create_initial_generation()

    print("initial generation: ")
    for chromosome in init_gen.chromosome_list:
        print(chromosome)
    print('\n')

    print("Theta values: ")
    for chromosome in init_gen.chromosome_list:
        print(chromosome.get_theta_list())
    print('\n')

    print("Circuits: ")
    for chromosome in init_gen.chromosome_list:
        circuit = Circuit(chromosome)
        circuit.generate_circuit()
        circuit.draw()
    print("\n")

    init_gen.run_generation(desired_chance_of_one)

    for fitness in init_gen.fitness_list:
        print(fitness)
    print("\n")

    best_fitness = min(init_gen.fitness_list)
    min_index = init_gen.fitness_list.index(best_fitness)

    best_chromosome = init_gen.chromosome_list[min_index]

    print("Fitness for best chromosome: " + str(best_fitness) + "\n"
          + "Best chromosome: \n" + str(best_chromosome))
    print("\n")

    # Mutation loop

    best_mutated_chromosome = []
    final_fitness = 8

    for gen in range(0, generations):

        # Mutate next generation of chromosomes
        next_gen = Generation(chromosomes, gates)
        next_gen.create_mutated_generation(best_chromosome)

        # Print mutated generation
        print("Mutated generation " + str(gen + 1) + ": ")
        for chromosome in next_gen.chromosome_list:
            print(chromosome)
        print('\n')

        print("Theta values: ")
        for chromosome in next_gen.chromosome_list:
            print(chromosome.get_theta_list())
        print('\n')

        # Check every Chromosome's fitness
        next_gen.run_generation(desired_chance_of_one)

        # Print generation best result
        best_fitness = min(next_gen.fitness_list)
        min_index = next_gen.fitness_list.index(best_fitness)

        best_chromosome = next_gen.chromosome_list[min_index]
        print("Fitness for best mutated chromosome: " + str(best_fitness) + "\n"
              + "Best mutated chromosome:\n" + str(best_chromosome))
        print("\n")

        # Check if there is a new best chromosome
        if final_fitness > best_fitness:
            final_fitness = best_fitness
            best_mutated_chromosome = best_chromosome

    print("Best fitness found: " + str(final_fitness))
    print("Best chromosome found: " + str(best_mutated_chromosome))

    circuit = Circuit(best_mutated_chromosome)
    circuit.generate_circuit()
    print(desired_chance_of_one)
    circuit.print_ca_outcomes()
    circuit.draw()
