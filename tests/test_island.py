from biosim.animals import Herbivore, Carnivore, Animals
from biosim.landscape import Cell, Lowland, Highland, Desert, Sea
import pytest

__author__ = 'Haris Karovic', 'Isak Finnøy'
__email__ = 'harkarov@nmbu.no', 'isfi@nmbu.no'

class TestIsland:
    """
    Class that tests island class.
    """
    def test_constructor(self):
