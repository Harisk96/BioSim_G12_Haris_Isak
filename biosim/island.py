#LEGGER MAPPET MIDLERTIDIG INN I DENNE FILEN:

default_map_string = """
WWWWWWWWWWWWWWWWWWWWW
WWWWWWWWHWWWWLLLLLLLW
WHHHHHLLLLWWLLLLLLLWW
WHHHHHHHHHWWLLLLLLWWW
WHHHHHLLLLLLLLLLLLWWW
WHHHHHLLLDDLLLHLLLWWW
WHHLLLLLDDDLLLHHHHWWW
WWHHHHLLLDDLLLHWWWWWW
WHHHLLLLLDDLLLLLLLWWW
WHHHHLLLLDDLLLLWWWWWW
WWHHHHLLLLLLLLWWWWWWW
WWWHHHHLLLLLLLWWWWWWW
WWWWWWWWWWWWWWWWWWWWW"""


from biosim.landscape import Highland, Lowland, Desert, Sea
from biosim.animals import Herbivore, Carnivore
import textwrap

import numpy as np


def check_length(strings):
    strings = list(map(len, strings))
    if strings.count(strings[0]) == len(strings):
        return True

class Island:

    cell_types = {'H': Highland,
                  'L': Lowland,
                  'D': Desert,
                  'W': Sea}


    def __init__(self, insert_map, init_animals):
        """
        Constructor for Island class
        :param maps: List, nested list as a matrix describing the layout of the island geography
        :param init_animals: ,
        """

        self.map = self.set_map_coordinates(insert_map)

       if init_animals is None:
            self.place_population(Island.default_herbivores)

#        y, x = loc
#        cell_left = (y, x-1)
#        cell_right = (y, x+1)
#        cell_up = (y+1, x)
#        cell_down = (y-1, x)
#        destination_cells = [cell_left, cell_right, cell_up, cell_down]

        self.destinations = destination_cells

#        self.len_x_coord = None
#        self.len_y_coord = None

        # self.maps = self.set_map_coordinates(map_input)

#        self.place_population_map(SETTE INN STARTPOPULASJON HER)

    def check_map(self, map_input):
        stringmap = map_input.strip()
        strings = stringmap.split('\n')

        if not check_length(strings):
            raise ValueError('Every line in stringmap must be of equal length')

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

        #        strings = self.check_map(map)
        #
        #        map_island = {}
        #        self.len_x_coord = len(strings[0])
        #        self.len_y_coord = len(strings)

        strings_island_map = self.check_map(map_input)
        coordinates_map = {}
        for y_index, line in enumerate(strings_island_map):
            for x_index, cell in enumerate(line):
                cell_instance = self.cell_types[cell]
                coordinates_map[(y_index, x_index)] = cell_instance
        return coordinates_map



    def procreate_cells_map(self):
        pass

    def feed_cells(self):
        for landscape in self.map.values():
            landscape.feed_all()


    def age_in_cells(self):
        pass

    def weightloss_cell(self):
        pass

    def place_population(self, init_pop):
        for position in population:
            loc = position['loc']
            if loc not in self.map.keys():
                raise ValueError('nonexistent loc in the map provided')
            if loc in self.map[loc] = self.cell_types['W']: #Rette opp denne
                raise ValueError('Animal can not live in water')
            pop = position['pop']
            self.map[loc].place_animals(pop)

    def migrate(self):
        pass

    # I FUNKSJONEN UNDER SKAL VI KALLE PÅ FUNKSJONER FRA ISLAND CELLEN FOR Å KJØRE GJENNOM ETT ÅR
    def run_function_one_year(self):
        pass
