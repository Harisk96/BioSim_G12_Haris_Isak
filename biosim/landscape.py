from biosim.animals import Animals, Herbivore, Carnivore


class Cell:
    params = {}
    """
    Class cell represents a single cell on the island map, the different
    landscape types are subclasses of the Cell superclass.
    """

    def __init__(self):
        self.fodder = 0
        current_animals = {Herbivore: []}

    def grow_fodder(self):


    def place_animals(self):
        """
        Place animals from list (list containing dicts?) into the cell.
        :return:
        """

    def birth_cycle(self):


    def weightloss(self):

    def feed(self):
        #grow fodder
        #feed_carnivores()
        #feed_herbivores

    def feed_herbivore

    #def feed carnivore (Jobber vi med senere)

    def age(self):

    def death_square(self):
        surviving = []
        eller_en_liste_med_dode = ?

    def add_newborn_square(self):???




    def reset_square(self):



    def delete(self):???

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