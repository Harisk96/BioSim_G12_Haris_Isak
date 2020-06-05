from biosim.animals import Animals, Herbivore, Carnivore


class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """

    def __init__(self):
        self.fodder = 0
        current_animals = {Herbivore: [], Carnivore: []}
        newborn_animals = {Herbivore: [], Carnivore: []}

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