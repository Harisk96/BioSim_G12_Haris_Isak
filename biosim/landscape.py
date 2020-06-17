import numpy as np
from biosim.animals import Herbivore, Carnivore
from operator import attrgetter
np.random.seed(1)

__author__ = "Haris Karovic", "Isak Finnøy"
__email__ = "harkarov@nmbu.no", "isfi@nmbu.no"


class Cell:
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.

    Methods:
    ---------------
    grow_fodder
    place_animals
    birth_cycle
    weight_loss_cell
    feed_all
    feed_herbivores
    feed_carnivores
    age_animals
    death_in_cell
    add_immigrants
    remove_emigrants
    emigratiom
    ---------------

    """
    params = {}

    @classmethod
    def set_params(cls, new_params):
        """
        Updates the parameters
        :param new_params: dict, dictionary with parameters
        :return: None
        """
        if not isinstance(new_params, dict):
            raise TypeError('Input has to be of type dict')

        cls.params.update(new_params)

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
                if newborn_herbivore is not None:

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
        The function iterates through all animals and activates the yearly_weight_loss
        function on each of them.
        :return: None
        """
        for herbivore in self.current_herbivores:
            herbivore.yearly_weight_loss()

        for carnivore in self.current_carnivores:
            carnivore.yearly_weight_loss()

    def feed_all(self):
        """
        Function that calls the grow_fodder and feeding functions for both animals.
        Makes it easier to call upon one function than three seperate ones later on.

        :return: None
        """
        self.grow_fodder()
        self.feed_herbivores()
        self.feed_carnivores()

    def feed_herbivores(self):
        """
        Function that makes the Herbivores eat fodder in the cell.
        All animals are shuffled randomly,
        then we use a for loop to iterate though the list of animals, this will make
        the Herbivores eat in random order. The eating is done by activating the eat function
        from the animals superclass on each Herbivore. Function breaks if there is no fodder left.
        self.fodder is the f_max parameter in Lowland and Highland, otherwise it is set
        as 0 in the constructor.

        :return: None
        """
        np.random.shuffle(self.current_herbivores)
        for herbivore in self.current_herbivores:
            remaining_fodder = self.fodder
            if remaining_fodder <= 0:
                break
            eaten = herbivore.eat(remaining_fodder)
            self.fodder -= eaten

    def feed_carnivores(self):

        """
        This function feeds the carnivores in the cell. As the Herbivores with least fitness is
        preyed upon first the list containing Herbivores are sorted by fitness in increasing order.
        As the Carnivores with the highest fitness are preying upon Herbivores first they are sorted
        by fitness in decreasing order. The sorting is done with the sort function and attrgetter.

        We then iterate though each Carnivore in the list of carnivores. The eat_carn function
        from the animals file is the called upon each Carnivore with the list of Herbivores as
        input. The dead Herbivores are then appended to a dead_herbivores list. After that we use
        a list comprehension to remove all the dead Herbivores from the cell.
        :return:
        """

        self.current_herbivores.sort(key=attrgetter('fitness'))
        self.current_carnivores.sort(key=attrgetter('fitness'), reverse=True)

        for carnivore in self.current_carnivores:
            dead_herbivores = carnivore.eat_carn(self.current_herbivores)
            self.current_herbivores = [herb for herb in self.current_herbivores if
                                       herb not in dead_herbivores]

    def age_animals(self):

        """
        This function iterates through all the animals in the cell, by using two for loops.
        Each for loop iterates for a species, then the update_age function is called
        upon each animal. This will make each every animal in the cell age by one year.

        :return: None
        """

        for herbivore in self.current_herbivores:
            herbivore.update_age()

        for carnivore in self.current_carnivores:
            carnivore.update_age()

    def death_in_cell(self):

        """
        This function iterates through all animals in the cell. Then the death function is called
        upon each animal. The death function determines wheter the animal dies. The dead animals
        get appended into a list. Then a list comprehension will remove the dead animals from
        the list of animals by using the dead animal list.
        :return: None
        """

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
        if not isinstance(list_animals, list):
            raise TypeError('input has to be of type list')

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
        if not isinstance(emigrants, list):
            raise TypeError('Input argument has to be of type dict')
        self.current_herbivores = list(set(self.current_herbivores)-set(emigrants))
        self.current_carnivores = list(set(self.current_carnivores) - set(emigrants))

    def emigration(self, adj_cells):

        if not isinstance(adj_cells, list):
            raise TypeError('input have to be of type list')
        if not len(adj_cells) == 4:
            raise ValueError('input list has to contain 4 elements')
        for i in range(4):
            if not isinstance(adj_cells[i], tuple):
                raise TypeError('Elements of input list has to be of type tuple')
            if len(adj_cells[i]) != 2:
                raise ValueError('Tuple elements have to contain two elements')
            if not isinstance(adj_cells[i][0], int) and (not isinstance(adj_cells[i][1], int)):
                raise TypeError('Tuple elements have to be of type integers')

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
    """
    Landscape type which is a subclass of cell
    migrate_to specifies whether the landscape is liveable and and an animal can migrate to it.
    """

    migrate_to = True
    params = {'f_max': 300.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.params['f_max']

    def grow_fodder(self):
        self.fodder = self.params['f_max']


class Lowland(Cell):
    """
    Landscape type which is a subclass of cell
    migrate_to specifies whether the landscape is liveable and and an animal can migrate to it.
    """

    migrate_to = True
    params = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.params['f_max']

    def grow_fodder(self):
        self.fodder = self.params['f_max']


class Desert(Cell):
    """
    Landscape type which is a subclass of cell
    migrate_to specifies whether the landscape is liveable and and an animal can migrate to it.
    """

    migrate_to = True


class Sea(Cell):
    """
    Landscape type which is a subclass of cell
    migrate_to specifies whether the landscape is liveable and and an animal can migrate to it.
    """

    migrate_to = False
