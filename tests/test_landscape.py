from biosim.animals import Herbivore, Carnivore, Animals
from biosim.landscape import Cell, Lowland, Highland, Desert, Sea
import pytest
import numpy as np
from operator import attrgetter
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

    def test_grow_fodder_Sea(self):
        w = Sea()
        assert w.grow_fodder() is None

    #@pytest.mark.parametrize('Species', [Herbivore, Carnivore])
    def test_place_animals(self):
        c = Cell()
        h_list = [Herbivore() for _ in range(10)]
        c_list = [Carnivore() for _ in range(15)]
        with pytest.raises(TypeError, match='list_of_animals has to be of type list'):
            assert c.place_animals("string")
        assert c.place_animals(h_list) == c.current_herbivores.append(h_list)
        assert c.place_animals(c_list) == c.current_carnivores.append(c_list)

    def test_birth_cycle(self, mocker):
        """
        c = Cell()
        mocker.patch("", return_value=Herbivore)
        c.n_herbivores = 10
        c.current_herbivores = [Herbivore() for _ in range(c.n_herbivores)]
        h_list = [Herbivore.birth() for _ in range(c.n_herbivores)]
        assert c.birth_cycle() == c.current_herbivores.append(h_list)
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        l = Lowland()
        l.current_herbivores = [Herbivore(5,100), Herbivore(5,100)]
        l.current_carnivores = [Carnivore(5,100), Carnivore(5,100)]
        l.birth_cycle()

        assert len(l.current_herbivores) >= 3
        assert len(l.current_carnivores) >= 3

    def test_death_in_cell(self):

        c = Cell()
        c.current_herbivores = [Herbivore(5,0), Herbivore(5,100), Herbivore(3,0)]
        c.current_carnivores = [Carnivore(2,0), Carnivore(5,100), Carnivore(5,100)]
        c.current_herbivores[0].fitness = 0
        c.current_herbivores[1].fitness = 1
        c.current_herbivores[2].fitness = 0
        c.current_carnivores[0].fitness = 0
        c.current_carnivores[1].fitness = 1
        c.current_carnivores[2].fitness = 1
        c.death_in_cell()

        assert len(c.current_herbivores) == 1
        assert len(c.current_carnivores) == 2


    def test_weight_loss(self):
        c = Cell()
        c.current_herbivores = [Herbivore(2, 10.0) for _ in range(10)]
        c.current_carnivores = [Carnivore(2, 10.0) for _ in range(10)]
        c.weight_loss()
        for i in range(10):
            assert c.current_herbivores[i].weight < 10.0
            assert c.current_carnivores[i].weight < 10.0

    def test_feed_herbivore(self):
        c = Cell()
        weight = 5.0
        c.current_herbivores = [Herbivore(2, weight) for _ in range(10)]
        c.fodder = 0
        c.feed_herbivores()
        for herb in c.current_herbivores:
            assert herb.weight - weight == pytest.approx(0)

        c.fodder = 100
        c.feed_herbivores()
        for herb in c.current_herbivores:
            assert herb.weight - weight > 0

    def test_feed_carnivore(self):
        c = Cell()
        c.current_carnivores = [Carnivore(4, 8.0), Carnivore(2, 4.0), Carnivore(6, 12.0)]
        c.current_herbivores = [Herbivore(6, 6.0), Herbivore(2, 2.0), Herbivore(4, 4.0)]
        c.feed_carnivores()
        assert c.current_carnivores[0].fitness > c.current_carnivores[1].fitness
        assert c.current_carnivores[1].fitness > c.current_carnivores[2].fitness
        assert c.current_herbivores[0].fitness < c.current_herbivores[1].fitness
        assert c.current_herbivores[1].fitness < c.current_herbivores[2].fitness

    @pytest.mark.parametrize('FerCells', [Lowland, Highland])
    def test_feed_all(self, FerCells):
        fc = FerCells()
        fc.feed_all()
        assert fc.fodder == fc.params['f_max']

    def test_age_animals(self):
        l = Lowland()
        l.current_carnivores = [Carnivore(1,1), Carnivore(3,3)]
        l.current_herbivores = [Herbivore(9,9), Herbivore(2,2)]
        l.age_animals()
        assert l.current_carnivores[0].age == 2
        assert l.current_carnivores[1].age == 4
        assert l.current_herbivores[0].age == 10
        assert l.current_herbivores[1].age == 3


if __name__ == "__main__":
    c = Cell()
    c.current_herbivores = [Herbivore(6, 6.0), Herbivore(2, 2.0), Herbivore(4, 4.0)]
    h = c.current_herbivores
    print(h[2])