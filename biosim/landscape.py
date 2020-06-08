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
        """
        Shuffles list of herbivores, so feeding can be done at random.
        :return:
        """
        random.shuffle(self.current_herbivores)

    def grow_fodder(self):

        pass

    def place_animals(self, list_of_animals):
        """
        Place animals from list (list containing dicts?) into the cell.
        :return:
        """
        if not isinstance(list_of_animals, list):
            raise TypeError('lololol')

        for animal in list_of_animals:
            self.current_herbivores.append(animal)

    def birth_cycle(self):

        newborn_herbivores = []
        nr_herbivores = self.n_herbivores
        if nr_herbivores > 1:
            for herbivore in self.current_herbivores:
                newborn_herbivore = herbivore.birth(nr_herbivores)
                if not newborn_herbivore:
                    continue
                #self.current_herbivores.append(newborn_herbivore)
                newborn_herbivores.append(newborn_herbivore)

        self.current_herbivores.extend(newborn_herbivores)


        #return self.current_herbivores, newborn_herbivores
            #Må huske på at vi får newborns inn i selve current herbivores

    def weight_loss(self):
        for herbivore in self.current_herbivores:
            herbivore.animals.yearly_weight_loss()

    def feed(self):
        self.grow_fodder()
        #self.feed_carnivores()
        self.feed_herbivores()
        #Herbivores spiser først

    def feed_herbivores(self):
        self.randomise_herbivores()
        for herbivore in self.current_herbivores:
            remaining_fodder = self.fodder
            if remaining_fodder <= 0:
                break
            eaten = herbivore.eat(remaining_fodder)
            self.fodder -= eaten


    # def feed carnivore (Jobber vi med senere)

    def age_animals(self):
        for herbivore in self.current_herbivores:
            herbivore.animals.update_age()

    def death_square(self):
    #Ta en titt på forelesning 08.06.2020, for remove er veldig ueffektivt.
        dead_herbivores = []
        for herbivore in self.current_herbivores:
            if herbivore.death():
                dead_herbivores.append(herbivore)
        for dead_herbivore in dead_herbivores:
            self.current_herbivores.remove(dead_herbivore)
        return dead_herbivores


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

    herbivore_list = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10]

    c.place_animals(herbivore_list)

    for i in range(10):
        for i in range(200):
            c.feed()
            c.birth_cycle()
            c.age_animals()
            c.weight_loss()
            c.animals.death()
        print(c.n_animals)