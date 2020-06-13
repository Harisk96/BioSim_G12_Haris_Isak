

from numba import jit
import numpy as np
np.random.seed(1)

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
    def set_params(cls, new_params):
        """
        Updates the parameters
        :param new_params:
        :return: dict, updated parameters
        """

        # Taken from bacteria.py from the biolab example folder. Modified to the current project
        for key in new_params:
            if key not in cls.params.keys():
                raise KeyError('Invalid parameter name: ' + key)

        if not isinstance(new_params, dict):
            raise TypeError('params must be of type dict')

        cls.params.update(new_params)

    def __init__(self, age=0, weight=None):
        """
        Constructor for animal class.
        """

        if age != int(age):
            raise TypeError("'age' must be of type int ")

        if weight is not None:
            if not isinstance(weight, (int, float)):
                raise TypeError('Weight must be either of type int or type float')
            if weight < 0:
                raise ValueError("'weight' must be greater than or equal to zero")

        if age < 0:
            raise ValueError("'age' must be greater than or equal to zero")

        self.age = age

        if weight is None:
            self.weight = np.random.normal(self.params['w_birth'], self.params['sigma_birth'])
        else:
            self.weight = weight

        self.fitness = self.update_fitness()


    def update_fitness(self):
        """
        Function that updates the fitness of the animal.
        :return: float, value between 0 and 1, returns current fitness of animal
        """
        if self.weight <= 0:
            self.fitness = 0
        else:
            q_positive = self._q(1, self.age, self.params['a_half'], self.params['phi_age'])
            q_negative = self._q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])
            self.fitness = q_positive * q_negative
        return self.fitness


    def eat(self, fodder):
        """
        When an animal eats an amount F of fodder, its weight increases by βF.
        :param fodder: Amount of food available the animal
        :return: float, increase of weight
        """

        if fodder <= 0:
            raise ValueError('Fodder available must be greater than or equal to 0')
        if fodder < self.params['F']:
            food_eaten = fodder
        else:
            food_eaten = self.params['F']

        added_weight = self.params['beta']*food_eaten
        self.weight += added_weight
        self.update_fitness()

        return food_eaten


    def yearly_weight_loss(self):
        """
        Every year, the weight of the animal decreases by ηw.
        :return: float, amount the animals weight decreases by
        """
        subtracted_weight = self.weight * self.params['eta']
        self.weight -= subtracted_weight
        self.update_fitness()


    def update_age(self):
        """
        Updates the age of the animal with one year pr cycle
        :return: int, positive integer greater or equal than zero, age of the animal
        """
        self.age += 1
        self.update_fitness()

    def birth(self, num_animals):
        """
        Decides probability for each animal in each cell whether it will give birth or not.
        Does also provide the conditions that have to be met in order to give birth.
        :return:
        """
        g = self.params['gamma']
        xi = self.params['xi']
        zeta = self.params['zeta']
        if self.weight < zeta * (self.params['w_birth'] + self.params['sigma_birth']):
            return None # Returns ''None'', see comments in landscape
        p_birth = min(1, g * self.fitness * (num_animals-1))

        if np.random.uniform(0, 1) < p_birth:
            birth_weight = np.random.normal(self.params['w_birth'], self.params['sigma_birth'])

            if xi*birth_weight < self.weight:
            # You are missing a check for whether xi*birth_weight > self.weight
                self.weight -= xi * birth_weight
                self.update_fitness()
            if isinstance(self, Herbivore):
                return Herbivore(0, birth_weight) #endret

            elif isinstance(self, Carnivore):
                return Carnivore(0, birth_weight) #endret
                 # This one is never called if the function returns a Herbivore or a Carnivore

    def migrate(self):
        """
        Decides the probability that the animal will move to one of the neighbouring four cells.
        All four cells have equal probability and the animal will not move if the chosen cell
        is water.
        :return: Bool, decides whether the animal moves to a neighboring cell or not
        """
        prob_mig = self.params['mu'] * self.fitness
        random_num = np.random.uniform(0, 1)
        return prob_mig > random_num

    def death(self):
        """
        Function that returns True if the animal is dead, false if it is alive
        :return: Bool, where True represents dead and False alive
        """
        if self.weight <= 0:
            return True
        prob_death = self.params['omega'] * (1 - self.fitness)
        random_num = np.random.uniform(0, 1)
        return prob_death > random_num

class Herbivore(Animals):
    """
    Herbivore subclass. Herbivores can stay in all the landscape types except water,
    i.e desert, highland and lowland, but will only be able to feed in cells with highland or
    lowland as landscape types. It tries to eat an amount F of food each year, but the amount of
    food it can eat depends on the amount of food in the cell. Herbivores eat in a random order.
    """

    params = {
        'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05, 'a_half': 40.0,
        'phi_age': 0.6, 'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
        'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2, 'omega': 0.4, 'F': 10.0
        }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)


class Carnivore(Animals):
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

    params = {
    'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75, 'eta': 0.125, 'a_half': 40.0,
    'phi_age': 0.3, 'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4, 'gamma': 0.8,
    'zeta': 3.5,'xi': 1.1, 'omega': 0.8, 'F': 50.0, 'DeltaPhiMax': 10.0
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)
    """
    def consumption_herb(self, herb_weight):

        self.weight += self.params['beta'] * herb_weight
        self.update_fitness()
    """
    def slay(self, herb):
        if self.fitness <= herb.fitness:
            return False

        elif 0 < self.fitness - herb.fitness < self.params['DeltaPhiMax']:
            prob_kill = (self.fitness - herb.fitness) / self.params['DeltaPhiMax']
            return np.random.uniform(0, 1) < prob_kill

        else:
            return True



#            slay = True # Useless

#        else:
#            slay = False # Useless

#        return slay # Delete all the slay variables. and return Random.uniform(0,1) < prob_kill instead.

    def eat_carn(self, herbivore_list):

        dead_herbs = []
        amount_eaten = 0

        for herbivore in herbivore_list:

            if amount_eaten >= self.params['F']:
                break

            if self.fitness <= herbivore.fitness:
                break

            if self.slay(herbivore):
                if amount_eaten + herbivore.weight > self.params['F']:
                    reduced_amount_eaten = self.params['F'] - amount_eaten
                    self.weight += self.params['beta']*reduced_amount_eaten
                    amount_eaten += reduced_amount_eaten
                else:
                    self.weight += self.params['beta'] * herbivore.weight
                    amount_eaten += herbivore.weight
                #self.consumption_herb(herbivore.weight) # Consumption herb is also an useless function, you are dividing up the code too excessively.
                self.update_fitness()
                dead_herbs.append(herbivore)
        return dead_herbs

"""
if __name__ == "__main__":
    h = Herbivore(age=2, weight=5.0)
    c = Carnivore(age=10, weight=5.0)
    print(h.fitness)
    print(type(h.fitness))
    print(c.fitness)
    print(type(c.fitness))

    h_list = [Herbivore() for _ in range(10)]
    for h in h_list:
        print(h.fitness)

    #more for animals with more weight
    #less for animals with less weight
"""
