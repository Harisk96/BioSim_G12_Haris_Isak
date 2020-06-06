from biosim import animals
from biosim.animals import Herbivore, Carnivore, Animals
import pytest
from unittest import mock

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

    @pytest.fixture(autouse=True)
    def teardown(self):
        pass

    h = Herbivore()
    c = Carnivore()

    def test_new_herb(self):
        """
        Tests that a new herbivore has age 0
        """
        h = Herbivore()
        assert h.age == 0

    def test_new_carn(self):
        c = Carnivore()
        assert c.age == 0

    def test_animal_fitness(self):
        """
        Tests that fitness equation returns float
        """
        h = Herbivore()
        assert 0 < h.update_fitness() < 1

