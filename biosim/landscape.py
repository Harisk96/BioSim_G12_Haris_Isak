import numpy as np
np.random.seed(1)

from biosim.animals import Animals, Herbivore, Carnivore

from operator import attrgetter
import matplotlib.pyplot as plt


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

    def randomise_herbivores(self): # completely useless function
        """
        Shuffles list of herbivores in random order, so feeding can be done at random.
        :return: None
        """
        np.random.shuffle(self.current_herbivores) #endret # Use np.random.shuffle because you have been using np.random in the other files. Assign a np.random.seed(1) at the top.
                                                    # slett funksjon,
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
    """
    l = Lowland()

    l.herb_list = [Herbivore(5, 20) for i in range(50)]
    l.carn_list = [Carnivore(5, 20) for i in range(20)]


    l.place_animals(l.herb_list)
    l.place_animals(l.carn_list)

#    fig = plt.figure(figsize=(8, 6.4))
#    plt.plot(0, len(l.herb_list), '*-', color='g', lw=0.5)
#    plt.plot(0, len(l.carn_list), '*-', color='r', lw=0.5)
#    plt.draw()
#    plt.pause(0.001)

    count_herb = [len(l.herb_list)]
    count_carn = [len(l.carn_list)]

   # fig = plt.figure()
   # ax = fig.add_subplot(1, 1, 1)

   #ax.set_xlim(0, 180)
    #ax.set_ylim(0, 200)

  #  line_herb = ax.plot(np.arange(200),
   #                np.full(200, np.nan), 'b-')[0]

    #line_carn = ax.plot(np.arange(200),
     #                   np.full(200, np.nan), 'r-')[0]
    for i in range(200):
        count_herb.append(l.n_herbivores)
        count_carn.append(l.n_carnivores)
        l.grow_fodder()
        l.feed_all()
        l.birth_cycle()
        l.age_animals()
        l.weight_loss()
        l.death_in_cell()

        #ydata = line_herb.get_ydata()
        #ydata[i] = l.n_herbivores
        #line_herb.set_ydata(ydata)

      #  ydata2 = line_carn.get_ydata()
       # ydata2[i] = l.n_carnivores
        #line_carn.set_ydata(ydata2)

        #plt.pause(1e-6)
    plt.plot(count_herb, 'b-')
    plt.plot(count_carn, 'r-')
    plt.show()



#        count_herb.append(len(l.herb_list))
#        count_carn.append(len(l.carn_list))

#        plt.plot(list(range(i + 2)), count_herb, '*-', color='g', lw=0.5)
#        plt.plot(list(range(i + 2)), count_carn, '*-', color='r', lw=0.5)
#        plt.draw()
#        plt.pause(0.001)

#        print(i, " Year End Herb numbers :-", len(herb_list))
#        print(i, " Year End Carn numbers :-", len(carn_list))
#    print(i, " Year End Herb numbers :-", len(herb_list))
#    print(i, " Year End Carn numbers :-", len(carn_list))
#    plt.show()
    """
    c = Cell()
    c.current_herbivores = [Herbivore() for _ in range(10)]
    c.current_carnivores = [Carnivore() for _ in range(10)]
    print(type(c.n_animals))




    # Bishnu's image:

    # plot afterwards







#        print(c.n_carnivores)
#        print(c.n_herbivores)
