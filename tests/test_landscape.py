from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Cell, Lowland, Highland, Sea
import pytest

__author__ = "Haris Karovic", "Isak Finnøy"
__email__ = "harkarov@nmbu.no", "isfi@nmbu.no"


class TestLandscape:
    """
    Class for testing the methods of landscape-file.
    """
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
        """
        Tests that grow_fodder sets the level of fodder for the fertile cells, i.e lowland and
        highland, to its f_max parameters.
        """
        c = FerCells()
        c.grow_fodder()
        assert c.fodder == c.params['f_max']

    def test_grow_fodder_sea(self):
        """
        Tests if the grow_fodder is None for the Sea subclass.
        """
        w = Sea()
        assert w.grow_fodder() is None

    def test_place_animals(self):
        """
        Tests if the place_animals method places animals in the cell.
        """
        c = Cell()
        h_list = [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20}
                  for _ in range(40)]
        c_list = [{'species': 'Carnivore',
                              'age': 5,
                              'weight': 20}
                  for _ in range(40)]

        with pytest.raises(TypeError, match='list_of_animals has to be of type list'):
            assert c.place_animals("string")
        assert c.place_animals(h_list) == c.current_herbivores.append(h_list)
        assert c.place_animals(c_list) == c.current_carnivores.append(c_list)

    def test_birth_cycle(self, mocker):
        """
        Tests if birth_cycle method results in increase of Herbivores. Mocks out the random
        function, numpy.random.uniform, with return_value 0, which implies birth_cycle always
        returns new herbivore and carnivore objects, which should yield larger number of animals
        in the cell.
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        low = Lowland()
        low.current_herbivores = [Herbivore(5, 100), Herbivore(5, 100)]
        low.current_carnivores = [Carnivore(5, 100), Carnivore(5, 100)]
        low.birth_cycle()

        assert len(low.current_herbivores) >= 3
        assert len(low.current_carnivores) >= 3

    def test_death_in_cell(self):
        """
        Asserts that setting the fitness and weight of animals to 0 results in death. Which is
        accomplished by setting the weight and fitness to zero, and assert that those animals are
        not included in the animals currently residing in that cell.
        """
        c = Cell()
        c.current_herbivores = [Herbivore(5, 0), Herbivore(5, 100), Herbivore(3, 0)]
        c.current_carnivores = [Carnivore(2, 0), Carnivore(5, 100), Carnivore(5, 100)]
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
        """
        Testing if the weight_loss_cell method results in loss of weight. Does this by creating a
        list of herbivores and carnivores, then iterate through them, asserting element wise that
        their weight has decreased.
        """
        c = Cell()
        c.current_herbivores = [Herbivore(2, 10.0) for _ in range(10)]
        c.current_carnivores = [Carnivore(2, 10.0) for _ in range(10)]
        c.weight_loss_cell()
        for i in range(10):
            assert c.current_herbivores[i].weight < 10.0
            assert c.current_carnivores[i].weight < 10.0

    def test_feed_herbivore(self):
        """
        Asserting that feed_herbivore method only increases the weight of the herbivore if there is
        fodder in the cell for the herbivore to eat. Compares how the method impacts the weight of
        the herbivore for no fodder vs fodder.
        """
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
        """
        Checks if the feed_carnivores result in the expected sorting of the herbivores and
        carnivores according to their fitness, and whether the carnivores eat the weakest herbivore.
        """
        c = Cell()
        c.current_carnivores = [Carnivore(4, 8.0), Carnivore(2, 4.0), Carnivore(6, 12.0)]
        c.current_herbivores = [Herbivore(6, 30.0), Herbivore(2, 0.1), Herbivore(4, 40.0)]
        c.feed_carnivores()
        assert c.current_carnivores[0].fitness > c.current_carnivores[1].fitness
        assert c.current_carnivores[1].fitness > c.current_carnivores[2].fitness
        assert c.current_herbivores[0].fitness < c.current_herbivores[1].fitness
        assert len(c.current_herbivores) < 3

    @pytest.mark.parametrize('FerCells', [Lowland, Highland])
    def test_feed_all(self, FerCells):
        """
        Asserts that the feed_all method resets the amount of fodder to the max parameters.
        """
        fc = FerCells()
        fc.feed_all()
        assert fc.fodder == fc.params['f_max']

    def test_age_animals(self):
        """
        Tests that the age_animals method ages the animals by one year. Creates a list of animals,
        then assert element wise that they have indeed increased by one year.
        """
        low = Lowland()
        low.current_carnivores = [Carnivore(1, 1), Carnivore(3, 3)]
        low.current_herbivores = [Herbivore(9, 9), Herbivore(2, 2)]
        low.age_animals()
        assert low.current_carnivores[0].age == 2
        assert low.current_carnivores[1].age == 4
        assert low.current_herbivores[0].age == 10
        assert low.current_herbivores[1].age == 3

    def test_add_immigrants(self):
        """
        Tests that the add_immigrants method adds new animals to the current animals in the cell.
        Starts by defining current_herbivores and current_carnivores, then checking if they increase
        by the number of immigrants we add.
        """
        cell = Cell()
        cell.current_carnivores = [Carnivore() for _ in range(10)]
        cell.current_herbivores = [Herbivore() for _ in range(10)]
        immigrants = [Herbivore(), Carnivore()]
        cell.add_immigrants(immigrants)
        assert cell.n_carnivores == 11 and cell.n_herbivores == 11
        with pytest.raises(TypeError):
            assert cell.add_immigrants((3, 2))

    def test_remove_emigrants(self):
        """
        Tests that remove_emigrants removes emigrating animals from the current animals in the cell-
        Starts by defining current_herbivores and current_carnivores, then checking if they decrease
        by the number of emigrant we remove.
        """
        cell = Cell()
        cell.current_carnivores = [Carnivore() for _ in range(10)]
        cell.current_herbivores = [Herbivore() for _ in range(10)]
        emigrants = [cell.current_herbivores[0], cell.current_carnivores[0]]
        cell.remove_emigrants(emigrants)
        assert cell.n_carnivores == 9 and cell.n_herbivores == 9
        with pytest.raises(TypeError):
            assert cell.remove_emigrants((2, 3))

    def test_emigration(self, mocker):
        """
        Testing that emigration method moves animals from one cell to another if the probability
        test numpy.random.uniform is lower than the probability of moving, which should imply that
        the emigration method should return True.
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        cell = Cell()
        adj_cells = [(10, 10), (10, 10), (10, 10), (10, 10)]
        carn = Carnivore()
        carn.has_migrated = False
        cell.current_carnivores.append(carn)
        herb = Herbivore()
        herb.has_migrated = False
        cell.current_herbivores.append(herb)
        emigrants = cell.emigration(adj_cells)
        assert isinstance(emigrants, dict)
        assert emigrants[(10, 10)] == cell.current_carnivores + cell.current_herbivores

    def test_emigration_exceptions(self):
        """
        Asserting that emigration method throws exceptions according to the scenarios which are
        expected to cause them.
        """
        cell = Cell()
        with pytest.raises(TypeError):
            assert cell.emigration({'1337': 1337})
        with pytest.raises(ValueError):
            assert cell.emigration([(1, 1)])
        with pytest.raises(TypeError):
            assert cell.emigration([[1], [2], [3], [4]])
        with pytest.raises(ValueError):
            assert cell.emigration([(1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 1, 1)])
        with pytest.raises(TypeError):
            assert cell.emigration([(0.5, 0.5), (0.5, 0.5), (0.5, 0.5), (0.5, 0.5)])

    def test_set_params(self):
        """
        Testing the set_params method in landscape file, that it sets the parameters according to
        our specifications.
        """
        cell = Cell()
        low = Lowland()
        new_params = {'f_max': 100}
        old_params = {'f_max': 800}  # parameter for fodder for lowland object
        assert low.params == old_params
        low.set_params(new_params)
        assert low.params == new_params
        with pytest.raises(TypeError):
            assert cell.set_params([1, 2])
