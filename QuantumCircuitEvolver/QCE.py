# Written by Sebastian T. Overskott 2022. Github link: https://github.com/Overskott/Evolving-quantum-circuits

from quantum_circuit_evolver import *

# DONE: Documentation and comments
# TODO: Error and exception handling
# TODO: Unit testing

# Suggestions:
# Add "softer" mutation i.e. just swapping connected qubits
# Make the FF more punishing for bad solutions
# Add crossover mutation

if __name__ == '__main__':
    gates = 10
    chromosomes = 10
    generations = 30

    # desired_chance_of_one = [1, 0, 1, 0, 0, 1, 0, 1]  # Very good results
    #desired_chance_of_one = [0.5, 0.7, 0.4, 0.0, 0.2, 0.7, 0.1, 0.9]  # Good results
    # desired_chance_of_one = [1, 1, 1, 1, 1, 1, 1, 1]  # Bad results
    # desired_chance_of_one = [0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8]  # Bad result
    # desired_chance_of_one = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # very good
    desired_chance_of_one = [1.0, 0.5, 1.0, 0.0, 0.0, 1.0, 0.5, 0.0]  # Ok results

    # Generate initial generation of chromosomes
    init_gen = Generation(10, gates)
    init_gen.create_initial_generation()

    init_gen.print_chromosomes()
    init_gen.print_theta_values()
    init_gen.print_circuits()

    init_gen.run_generation(desired_chance_of_one)

    init_gen.print_fitness()

    print("Fitness for best chromosome: " + str(init_gen.get_best_fitness()) + "\n"
          + "Best chromosome: \n" + str(init_gen.get_best_chromosome()))
    print("\n")

    # Final value placeholders
    current_chromosome = init_gen.get_best_chromosome()
    best_chromosome = current_chromosome
    final_fitness = init_gen.get_best_fitness()

    # Mutation loop
    for gen in range(0, generations):

        # Mutate next generation of chromosomes
        next_gen = Generation(chromosomes, gates)
        next_gen.create_mutated_generation(current_chromosome)

        next_gen.print_chromosomes()
        # Check every Chromosome's fitness
        next_gen.run_generation(desired_chance_of_one)

        # Print generation best result
        print("Fitness for best mutated chromosome in mutation " + str(gen + 1) + ": " + str(next_gen.get_best_fitness()) + "\n"
              + "Best mutated chromosome:\n" + str(next_gen.get_best_chromosome()))
        print("------------------------------------------------------------------------------")
        print("\n")

        # Check if there is a new_list best chromosome
        current_fitness = next_gen.get_best_fitness()
        if final_fitness > current_fitness:
            final_fitness = current_fitness
            best_chromosome = current_chromosome
            if final_fitness < 0.01:
                break
            print("New best!")
            print("------------------------------------------------------------------------------")
            print("\n")

    print("Best fitness found: " + str(final_fitness))
    print("Best chromosome found: " + str(best_chromosome))

    circuit = Circuit(best_chromosome)
    circuit.print_ca_outcomes(desired_chance_of_one)
    print("\n")

    circuit.generate_circuit()
    circuit.draw()
