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
        """
        Test that constructor instantiates the objects with the correct parameters.
        """
        c = Cell()
        assert c.fodder == 0
        assert isinstance(c.current_carnivores, list)
        assert isinstance(c.current_herbivores, list)

    def test_n_herbivores(self):
        """
        Tests that n_herbivores property returns correct amount of herbivores.
        """
        nr_herbs = 10
        c = Cell()
        c.current_herbivores = [Herbivore() for _ in range(nr_herbs)]
        assert c.n_herbivores == nr_herbs

    def test_n_carnivores(self):
        """
        Tests that n_carnivores property returns correct amount of carnivores.
        """
        nr_carns = 10
        c = Cell()
        c.current_carnivores = [Carnivore() for _ in range(nr_carns)]
        assert c.n_carnivores == nr_carns

    def test_n_animals(self):
        """
        Tests that n_animals property returns a tuple with number of carnivores and herbivores in
        each cell.
        """
        nr_carns = 15
        nr_herbs = 10
        c = Cell()
        c.current_herbivores = [Herbivore() for _ in range(nr_herbs)]
        c.current_carnivores = [Carnivore() for _ in range(nr_carns)]
        assert c.n_animals == (10, 15)

    @pytest.mark.parametrize('FerCells', [Lowland, Highland])
    def test_grow_fodder(self, FerCells):
        c = FerCells()
        c.grow_fodder()
        assert c.fodder == c.params['f_max']

    @pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_place_animals(self, Species):

        c = Cell()
