from pytest import approx

from biosim.animals import Herbivore, Carnivore, Animals
import pytest
import numba
from unittest import mock
import random

__author__ = 'Haris Karovic', 'Isak Finnøy'
__email__ = 'harkarov@nmbu.no', 'isfi@nmbu.no'


class TestAnimals:
    """
    Test animals module
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        Sets the testing environment up
        """
        self.herb_params = {
            'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
            'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
            'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None
        }
        self.carn_params = {
            'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
            'phi_age': 0.3, 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
            'zeta': 3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0
        }

    animals = {Herbivore: Herbivore(), Carnivore: Carnivore()}

    @pytest.fixture(autouse=True)
    def teardown(self):
        pass

    h = Herbivore()
    c = Carnivore()

    def test_new_animal(self):
        """
        Tests that a new herbivore has age 0
        """
        h = Herbivore()
        c = Carnivore()
        assert h.age == 0 and c.age == 0

    def test_animal_age(self):
        """
        Tests that fitness equation returns float
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(4, 7.0)
        h.update_age()
        c.update_age()
        assert h.age == 3 and c.age == 5  # 2 + 1

    def test_subclass(self):
        """
        Tests that Herbivore and Carnivore is a subclass of Animals
        """
        h = Herbivore()
        c = Carnivore()
        assert issubclass(h.__class__, Animals)
        assert issubclass(c.__class__, Animals)

    def test_instance_super(self):
        """
        Tests that Herbivore-object and Carnivore-object is an instance of Animals
        """
        h = Herbivore()
        c = Carnivore()
        assert isinstance(h, Animals)
        assert isinstance(c, Animals)

    def test_initial_weight(self):
        """
        Testing if the birth weight is positive
        """
        h = Herbivore()
        c = Carnivore()
        assert h.weight and c.weight >= 0

    def test_yearly_weight_loss(self):
        """
        Testing if yearly_weight_loss results in lower weight
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(2, 7.0)
        h.yearly_weight_loss()
        c.yearly_weight_loss()
        assert h.weight < 5.0 and c.weight < 7.0

    def test_eat_limits(self):
        """
        Testing if available food lower than appetite leads to expected weight increase
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        h.eat(5.0)
        c.eat(7.0)
        exp_inc_h = h.params['beta'] * 5.0
        exp_inc_c = c.params['beta'] * 7.0
        assert h.weight == (5.0 + exp_inc_h) and c.weight == (7.0 + exp_inc_c)

    def test_eat_appetite(self):
        """
        Testing if available food higher than appetite results in weight increase limited by the
        appetite
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        h.eat(15)
        c.eat(75)
        exp_inc_h = h.params['beta'] * 10.0
        exp_inc_c = c.params['beta'] * 50.0
        assert h.weight == (5.0 + exp_inc_h) and c.weight == (7.0 + exp_inc_c)

    def test_update_fitness_new_param(self):
        """
        Testing if update_fitness updates fitness with different parameters
        """
        h = Herbivore(2, 5.0)
        f1 = h.fitness
        h.age = 5
        h.weight = 10.0
        h.update_fitness()
        f2 = h.fitness
        assert f1 != f2

    def test_update_fitness_same_param(self):
        """
        Testing that the update_fitness function doesnt change fitness for same parameters
        """
        h = Herbivore(2, 5.0)
        f1 = h.fitness
        h.update_fitness()
        f2 = h.fitness
        assert f1 == f2

    def test_fitness(self):
        """
        Testing that the fitness attribute is a float.
        """
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        assert isinstance(h.fitness, float)
        assert isinstance(c.fitness, float)

    def test_fitness_weight(self):
        """
        Testing that fitness equals zero if weight is zero.
        """
        h = Herbivore(2, 0.0)
        c = Carnivore(3, 0.0)
        c.update_fitness()
        h.update_fitness()
        assert h.fitness == 0
        assert c.fitness == 0

    def test_eat_valerr(self):
        """
        Asserts that input of negative fodder raises a ValueError.
        """
        h = Herbivore(2, 5.0)
        with pytest.raises(ValueError):
            assert h.eat(-1)

    def test_eat_fodder(self):
        """
        Asserts that animal
        """
        h = Herbivore(2, 5.0)
        fodder = h.params['F'] - 5
        assert h.eat(fodder) == fodder

    def test_eat_food_eaten(self):
        h = Herbivore(2, 5.0)
        float_ = 5.0
        fodder = h.eat(float_)
        assert isinstance(fodder, float)

    def test_set_params(self):
        h = Herbivore()
        old_params = h.params
        new_herb_params = {'w_birth': 8.0, 'sigma_birth': 1.7, 'beta': 1.2}
        h.set_params(new_herb_params)
        assert h.params['w_birth'] == pytest.approx(8.0)
        assert h.params != old_params


    def test_constructor(self):
        h = Herbivore()
        c = Carnivore()
        assert isinstance(c, Carnivore)
        assert isinstance(h, Herbivore)

    def test_birth(self, mocker):
        """
        Testing the birth function. Mocks out the random function with 0, guaranteeing that the
        probability for death exceeds the random function, which should yield the boolean True.
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        h = Herbivore(2, 50.0)
        c = Carnivore(3, 50.0)
        herb = h.birth(30)
        carni = c.birth(50)
        assert isinstance(herb, Herbivore)
        assert isinstance(carni, Carnivore)

    def test_death(self, mocker):
        """
        Testing the death function. Mocks out the random function with 0, guaranteeing that the
        probability for death exceeds the random function, which should yield the boolean True.
        """
        mocker.patch("numpy.random.uniform", return_value=0)
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        dead_herb = h.death()
        dead_carn = c.death()
        assert dead_herb is True
        assert dead_carn is True

    def test_migrate(self, mocker):
        """
        Testing the migration function. Mocks out the random function with 0, guaranteeing that the
        probability for migration exceeds the random function, which will then yield the boolean True.
        """
        mocker.patch('numpy.random.uniform', return_value=0)
        h = Herbivore(2, 5.0)
        c = Carnivore(3, 7.0)
        move_herb = h.migrate()
        move_carn = c.migrate()
        assert move_herb is True
        assert move_carn is True
