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

import copy
from typing import List
from .Chromosome import Chromosome
from .Circuit import Circuit


class Generation(object):
    """
    This class represents a collection of chromosomes. The Collection is called a
    generation.

    Attributes
    ----------
    chromosome_list: List[int]
        List of chromosomes that habits the generation.
    fitness_list: List[float]
        list of fitness scores corresponding to the chromosomes in chromosome_list.
    _chromosomes: int
        The number of chromosomes in the generation
    _gates: int
        Number of gates in each chromosome.
    """

    def __init__(self, chromosomes: int, gates: int) -> None:
        """
        The Generation constructor.

        Parameters
        ----------
        chromosomes (int):
            Number of chromosomes in the generation.
        gates (int):
            Number of gates in each chromosome.
        """
        self.chromosome_list: List[Chromosome] = []
        self.fitness_list: List[float] = []
        self._chromosomes: int = chromosomes
        self._gates: int = gates

    def create_initial_generation(self, gate_types: List[str]) -> None:
        """
        Populates the generation with chromosomes.
        """
        self.chromosome_list.clear()
        for i in range(self._chromosomes):
            chromosome = Chromosome(gate_types)
            chromosome.generate_random_chromosome(self._gates)
            self.chromosome_list.append(chromosome)

    def create_mutated_generation(self, parent: Chromosome, probability=70) -> None:
        """
        Populates the generation with mutated chromosomes. The parent in included as the first member of the next
        generation. The mutated chromosomes uses parameter parent as source for mutation.

        Parameters
        ----------
        parent (Chromosome):
            The chromosome all mutations will be generated from.
        """

        self.chromosome_list.clear()
        self.chromosome_list.append(parent)
        for i in range(self._chromosomes-1):
            mutated_chromosome = copy.deepcopy(parent)
            mutated_chromosome.mutate_chromosome(probability)
            self.chromosome_list.append(mutated_chromosome)

    def run_generation_diff(self, desired_outcome: List[float]) -> None:
        """
        Runs the simulator for all the chromosomes in the generation and
        stores the fitness for each chromosome in fitness_list.

        Parameters
        ----------
        desired_outcome (List[float]):
            A list of the eight CA outcomes we wish to test the chromosomes against.
        """

        for chromosome in self.chromosome_list:
            circuit = Circuit(chromosome)
            chromosome_fitness = abs(circuit.find_chromosome_fitness(desired_outcome))
            self.fitness_list.append(chromosome_fitness)

    def run_generation_KL(self, desired_outcome: List[float]) -> None:
        """
        Runs the simulator for all the chromosomes in the generation and
        stores the fitness for each chromosome in fitness_list.

        Parameters
        ----------
        desired_outcome (List[float]):
            A list of the eight CA outcomes we wish to test the chromosomes against.
        """

        for chromosome in self.chromosome_list:
            circuit = Circuit(chromosome)
            chromosome_fitness = abs(circuit.find_kullback_liebler_fitness(desired_outcome))
            self.fitness_list.append(chromosome_fitness)

    def get_best_fitness(self):
        """Returns the fitness value for the best chromosome in the generation."""
        best_fitness = min(self.fitness_list)
        return best_fitness

    def get_best_chromosome(self):
        """Returns the chromosome with the best fitness in the generation."""
        best_fitness_index = self.fitness_list.index(self.get_best_fitness())
        best_chromosome = self.chromosome_list[best_fitness_index]
        return best_chromosome

    def print_chromosomes(self):
        """Prints all the generation's chromosomes."""
        print("Chromosomes: ")
        for chromosome in self.chromosome_list:
            print(chromosome)
        print('\n')

    def print_theta_values(self):
        """Prints all the generation's theta values."""
        print("Theta values: ")
        for chromosome in self.chromosome_list:
            print(chromosome.get_theta_list())
        print('\n')

    def print_circuits(self):
        """Prints all the generation's chromosome's circuits."""
        print("Circuits: ")
        for chromosome in self.chromosome_list:
            circuit = Circuit(chromosome)
            circuit.generate_circuit()
            circuit.draw()
        print("\n")

    def print_fitness(self):
        """Prints the generation's chromosome's fitness"""
        for fitness in self.fitness_list:
            print(fitness)
        print("\n")
