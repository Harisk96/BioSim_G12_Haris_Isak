from biosim.animals import Herbivore, Carnivore, Animals
from biosim.landscape import Cell, Lowland, Highland, Desert, Sea
from biosim.island import Island
import pytest
import textwrap

__author__ = 'Haris Karovic', 'Isak Finnøy'
__email__ = 'harkarov@nmbu.no', 'isfi@nmbu.no'

ini_herbs = [{'loc': (10, 9),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
ini_carns = [{'loc': (10, 9),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(40)]}]
default_population = ini_herbs + ini_carns

default_maps = """
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

default_maps = textwrap.dedent(default_maps)

class TestIsland:
    """
    Class that tests island class.
    """
    def test_constructor(self):
        """
        Tests the constructor of the island class
        """
        i = Island(default_maps, default_population)
        assert hasattr(i, 'map')
        assert hasattr(i, 'place_population')
        assert hasattr(i, '_year')

