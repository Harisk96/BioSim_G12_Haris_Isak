from pytest import approx

from biosim.animals import Herbivore, Carnivore, Animals
import pytest
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
        self.default_params = {
            Herbivore:
                {
                    'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
                    'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2,
                    'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None
                },
            Carnivore:
                {
                    'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
                    'phi_age': 0.3, 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
                    'zeta': 3.5, 'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0
                }
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

    # mocks out the random.uniform function with the value 0



def test_birth(mocker):
    """
    Testing the birth function
    """

    mocker.patch("random.uniform", return_value=0)
    h = Herbivore(2, 5.0)
    herb = h.birth(30)
    assert isinstance(herb, Herbivore)
