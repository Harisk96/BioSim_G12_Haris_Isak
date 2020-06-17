# LEGGER MAPPET MIDLERTIDIG INN I DENNE FILEN:

import random
from biosim.landscape import Highland, Lowland, Desert, Sea
from biosim.animals import Animals, Herbivore, Carnivore
import textwrap

import numpy as np

class Island:
    cell_types = {'H': Highland,
                  'L': Lowland,
                  'D': Desert,
                  'W': Sea}

    def __init__(self, insert_map, init_animals):
        """
        Constructor for Island class
        :param insert_map: str, strings ordered in a square pattern
        :param init_animals: list, list of dictionary, places herbivores and carnivores on the map
        """

        self.map = self.set_map_coordinates(insert_map)
        self.place_population(init_animals)
        self._year = 0



    @staticmethod
    def check_length(strings):
        """
        Determines whether the strings that are passed to it have the same length.
        :param strings: Str, strings that constitute the map of the island.
        :return: Bool, according to whether the input strings have the same length or not
        """
        strings = list(map(len, strings))

        if strings.count(strings[0]) == len(strings):
            return True

    @property
    def year(self):
        """
        Property that returns the current year of the simulation
        :return: int
        """
        return self._year

    @year.setter
    def year(self, current_year):
        """
        Setter that sets the year property to its current value.
        :param current_year: int, positive integer that is the current year of the simulation.
        :return: int
        """
        self._year = current_year

    @property
    def num_animals(self):
        """
        Returns the total number of animals currently on the island.
        :return: int, positive integer, number of animals currently on the island.
        """
        num_animals = 0
        for cell in self.map.values():
            num_animals += cell.n_herbivores + cell.n_carnivores
        return num_animals

    @property
    def num_animals_per_species(self):
        """
        Returns a dictionary with number of herbivores and carnivores.
        :return: dict
        """

        num_animals_per_species = {'Herbivore': 0, 'Carnivore': 0}
        for cell in self.map.values():
            num_animals_per_species['Herbivore'] += cell.n_herbivores
            num_animals_per_species['Carnivore'] += cell.n_carnivores
        return num_animals_per_species


    def fitness_list(self):
        """
        Returns lists of the fitness of the carnivores and herbivores currently on the island.
        :return: list, two lists
        """

        herbfit_list = []
        for cell in self.map.values():
            for herb in cell.current_herbivores:
                herbfit_list.append(herb.fitness)

        carnfit_list = []
        for cell in self.map.values():
            for carn in cell.current_carnivores:
                carnfit_list.append(carn.fitness)

        return herbfit_list, carnfit_list

    def age_list(self):
        """
        Returns lists of the ages of the herbivores and carnivores currently on the island
        :return: list, two lists
        """

        herbage_list = []
        for cell in self.map.values():
            for herb in cell.current_herbivores:
                herbage_list.append(herb.age)

        carnage_list = []
        for cell in self.map.values():
            for carn in cell.current_carnivores:
                carnage_list.append(carn.age)

        return herbage_list, carnage_list

    def weight_list(self):
        """
        List of the weights of the herbivores and carnivores currently on the island.
        :return: list, two lists
        """

        herbweight_list = []
        for cell in self.map.values():
            for herb in cell.current_herbivores:
                herbweight_list.append(herb.weight)

        carnweight_list = []
        for cell in self.map.values():
            for carn in cell.current_carnivores:
                carnweight_list.append(carn.weight)

        return herbweight_list, carnweight_list

    def check_map(self, map_input):
        """
        Method that checks that the input map has the necessary properties, and that they are valid.
        :param map_input: str, arranged in a matrix.
        :return: str
        """
        stringmap = map_input.strip()
        strings = stringmap.split('\n')

        if not self.check_length(strings):
            raise ValueError('Every line in stringmap must be of equal length')

        for row in strings:
            for cell in row:
                if cell not in Island.cell_types:
                    raise ValueError("Invalid code for landscape type.")

        for elems in str([strings[0] + strings[-1]])[2:-2]:
            if elems != 'W':
                raise ValueError('Not island, island must be surrounded by water'
                                 ', error on southside or northside')

        for elems in strings:
            if not elems.startswith('W'):
                raise ValueError('Not island, island must be surrounded by water,'
                                 ' error on westside')

        for elems in strings:
            if not elems.endswith('W'):
                raise ValueError('Not island, island must be surrounded by water, '
                                 'error on eastside')

        return strings

    def set_map_coordinates(self, map_input):

        strings_island_map = self.check_map(map_input)


        coordinates_map = {}  # []
        for y_index, line in enumerate(strings_island_map):
            for x_index, cell in enumerate(line):
                cell_instance = self.cell_types[cell]()
                coordinates_map[(y_index+1, x_index+1)] = cell_instance
        return coordinates_map

    def procreate_cells_map(self):
        for cell in self.map.values():
            cell.birth_cycle()


    def feed_cells_island(self):
        """
        Method that updates the fodder in the cell,
        and makes all the animals it contains eat.
        :return:
        """
        for landscape in self.map.values():
            landscape.feed_all()

    def age_in_cells(self):
        """
        Method that ages the animals in the cell by one year.
        :return:
        """
        for cell in self.map.values():
            cell.age_animals()

    def weightloss_island(self):
        """
        Method that makes it so that animals in the cell loses
        weight.
        :return: None
        """
        for cell in self.map.values():
            cell.weight_loss_cell()

    def die_island(self):

        for cell in self.map.values():
            cell.death_in_cell()

    def place_population(self, init_pop):
        """
        Method that places animals in the cells that constitutes the island
        :param init_pop: list of dict, animals to be placed on the island
        :return: None
        """
        for position in init_pop:
            loc = position['loc']
            if loc not in self.map.keys():
                raise KeyError('nonexistent loc in the map provided')
            if not self.map[loc].migrate_to:  # IKKE SIKKERT DENNE FUNGERER
                raise ValueError('Animal can not live in water')
            pop = position['pop']
            self.map[loc].place_animals(pop)

    def map_size(self):
        coordinates = self.map.keys()
        list_of_coordinates = list(coordinates)
        size = list_of_coordinates[-1]
        return size

    def get_adj_cells(self, coords):
        y, x = coords
        adjacent_cells = [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]
        return adjacent_cells

    def migration_island(self):

        for y, coords in enumerate(self.map):
            self.get_adj_cells(coords)
            if self.map[coords].migrate_to:
                adjacent_cells = self.get_adj_cells(coords)
                migrants_dict = self.map[coords].emigration(adjacent_cells)

                for destination, migrant in migrants_dict.items():
                    if self.map[destination].migrate_to and migrant:
                        self.map[destination].add_immigrants(migrant)
                        self.map[coords].remove_emigrants(migrant)


    # I FUNKSJONEN UNDER SKAL VI KALLE PÅ FUNKSJONER FRA ISLAND CELLEN FOR Å KJØRE GJENNOM ETT ÅR
    def run_function_one_year(self):
        self.fitness_list()
        self.age_list()
        self.weight_list()
        self.feed_cells_island()
        self.procreate_cells_map()
        self.migration_island()
        self.age_in_cells()
        self.weightloss_island()
        self.die_island()
        self.year += 1

        for cell in self.map.values():
            for anim in cell.current_herbivores + cell.current_carnivores:
                anim.set_has_migrated(False)




if __name__ == "__main__":
    i = Island