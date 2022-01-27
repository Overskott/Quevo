#  Copyright 2022 Sebastian T. Overskott Github link: https://github.com/Overskott/Quevo
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import Quevo

# DONE: Documentation and comments
# TODO: Error and exception handling
# TODO: Unit testing

if __name__ == '__main__':
    gates = 5
    chromosomes = 10
    generations = 100
    gate_types = ['cx', 'x', 'h', 'rxx', 'rzz', 'swap', 'z', 'y', 'toffoli']

    desired_chance_of_one = [0.394221, 0.094721, 0.239492, 0.408455, 0.0, 0.730203, 0.915034, 1.0]
    # Probabilities from : https://link.springer.com/article/10.1007/s11571-020-09600-x

    # Generate initial generation of chromosomes
    init_gen = Quevo.Generation(10, gates)
    init_gen.create_initial_generation(gate_types)

    init_gen.run_generation_diff(desired_chance_of_one)

    print("Fitness for best chromosome: " + str(init_gen.get_best_fitness()) + "\n"
          + "Best chromosome: \n" + str(init_gen.get_best_chromosome()))
    print("\n")

    # Final value placeholders
    current_chromosome = init_gen.get_best_chromosome()
    best_chromosome = current_chromosome
    final_fitness = init_gen.get_best_fitness()

    final_fitness_list = [final_fitness]
    random_list = [final_fitness]
    list_10 = [final_fitness]
    list_50 = [final_fitness]
    list_70 = [final_fitness]

    # Mutation loop

    for gen in range(0, generations):

        # Mutate next generation of chromosomes
        next_gen = Quevo.Generation(chromosomes, gates)
        next_gen.create_mutated_generation(current_chromosome, 30)

        # Check every Chromosome's fitness
        next_gen.run_generation_KL(desired_chance_of_one)

        current_fitness = next_gen.get_best_fitness()
        current_chromosome = next_gen.get_best_chromosome()

        # Print generation best result
        print("Fitness for best mutated chromosome in mutation " + str(gen + 1) + ": "
              + str(current_fitness) + "\n"
              + "Best mutated chromosome:\n" + str(next_gen.get_best_chromosome()))
        print("------------------------------------------------------------------------------")
        print("\n")

        # Check if there is a new_list best chromosome

        if final_fitness > abs(current_fitness):
            final_fitness = current_fitness
            best_chromosome = current_chromosome
            print("New best!")
            print("------------------------------------------------------------------------------")
            print("\n")

        if current_fitness < 0.01:
            break
    print("Best fitness found: " + str(final_fitness))
    print("Best chromosome found: " + str(best_chromosome))

    circuit = Quevo.Circuit(best_chromosome)
    circuit.print_ca_outcomes(desired_chance_of_one)
    print("\n")

    circuit.generate_circuit()
    circuit.draw()
