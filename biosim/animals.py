

from numba import jit
import numpy as np
import random

__author__ = "Haris Karovic", "Isak Finnøy"
__email__ = "harkarov@nmbu.no", "isfi@nmbu.no"

class Animals:
    """
    Superclass that represents an animal. Contains all the features for for creating the animals.
    herbivores and carnivores are subclasses of this superclass.
    """
    params = {}

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
        return 1.0 / (1 + np.exp(sign * phi * (x - x_half)))

    @classmethod
    def _fitness_equation(cls, age, weight, params):
        """
        Function that calculates the current fitness of the animal.
        :param age: int, age of the animal
        :param weight: float, weight of the animal
        :param params: dict, dictionary containing the parameters

        :return: float, value between 0 and 1, returns current fitness of animal
        """

        q_positive = cls._q(1, age, params['a_half'], params['phi_age'])
        q_negative = cls._q(-1, weight, params['w_half'], params['phi_weight'])

        q = q_positive * q_negative

        return q

    @classmethod
    def set_params(cls, params):
        """
        Updates the parameters
        :param params:
        :return:
        """

        if not isinstance(params, dict):
            raise TypeError('params must be of type dict')

        cls.params.update(params)

    def __init__(self, age=0, weight=None):
        """
        Constructor for animal class.
        """
        if not isinstance(age, int):
            raise TypeError("'age' must be of type int ")

        if age > 0 and (not isinstance(weight, (int, float))):
            raise TypeError('Weight must be of either type int or type float after first iteration')

        if age < 0:
            raise ValueError("'age' must be greater than or equal to zero")

        if weight < 0:
            raise ValueError("'weight' must be greater than or equal to zero")

        self.age = age
        if weight is None:
            self.weight = np.random.normal(self.params['w_birth'], self.params['sigma_birth'])

        self.fitness = None
        if self.fitness is None:
            self.update_fitness()


    def update_fitness(self):
        self.fitness = self._fitness_equation(self.age, self.weight, self.params)

    def set_params(self):
        """
        Setting the parameters given in the project PDF for the animal superclass.
        :return:
        """
        pass


    def eat(self, F):
        """
        When an animal eats an amount F of fodder, its weight increases by βF.
        :param F: Amount of food eaten by the animal
        :return: float, increase of weight
        """
        added_weight = self.params['beta']*F
        self.weight += added_weight
        self.update_fitness()



    def yearly_weight_loss(self):
        """
        Every year, the weight of the animal decreases by ηw.
        :return: float, amount the animals weight decreases by
        """
        subtracted_weight = self.weight*self.params['eta']
        self.weight -= subtracted_weight
        self.update_fitness()


    def update_age(self):
        """
        Updates the age of the animal with one year pr cycle
        :return: int, positive integer greater or equal than zero, age of the animal
        """
        self.age += 1
        self.update_fitness()

    def birth(self, N):
        """
        Decides probability for each animal in each cell whether it will give birth or not.
        Does also provide the conditions that have to be met in order to give birth.
        :return:
        """
        g = self.params['gamma']
        zeta = self.params['zeta']
        xi = self.params['xi']
        p_birth = np.min(1, g * self.fitness * (N - 1))

        #Each animal can only give birth to one offspring
        #If weight of baby is higher than mothers weight, no offpsring is born, mother weight is same.
        while not offspring: # while offspring = False

            if self.weight < zeta(params['w_birth'] + params['sigma_weight']):
                return
            #sannsynligheten for at offspring skjer
            else:
                p_birth = p_birth

            if random.uniform(0, 1) <= p_birth:
                birth_weight = np.random.normal(self.params['w_birth'], self.params['sigma_birth'])
                self.weight -= xi*birth_weight


                if isinstance(self, Herbivore):
                    self.update_fitness()
                    return Herbivore(0, birth_weight)


                elif isinstance(self, Carnivore):
                    self.update_fitness()
                    return Carnivore(0, birth_weight)

                offspring = True
                return offspring


 #   def update_fitness(self): (Completing and testing, is it between zero and 1, does it increase with weight)
        """
        The overall condition of the animal is described by its ﬁtness,
        which is calculated based on age and weight using a formula.
        :return: Float, value between 0 and 1 representing fitness.
        """
        self._fitness_fitness(self, weight)

    def migrate(self):
        """
        Decides the probability that the animal will move to one of the neighbouring four cells.
        All four cells have equal probability and the animal will not move if the chosen cell
        is water.
        :return:
        """
        pass
    # def prob_move():
    # def prob_die():

class Herbivore(Animal):
    """
    Herbivore subclass. Herbivores can stay in all the landscape types except water,
    i.e desert, highland and lowland, but will only be able to feed in cells with highland or
    lowland as landscape types. It tries to eat an amount F of food each year, but the amount of
    food it can eat depends on the amount of food in the cell. Herbivores eat in a random order.
    """

    params = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
    'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5,
    'xi': 1.2, 'omega': 0.4, 'F': 10.0, 'DeltaPhiMax': None}

    def __init__(self, age, weight):
        super().__init__(age, weight)

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

    params = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
    'phi_age': 0.3, 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8, 'zeta': 3.5,
    'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0}

    def __init__(self, age, weight):
        super().__init__(age, weight)

    def slay(self):
        """
        Function that determines wether and when a carnivore will kill a herbivore and consume it.
        :return:
        """

if __name__ == "__main__":
    h = Herbivore(age=2, weight=100)
    print(h.fitness)
    h.update_wih

    #more for animals with more weight
    #less for animals with less weight