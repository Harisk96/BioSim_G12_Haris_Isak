#LEGGER MAPPET MIDLERTIDIG INN I DENNE FILEN:

geogr = """
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

import numpy as np

def check_length(strings):
    strings = list(map(len, strings))
    if strings.count(strings[0]) == len(strings):
        return True

class Island:



    cell_types = {'H': Highland,
                  'L': Lowland,
                  'D': Desert,
                  'S': Sea}

    def __init__(self, letter_map, init_animals):
        self.map = self.create_map(geogr)
        self.place_population(SETTE INN STARTPOPULASJON HER)

    def clean_stringmap(stringmap):
        stringmap = stringmap.strip()
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



    def procreate_cells_map(self):
        pass

    def feed_cells(self):
        pass

    def create_map(self):
        pass

    def place_herbivores(self):
        pass

    def age_in_cells(self):
        pass

    def weightloss_cell(self):
        pass

    def place_population(self):
        pass

    def migrate(self):
        pass

    # I FUNKSJONEN UNDER SKAL VI KALLE PÅ FUNKSJONER FRA ISLAND CELLEN FOR Å KJØRE GJENNOM ETT ÅR
    def run_function_one_year(self):
        pass
