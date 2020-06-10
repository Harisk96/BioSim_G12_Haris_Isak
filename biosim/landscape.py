from biosim.animals import Animals, Herbivore, Carnivore

import random
from operator import attrgetter


class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """

    def __init__(self):
        self.fodder = 0
        self.current_herbivores = []
        self.current_carnivores = []

    @property
    def n_herbivores(self):
        """
        Function that returns number of herbivores by taking the length of herbivores list.
        """
        return len(self.current_herbivores)

    @property
    def n_carnivores(self):
        return len(self.current_carnivores)

    @property
    def n_animals(self):
        """
        Function that returns the total number of both species in one cell.
        :return:
        """
        return self.n_herbivores + self.n_carnivores

    def randomise_herbivores(self): # completely useless function
        """
        Shuffles list of herbivores, so feeding can be done at random.
        :return:
        """
        random.shuffle(self.current_herbivores) # Use np.random.shuffle because you have been using np.random in the other files. Assign a np.random.seed(1) at the top.

    def grow_fodder(self):
        """
        Function that can be calle upon to grow fodder at the end of a year.
        This function is overridden in the highland and lowland subclass.
        """
        pass

    def place_animals(self, list_of_animals):
        """
        Place animals from list into the cell.
        :return:
        """
        if not isinstance(list_of_animals, list):
            raise TypeError('list_of_animals has to be of type list')

        for animal in list_of_animals:
            if animal.__class__.__name__ == "Carnivore":
                self.current_carnivores.append(animal)
            else:
                self.current_herbivores.append(animal)

    def birth_cycle(self):
        """
        Function that procreates the animals in a cell by iterating through all animals.
        Appends newborn herbivores in to a list, then extends that list into list containing
        current herbivores in cell
        :return:
        """
        newborn_herbivores = []
        nr_herbivores = self.n_herbivores
        if nr_herbivores > 1:
            for herbivore in self.current_herbivores:
                newborn_herbivore = herbivore.birth(nr_herbivores)
                if not newborn_herbivore:  # Newborn_Herbivore is not a bool value, this creates some problems. You should do it differently, see comments on birth, perhaps return a boolean value?
                    # If you still want to use your method with the ''None'' you should change the if test to if newborn_herbivore is not None, this should work better and you can avoid problems in this manner.
                    continue
                newborn_herbivores.append(newborn_herbivore)

        self.current_herbivores.extend(newborn_herbivores)

        newborn_carnivores = []
        nr_carnivores = self.n_carnivores
        if nr_carnivores > 1:
            for carnivore in self.current_carnivores:
                newborn_carnivore = carnivore.birth(nr_carnivores)
                if not newborn_carnivore:
                    continue
                newborn_carnivores.append(newborn_carnivore)

        self.current_carnivores.extend(newborn_carnivores)
        # Can you think of a better way to implement this function? No need to do it now.

    def weight_loss(self):
        """

        :return:
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
        self.randomise_herbivores()
        for herbivore in self.current_herbivores:
            remaining_fodder = self.fodder
            if remaining_fodder <= 0:
                break
            eaten = herbivore.eat(remaining_fodder)
            self.fodder -= eaten

    def feed_carnivores(self):

        self.current_herbivores = sorted(self.current_herbivores, key=attrgetter('fitness'))
        self.current_carnivores = sorted(self.current_carnivores, key=attrgetter('fitness'),
                                         reverse=True)

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
        for dead_herbivore in dead_herbivores:
            self.current_herbivores.remove(dead_herbivore)

        dead_carnivores = []
        for carnivore in self.current_carnivores:
            if carnivore.death():
                dead_carnivores.append(carnivore)
        for dead_carnivore in dead_carnivores:
            self.current_carnivores.remove(dead_carnivore)


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
    c = Lowland()
    h1 = Herbivore()
    h2 = Herbivore()
    h3 = Herbivore()
    h4 = Herbivore()
    h5 = Herbivore()
    h6 = Herbivore()
    h7 = Herbivore()
    h8 = Herbivore()
    h9 = Herbivore()
    h10 = Herbivore()

    c1 = Carnivore()
    c2 = Carnivore()
    c3 = Carnivore()
    c4 = Carnivore()
    c5 = Carnivore()
    c6 = Carnivore()
    c7 = Carnivore()
    c8 = Carnivore()
    # Placing animals like this is cumbersome.
    # Do this:
    # Bishnu's image:
    # herbivore_list = [Herbivore(5,20) for i in range(50)]
    # carnivore_list = [Carnivore(5,20) for i in range(20)]'
    # plot afterwards
    herbivore_list = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]
    carnivore_list = [c1, c2, c3, c4, c5, c6, c7, c8]

    c.place_animals(herbivore_list)
    c.place_animals(carnivore_list)

    for i in range(10):
        for j in range(200):
            c.feed_all()
            c.birth_cycle()
            c.age_animals()
            c.weight_loss()
            c.death_in_cell()
            #print(c.n_animals)
            print(c.n_carnivores)
