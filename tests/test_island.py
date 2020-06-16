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

    def test_year_property(self):
        """
        Tests if year-property returns the value of the year-attribute
        """
        i = Island(default_maps, default_population)
        i._year = 3
        assert i.year == 3

    def test_num_animals(self):
        i = Island(default_maps, default_population)
        assert i.num_animals == 190

    def test_num_per_species(self):
        i = Island(default_maps, default_population)
        exp_dict = {'n_herbs': 150, 'n_carns': 40}
        assert i.num_animals_per_species == exp_dict

    def test_check_map(self):
        i = Island(default_maps, default_population)
        checked_map = i.check_map(default_maps)
        assert isinstance(checked_map, list)
        for i in checked_map:
            assert isinstance(i, str)
            assert len(i) == 21

    def test_check_map_exceptions(self):
        pass

    def test_fitness_list(self):
        """
        Method that tests that fitness_list returns the fitness of the current herbivores on the
        island.
        """
        i = Island(default_maps, default_population)
        fit_list = i.fitness_list()
        h_fit_list = fit_list[0]
        c_fit_list = fit_list[1]
        h = Herbivore(5, 20)
        c = Carnivore(5, 20)
        for i in h_fit_list:
            assert i == pytest.approx(h.fitness)
        for i in c_fit_list:
            assert i == pytest.approx(c.fitness)
        assert isinstance(h_fit_list, list)
        assert isinstance(c_fit_list, list)

    def test_age_list(self):
        i = Island(default_maps, default_population)
        age_list = i.age_list()
        h_age_list = age_list[0]
        c_age_list = age_list[1]
        h = Herbivore()
        h.age = 5
        c = Carnivore()
        c.age = 5
        for i in h_age_list:
            assert i == h.age
        for i in c_age_list:
            assert i == c.age
        assert(h_age_list, list)
        assert(c_age_list, list)

    def test_weight_list(self):
        i = Island(default_maps, default_population)
        weight_list = i.weight_list()
        h_weight_list = weight_list[0]
        c_weight_list = weight_list[1]
        h = Herbivore()
        h.weight = 20
        c = Carnivore()
        c.weight = 20
        for i in h_weight_list:
            assert i == h.weight
        for i in c_weight_list:
            assert i == c.weight
        assert isinstance(h_weight_list, list)
        assert isinstance(c_weight_list, list)

    def test_set_coordinates_map(self):
        i = Island(default_maps, default_population)
        cords_dict = i.set_map_coordinates(default_maps)
        assert isinstance(cords_dict, dict)

    def test_procreation_cells_map(self, mocker):
        mocker.patch("numpy.random.uniform", return_value=0)
        ini_herbs = [{'loc': (10, 9),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 40}
                              for _ in range(20)]}]
        ini_carns = [{'loc': (10, 9),
                      'pop': [{'species': 'Carnivore',
                               'age': 5,
                               'weight': 40}
                              for _ in range(20)]}]
        fertile_population = ini_herbs + ini_carns
        i = Island(default_maps, fertile_population)
        i.procreate_cells_map()
        assert i.num_animals_per_species['n_herbs'] > 20
        assert i.num_animals_per_species['n_carns'] > 20
        assert i.num_animals > 40

    def test_feed_cells(self):
        i = Island(default_maps, default_population)
        old_weight_herb = i.weight_list()
        i.feed_cells_island()

