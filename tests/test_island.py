from biosim.animals import Herbivore, Carnivore, Animals
from biosim.landscape import Cell, Lowland, Highland, Desert, Sea
from biosim.island import Island
import pytest
import textwrap

__author__ = 'Haris Karovic', 'Isak Finnøy'
__email__ = 'harkarov@nmbu.no', 'isfi@nmbu.no'

ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
ini_carns = [{'loc': (10, 10),
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
        exp_dict = {'Herbivore': 150, 'Carnivore': 40}
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
        assert i.num_animals_per_species['Herbivore'] > 20
        assert i.num_animals_per_species['Carnivore'] > 20
        assert i.num_animals > 40

    def test_feed_cells(self):
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
        feeding_population = ini_carns + ini_herbs
        i = Island(default_maps, feeding_population)
        old_weights_herb = i.weight_list()[0]
        old_weights_carn = i.weight_list()[1]
        i.feed_cells_island()
        new_weights_herb = i.weight_list()[0]
        new_weights_carn = i.weight_list()[1]
        assert sum(new_weights_carn) > sum(old_weights_carn)
        assert sum(new_weights_herb)/len(new_weights_herb) > \
               sum(old_weights_herb)/len(old_weights_herb)

    def test_age_in_cells(self):
        i = Island(default_maps, default_population)
        i.age_in_cells()

        for cell in i.map.values():
            if cell.migrate_to:
                for herb in cell.current_herbivores:
                    assert herb.age == 6
                for carn in cell.current_carnivores:
                    assert carn.age == 6

    def test_weight_loss(self):
        i = Island(default_maps, default_population)
        old_weights_herb = i.weight_list()[0]
        old_weights_carn = i.weight_list()[1]
        i.weightloss_island()
        new_weights_herb = i.weight_list()[0]
        new_weights_carn = i.weight_list()[1]
        assert sum(new_weights_carn) < sum(old_weights_carn)
        assert sum(new_weights_herb) < sum(old_weights_herb)

    def test_die_island(self, mocker):
        mocker.patch("numpy.random.uniform", return_value=0)
        i = Island(default_maps, default_population)
        old_n_herbs = i.num_animals_per_species['Herbivore']
        old_n_carns = i.num_animals_per_species['Carnivore']
        i.die_island()
        for cell in i.map.values():
            assert len(cell.current_herbivores) < old_n_herbs
            assert len(cell.current_carnivores) < old_n_carns

    def test_place_animals(self):
        i = Island(default_maps, default_population)
        hlist = [{'loc': (10, 9),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 40}
                              for _ in range(10)]}]
        i.place_population(hlist)
        assert i.num_animals == 200
        badlist = [{'loc': (-1, -1),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 40}
                              ]}]
        with pytest.raises(KeyError):
            assert i.place_population(badlist)
        badlist2 = [{'loc': (1, 1),
                    'pop': [{'species': 'Herbivore',
                             'age': 5,
                             'weight': 40}
                            ]}]
        with pytest.raises(ValueError):
            assert i.place_population(badlist2)

    def test_map_size(self):
        """
        Asserts that the map_size method returns the dimensions.
        """
        i = Island(default_maps, default_population)
        assert i.map_size() == (13, 21)

    def test_get_adj_cells(self):
        """
        Asserts that the get_adj_cells method returns the adjacent cells, and which are not
        diagonally placed relatively to the current cell.
        """
        i = Island(default_maps, default_population)
        adjacent_cells = [(11, 10), (9, 10), (10, 11), (10, 9)]
        assert i.get_adj_cells((10, 10)) == adjacent_cells

    def test_migration_island(self, mocker):
        """
        Asserts that the Island method migration_island migrates animals to an adjacent cell.
        For the sake of simplicity, we mock out the numpy.random.randint to always return the same
        adjacent cell, in this case (11, 10). Asserts that number of animals present in the cell
        increases from zero to a number larger than zero.
        """
        mocker.patch("numpy.random.randint", return_value=0)
        i = Island(default_maps, default_population)
        old_pop_destination = i.map[11, 10].n_herbivores + i.map[(11, 10)].n_carnivores
        i.migration_island()
        new_pop_destination = i.map[11, 10].n_herbivores + i.map[(11, 10)].n_carnivores
        assert old_pop_destination == 0
        assert new_pop_destination > 0

    def test_run_function_one_year(self):
        """
        Asserts that run_function_one_year causes the changes which are to be expected with the
        methods that it calls. This test is a bit superfluous, but we wanted to see that it managed
        to implement the expected changes during the course over a year.
        """
        # Places the default_population in a lowland cell
        ini_herbs = [{'loc': (10, 9),
                      'pop': [{'species': 'Herbivore',
                               'age': 5,
                               'weight': 50}
                              for _ in range(150)]}]
        ini_carns = [{'loc': (10, 9),
                      'pop': [{'species': 'Carnivore',
                               'age': 5,
                               'weight': 50}
                              for _ in range(40)]}]
        population = ini_herbs + ini_carns
        i = Island(default_maps, population)
        i.year = 0 # initializes the current year as 0
        old_herb_weight_list = i.weight_list()[0] # list of weights original herbivores
        old_carn_weight_list = i.weight_list()[1] # list of weights original carnivores
        old_herb_fitness_list = i.fitness_list()[0] # list of fitness of original herbivores
        old_carn_fitness_list = i.fitness_list()[1] # list of fitness of original carnivores
        i.run_function_one_year()
        assert i.year == 1 # asserts that the year has been updated by one year
        herb_age_list = i.age_list()[0] # list of age of herbivores after one year
        carn_age_list = i.age_list()[1] # list of age of carnivores after one year
        for herb_age in herb_age_list:
            assert herb_age == 6 or herb_age == 1 # asserts that herbivores have aged by one year,
                                                  # surviving original herbivores with age 6 and
                                                  # surviving new_borns with age 1
        for carn_age in carn_age_list:
            assert carn_age == 6 or carn_age == 1 # asserts that herbivores have aged by one year,
                                                  # surviving original herbivores with age 6 and
                                                  # surviving new_borns with age 1

        assert i.weight_list()[0] != old_herb_weight_list # asserts that list of weights changed
        assert i.weight_list()[1] != old_carn_weight_list # asserts that list of weights changed
        assert i.fitness_list()[0] != old_herb_fitness_list # asserts that list of fitness changed
        assert i.fitness_list()[1] != old_carn_fitness_list # asserts that list of fitness changed
        c1 = i.map[(11, 9)].n_carnivores + i.map[(11, 9)].n_herbivores # population adjacent cell
        c2 = i.map[(9, 9)].n_carnivores + i.map[(9, 9)].n_herbivores # population adjacent cell
        c3 = i.map[(10, 10)].n_carnivores + i.map[(10, 10)].n_herbivores # population adjacent cell
        c4 = i.map[(10, 8)].n_carnivores + i.map[(10, 8)].n_herbivores # population adjacent cell
        assert c1 > 0 or c2 > 0 or c3 > 0 or c4 > 0 # checking if at least one originally empty
                                                    # cells have received migrating animals
        for cell in i.map.values():
            for animal in cell.current_herbivores + cell.current_carnivores:
                assert animal.has_migrated is False # asserts that the animal's has_migrated
                                                    # status is reset to false after each cyclus

