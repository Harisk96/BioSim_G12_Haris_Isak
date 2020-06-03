
from numba import jit
import numpy as np

__author__ = "Haris Karovic", "Isak Finnøy"
__email__ = "harkarov@nmbu.no", "isfi@nmbu.no"

class Animals:
    """
    Superclass that represents an animal. Contains all the features for for creating the animals.
    herbivores and carnivores are subclasses of this superclass.
    """
    parameters = {}

    @staticmethod
    @jit
    def _q(sign, x, x_half, phi):
        """
        Function used to compute fitness
        :param sign: int, takes the value +1 for age and -1 for weight
        :param x: int, float, age multiplied with weight
        :param x_half: int, float, age halved multiplied with weight halved
        :param phi: int, float, phi_age multiplied with phi_weight
        :return: float
        """
        return 1.0/(1 + np.exp(sign*phi*(x - x_half)))

    @classmethod
    def _calculate_fitness(cls):




    def __init__(self, age=0, w_birth):
        """
        Constructor for animal class.
        """
        self.age = age
        self.w_birth = w_birth

    def set_params(self):
        """
        Setting the parameters given in the project PDF for the animal superclass.
        :return:
        """

        w_birth =

    @classmethod
    @jit
    def initial_weight(cls, params):
        """
         the birth weight is drawn from a Gaussian distribution with w_mean_birth and sigma_birth.
         We use numpy.random to draw a random value from the distribution we create with .normal.
         The mean and the standard deviation of the weight are pulled from the parameters dictionary
          of the subclass.

        :return: float; initial weight
        """

        return np.random.normal(params['w_birth'], params['sigma_birth'])


    def weight_update(self):
        """
        When an animal eats an amount F of fodder, its weight increases by βF. Every year,
        the weight of the animal decreases by ηw.
        :return:
        """

    def birth(self):
        """
        Decides probability for each animal in each cell whether it will give birth or not.
        Does also provide the conditions that have to be met in order to give birth.
        :return:
        """

    def fitness(self):
        """
        The overall condition of the animal is described by its ﬁtness,
        which is calculated based on age and weight using a formula.
        :return: Float, value between 0 and 1 representing fitness.
        """
    def update_fitness(self):
        """
        Updates the fitness of the animal, which is re-calculated as a consequence of changes in
        the attributes of the animal.
        :return: Float, value between 0 and 1 representing the new value of the fitness
        """
    def migrate(self):
        """
        Decides the probability that the animal will move to one of the neighbouring four cells.
        All four cells have equal probability and the animal will not move if the chosen cell
        is water.
        :return:
        """


class Herbivore(Animal):
    """
    Herbivore subclass. Herbivores can stay in all the landscape types except water,
    i.e desert, highland and lowland, but will only be able to feed in cells with highland or
    lowland as landscape types. It tries to eat an amount F of food each year, but the amount of
    food it can eat depends on the amount of food in the cell. Herbivores eat in a random order.
    """

    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
    'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5,
    'xi': 1.2, 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def feed(self):

class Carnivore(Animal):
    """
    Carnivore subclass. Carnivores can stay in all landscape types except water, i.e desert,
    highland and lowland, and will be able to prey on herbivores in all the aforementioned
    landscape types, though not on other carnivores. The carnivores prey on herbivores until one of
    the following conditions are met:
                                     1. It has eaten an amount of herbivores >= F
                                     2. It has tries to kill every herbivore in the cell
    The carnivores prey in order of their fitness, so that the fittest carnivore eats first. They
    try to kill one herbivore at a time, trying to kill the herbivore with the lowest fitness first.
    """

    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125, 'a_half': 4.0,
    'phi_age': 0.3, 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5,
    'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}


    def slay(self):
        """
        Function that determines wether and when a carnivore will kill a herbivore and consume it.
        :return:
        """