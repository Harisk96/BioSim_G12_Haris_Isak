import numpy as np
import random
np.random.seed(1)
from biosim.animals import Animals, Herbivore, Carnivore
from operator import attrgetter
import matplotlib.pyplot as plt
import random


class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """


    def __init__(self):
        """
        constructor for the cell super class.
        """
        self.fodder = 0
        self.current_herbivores = []
        self.current_carnivores = []


    @property
    def n_herbivores(self):
        """
        Function that returns number of herbivores in one cell by calculating the length
        of herbivores list.
        :return: int >= 0, number of herbivores in one cell.
        """
        return len(self.current_herbivores)

    @property
    def n_carnivores(self):
        """
        Function that returns number of carnivores in one cell by calculating the length
        of carnivores list.
        :return: int >= 0, number of carnivores in one cell.
        """
        return len(self.current_carnivores)

    @property
    def n_animals(self):
        """
        Function that returns a tuple with number of herbivores and number of carnivores in one
        cell.
        :return: tuple of positive integers, which represents number of each type in one cell.
        """
        return self.n_herbivores, self.n_carnivores

    def grow_fodder(self):
        """
        Function that can be called upon to grow fodder at the end of a year.
        This function is overridden in the highland and lowland subclass.
        """
        pass

    def place_animals(self, list_of_animals):
        """
        Place animals from list into the cell.
        :return: None
        """

        for animal in list_of_animals:

            if not isinstance(list_of_animals, list):
                raise TypeError('list_of_animals has to be of type list')

            age = animal['age']
            weight = animal['weight']
            species = animal['species']

            if species == 'Herbivore':
                self.current_herbivores.append(Herbivore(age, weight))
            if species == 'Carnivore':
                self.current_carnivores.append(Carnivore(age, weight))

    def birth_cycle(self):
        """
        Function that procreates the animals in a cell by iterating through all animals.
        Appends newborn herbivores in to a list, then extends that list into list containing
        current herbivores in cell
        :return: None
        """
        newborn_herbivores = []
        nr_herbivores = self.n_herbivores
        if nr_herbivores > 1:
            for herbivore in self.current_herbivores:
                newborn_herbivore = herbivore.birth(nr_herbivores)
                if newborn_herbivore is not None:  # Newborn_Herbivore is not a bool value, this creates some problems. You should do it differently, see comments on birth, perhaps return a boolean value?
                    # If you still want to use your method with the ''None'' you should change the if test to if newborn_herbivore is not None, this should work better and you can avoid problems in this manner.
                    newborn_herbivores.append(newborn_herbivore)

        self.current_herbivores.extend(newborn_herbivores)

        newborn_carnivores = []
        nr_carnivores = self.n_carnivores
        if nr_carnivores > 1:
            for carnivore in self.current_carnivores:
                newborn_carnivore = carnivore.birth(nr_carnivores)
                if newborn_carnivore is not None:
                    newborn_carnivores.append(newborn_carnivore)

        self.current_carnivores.extend(newborn_carnivores)
        # Can you think of a better way to implement this function? No need to do it now.

    def weight_loss_cell(self):
        """
        Makes it so that the animals in the cell loses weight on an annual basis.
        :return: None
        """
        for herbivore in self.current_herbivores:
            herbivore.yearly_weight_loss()

        for carnivore in self.current_carnivores:
            carnivore.yearly_weight_loss()

    def feed_all(self):
        self.grow_fodder()
        self.feed_herbivores()
        self.feed_carnivores()

    def feed_herbivores(self):
        np.random.shuffle(self.current_herbivores)
        for herbivore in self.current_herbivores:
            remaining_fodder = self.fodder
            if remaining_fodder <= 0:
                break
            eaten = herbivore.eat(remaining_fodder)
            self.fodder -= eaten

    def feed_carnivores(self):

        self.current_herbivores.sort(key=attrgetter('fitness')) #= sorted(self.current_herbivores, key=attrgetter('fitness'))
        self.current_carnivores.sort(key=attrgetter('fitness'), reverse=True)  #= sorted(self.current_carnivores, key=attrgetter('fitness'),
                                         #reverse=True)

        for carnivore in self.current_carnivores:
            dead_herbivores = carnivore.eat_carn(self.current_herbivores)
            self.current_herbivores = [herb for herb in self.current_herbivores if
                                       herb not in dead_herbivores]

    def age_animals(self):
        for herbivore in self.current_herbivores:
            herbivore.update_age()

        for carnivore in self.current_carnivores:
            carnivore.update_age()

    def death_in_cell(self):
        # Ta en titt på forelesning 08.06.2020, for remove er veldig ueffektivt.
        dead_herbivores = []
        for herbivore in self.current_herbivores:
            if herbivore.death():
                dead_herbivores.append(herbivore)
        self.current_herbivores = [herb for herb in self.current_herbivores if
                                   herb not in dead_herbivores]

        dead_carnivores = []
        for carnivore in self.current_carnivores:
            if carnivore.death():
                dead_carnivores.append(carnivore)
        self.current_carnivores = [carn for carn in self.current_carnivores if
                                   carn not in dead_carnivores]

    def add_immigrants(self, list_animals):
        herbs = [anim for anim in list_animals if anim.__class__.__name__ == 'Herbivore']
        carns = [anim for anim in list_animals if anim.__class__.__name__ == 'Carnivore']
        self.current_herbivores.extend(herbs)
        self.current_carnivores.extend(carns)

    def remove_emigrants(self, emigrants):
        """
        Removes emigrants from cell (removes them from self.current_herbivores and
        self.current_carnivores.
        :return:
        """
        self.current_herbivores = list(set(self.current_herbivores)-set(emigrants))
        self.current_carnivores = list(set(self.current_carnivores) - set(emigrants))

    def emigration(self, adj_cells):


        emigrants = {}

        animal_list = self.current_carnivores + self.current_herbivores

        list_of_emigrants = [emi for emi in animal_list if emi.migrate()
                             and emi.has_migrated is False]
        for emi in list_of_emigrants:
            destination = adj_cells[np.random.randint(0, 4)]
            if destination in emigrants.keys():
                emigrants[destination].append(emi)
            else:
                emigrants[destination] = [emi]

        for animal in animal_list:
            animal.set_has_migrated(True)

        return emigrants



class Highland(Cell):
    migrate_to = True
    params = {'f_max': 300.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.params['f_max']

    def grow_fodder(self):
        self.fodder = self.params['f_max']


class Lowland(Cell):
    migrate_to = True
    params = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.params['f_max']

    def grow_fodder(self):
        self.fodder = self.params['f_max']


class Desert(Cell):
    migrate_to = True


class Sea(Cell):
    migrate_to = False

if __name__ == "__main__":
    cell = Cell()
    adj_cells = [(9, 10), (11, 10), (10, 9), (10, 11)]
    carn = Carnivore()
    carn.has_migrated = False
    cell.current_carnivores.append(carn)
    herb = Herbivore()
    herb.has_migrated = False
    cell.current_herbivores.append(herb)
    print(cell.emigration(adj_cells))

    """
    c.current_herbivores = [Herbivore() for _ in range(10)]
    h_list = [Herbivore() for _ in range(5)]
    print(len(c.current_herbivores))
    print((h_list))
    for i in range(len(c.current_herbivores)):
        print(c.current_herbivores[i].weight)
    print(len(c.current_herbivores))
    """