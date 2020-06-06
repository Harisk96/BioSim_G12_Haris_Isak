from biosim.animals import Animals, Herbivore, Carnivore


class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """

    def __init__(self):
        self.fodder = 0
        current_herbivores = []
        # current_carnivores = []

    @property
    def n_herbivores:
        return self.len(current_herbivores)

    #    @property
    #    def n_carnivores:
    #        return self.len(current_carnivores)

    @property
    def n_animals
        return self_n_herbivores  # +self.len(current_carnivores)

    def randomise_herbivores(self):
        # Her må randomisere herbivores listen for å kunne feede listen bortover.
        random.shuffle(current_herbivores)

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
            for herbivore in self.herbivores:
                newborn_herbivore = herbivore.animals.birth_check(nr_herbivores)
                if not newborn:
                    continue
                self.herbivores.append(newborn)
                newborn_herbivores.append(newborn)

                return self.herbivors, newborn_herbivores

    def weightloss(self):
        for herbivore in self.herbivores:
            herbivore.animals.yearly_weightloss()

    def feed(self):
        self.grow_fodder()
        self.feed_carnivores()
        self.feed_herbivores

    def feed_herbivore(self):
        biosim.animals.eat

    # def feed carnivore (Jobber vi med senere)

    def age_animals(self):
        for herbivore in self.herbivores:
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

    lass Desert(Cell):\
        migrate_to = True

    class Sea(Cell):
        migrate_to = False