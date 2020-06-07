from biosim.animals import Animals, Herbivore, Carnivore

import random

class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """

    def __init__(self):
        self.fodder = 0
        self.current_herbivores = []
        # current_carnivores = []

    @property
    def n_herbivores(self):
        return len(self.current_herbivores)

# Funksjonen under bruker vi når carnivores kommer.
    #    @property
    #    def n_carnivores:
    #        return self.len(current_carnivores)

    @property
    def n_animals(self):
        return self.n_herbivores  # +self.len(current_carnivores)

    def randomise_herbivores(self):
        # Her må randomisere herbivores listen for å kunne feede listen bortover.
        random.shuffle(self.current_herbivores)

    def grow_fodder(self):
        self.fodder += 0

    def place_animals(self):
        """
        Place animals from list (list containing dicts?) into the cell.
        :return:
        """

    def birth_cycle(self):

        newborn_herbivores = []
        nr_herbivores = self.n_herbivores
        if nr_herbivores > 1:
            for herbivore in self.current_herbivores:
                newborn_herbivore = herbivore.animals.birth_check(nr_herbivores)
                if not newborn_herbivore:
                    continue
                self.current_herbivores.append(newborn_herbivore)
                newborn_herbivores.append(newborn_herbivore)

                return self.current_herbivores, newborn_herbivores

    def weightloss(self):
        for herbivore in self.current_herbivores:
            herbivore.animals.yearly_weight_loss()

    def feed(self):
        self.grow_fodder()
        #self.feed_carnivores()
        self.feed_herbivores

    def feed_herbivores(self):
        self.randomise_herbivores()
        .eat

    # def feed carnivore (Jobber vi med senere)

    def age_animals(self):
        for herbivore in self.current_herbivores:
            herbivore.animals.update_age()

    def death_square(self):
        surviving = []
        eller_en_liste_med_dode = ?

        def add_newborn_square(self): ?

            ??

        def reset_square(self):

        def delete(self): ?

            ??

class Highland(Cell):
    migrate_to: True
    params = {'f_max': 300.0}

    def __init__(self):
        super().__init__()
        self.fodder = self.params['f_max']

    def _yearly_fodder(self):
        self.fodder = self.params['fmax']

class Lowland(Cell):
            migrate_to: True
            params = {'f_max': 800.0}

    def __init__(self):
        super().__init__()
            self.fodder = self.params['f_max']

    def _yearly_fodder(self):
                self.fodder = self.params['fmax']

class Desert(Cell):
        migrate_to = True

class Sea(Cell):
        migrate_to = False