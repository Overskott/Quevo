from quantum_circuit_evolver import *

# TODO: Setting up unit testing
# TODO: Documentation and comments
# TODO: Error and exception handling

if __name__ == '__main__':
    gates = 5
    chromosomes = 10
    genes = gates * 3
    generations = 20
    desired_chance_of_one = [0.5, 0.3, 0.4, 0, 0.5, 0.2, 0, 0.9]

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

    print("Circuits: ")
    for chromosome in init_gen.chromosome_list:
        circuit = Circuit(chromosome)
        circuit.generate_circuit()
        circuit.draw()



    input()

    # Print initial generation

    for chromosome in init_gen:
        print(chromosome)


    # Check every Chromosome's fitness
    fitness_list = generated_circuit.run_generation(init_gen)

    # Print initial gen fitness best result
    best_fitness = min(fitness_list)
    min_index = fitness_list.index(best_fitness)

    best_chromosome = init_gen[min_index]

    print("Fitness for best chromosome: " + str(best_fitness) + "\n"
          + "Best chromosome: \n" + str(best_chromosome))
    print("\n")

    # Mutation loop

    best_mutated_chromosome = []
    final_fitness = 8

    for gen in range(0, generations):

        # Mutate next generation of chromosomes
        mutated_circuit = Circuit(gates)
        mutated_gen = create_mutated_generation(
            chromosomes, best_chromosome)

        # Print mutated generation
        print("Mutated generation " + str(gen + 1) + ": ")
        for chromosome in mutated_gen:
            print(chromosome)
        print('\n')

        # Check every Chromosome's fitness
        mutated_fitness_list = mutated_circuit.run_generation(mutated_gen)

        # Print generation best result
        best_fitness = min(mutated_fitness_list)
        min_index = mutated_fitness_list.index(best_fitness)

        best_chromosome = mutated_gen[min_index]
        print("Fitness for best mutated chromosome: " + str(best_fitness) + "\n"
              + "Best mutated chromosome:\n" + str(best_chromosome))
        print("\n")

        # Check if there is a new best chromosome
        if final_fitness > best_fitness:
            final_fitness = best_fitness
            best_mutated_chromosome = best_chromosome

    print("Best fitness found: " + str(final_fitness))
    print("Best chromosone found: " + str(best_mutated_chromosome))


