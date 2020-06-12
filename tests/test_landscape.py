from biosim.animals import Herbivore, Carnivore, Animals
from biosim.landscape import Cell, Lowland, Highland, Desert, Sea
import pytest
from unittest import mock

__author__ = "Haris Karovic", "Isak Finnøy"
__email__ = "harkarov@nmbu.no", "isfi@nmbu.no"

def set_params():
    """
    Sets the testing environment up.
    """
    low_params = {'f': 800, 'migrate_to': True}
    high_params = {'f': 300, 'migrate_to': True}
    desert_params = {'migrate_to': True}
    sea_params = {'migrate_to': False}

    Highland.set_params(**high_params)
    Lowland.set_params(**low_params)
    Desert.set_params(**desert_params)
    Sea.set_params(**sea_params)

class TestLandscape:
    """
    Class for testing the methods of landscape-file.
    """
    #@pytest.mark.parametrize('FerCells', [Lowland, Highland])
    #@pytest.mark.parametrize('InferCells', [Desert, Sea])
    def test_constructor(self):
        c = Cell()
        assert c.fodder == 0
        assert isinstance(c.current_carnivores, list)
        assert isinstance(c.current_herbivores, list)
