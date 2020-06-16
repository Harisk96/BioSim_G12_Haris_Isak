import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Sea, Highland, Desert
from biosim.animals import Herbivore, Carnivore
import numpy as np

class Visualization:

    def __init__(self):
        self.steps = 0
        self.current_herbivore_data = []
        self.current_carnivore_data = []

    def graphics_setup(self, rgb_map=None):
        self.fig_win = plt.figure(figsize=(16, 10))
        plt.axis('off')

        self.fitness_ax = self.fig_win.add_subplot(6, 3, 16)
        self.fitness_ax.title.set_text('Histogram fitness')
        self.fitness_axis = None
        self.age_ax = self.fig_win.add_subplot(6, 3, 17)
        self.age_ax.title.set_text('Histogram age')
        self.weight_ax = self.fig_win.add_subplot(6, 3, 18)
        self.weight_ax.title.set_text('Histogram weight')

        #Setting up heatmap
        self.heatmap_herbies_ax = self.fig_win.add_axes([0.1, 0.28, 0.3, 0.3])
        self.herbies_axis = None
        self.heatmap_herbies_ax.title.set_text('Heatmap: Herbivore distribution')
        self.heatmap_herbies_ax.set_yticklabels([])
        self.heatmap_herbies_ax.set_xticklabels([])

        self.heatmap_carnies_ax = self.fig_win.add_axes([0.5, 0.28, 0.3, 0.3])
        self.carnies_axis = None
        self.heatmap_carnies_ax.title.set_text('Heatmap: Carnivore distribution')
        self.heatmap_carnies_ax.set_yticklabels([])
        self.heatmap_carnies_ax.set_xticklabels([])

        # The island map
        self.island_map_ax = self.fig_win.add_axes([0.1, 0.65, 0.4, 0.3])  # llx, lly, w, h
        self.island_map_ax.title.set_text('Island Map')
        self.island_map_ax.set_yticklabels([])
        self.island_map_ax.set_xticklabels([])
        # Let us create island at the beginning since it is constant
        self.island_map_ax.imshow(rgb_map)

        #Line graphs
        self.linegraph_ax = self.fig_win.add_axes([0.5, 0.65, 0.4, 0.3])

        # Year counter
        self.year_txt = self.fig_win.add_axes([0.5,0.95, 0.05, 0.05])
        self.year_txt.axis('off')
        self.changing_text = self.year_txt.text(0.2, 0.5, 'Year:' + str(0), fontdict={'weight': 'bold', 'size': 16})



        plt.pause(0.01)

    def update_graphics(self, distribution=None, num_species_dict=None):
        self.steps += 1
        self.changing_text.set_text('Year:' + str(self.steps))

    #Heatmap update
        if self.herbies_axis is None:
            self.herbies_axis = self.heatmap_herbies_ax.imshow(distribution[0],
                                                               interpolation='nearest',
                                                               cmap='Greens'
                                                               , vmin=0, vmax=50)
            self.heatmap_herbies_ax.figure.colorbar(self.herbies_axis,
                                                    ax=self.heatmap_herbies_ax,
                                                    orientation='horizontal',
                                                    fraction=0.07, pad=0.04)
        else:
            self.herbies_axis.set_data(distribution[0])

        if self.carnies_axis is None:
            self.carnies_axis = self.heatmap_carnies_ax.imshow(distribution[1],
                                                               interpolation='nearest',
                                                               cmap='OrRd', vmin=0, vmax=50)
            self.heatmap_carnies_ax.figure.colorbar(self.carnies_axis,
                                                    ax=self.heatmap_carnies_ax,
                                                    orientation='horizontal',
                                                    fraction=0.07, pad=0.04)
        else:
            self.carnies_axis.set_data(distribution[1])

        #line graph plot update:
        self.current_herbivore_data.append(num_species_dict['n_herbs'])
        self.current_carnivore_data.append(num_species_dict['n_carns'])
        length = len(self.current_carnivore_data)
        x_value = list(np.arange(length))
        self.linegraph_ax.set_ylim(0, max(self.current_herbivore_data)+10)

        self.linegraph_ax.title.set_text('# of animals by species')
        self.linegraph_ax.set_xlabel('years')
        self.linegraph_ax.set_ylabel('number of species')

        self.linegraph_ax.plot(x_value, self.current_herbivore_data, '-', color='g', linewidth=0.5)
        self.linegraph_ax.plot(x_value, self.current_carnivore_data, '-', color='r', linewidth=0.5)



        plt.pause(1e-6)

    def histogram_fitness_updates(self, fitness_list_herb=None, fitness_list_carn=None):

        self.fitness_ax.clear()
        self.fitness_ax.title.set_text('Histogram of fitness')
        self.fitness_ax.hist(fitness_list_herb, bins=10, histtype='step', color='g')
        self.fitness_ax.hist(fitness_list_carn, bins=10, histtype='step', color='r')

    def histogram_age_updates(self, age_list_herb=None, age_list_carn=None):
        self.age_ax.clear()
        self.age_ax.title.set_text('Histogram of age')
        self.age_ax.hist(age_list_herb, bins=10, histtype='step', color='g')
        self.age_ax.hist(age_list_carn, bins=10, histtype='step', color='r')

    def histogram_weight_updates(self, weight_list_herb=None, weight_list_carn=None):
        self.weight_ax.clear()
        self.weight_ax.title.set_text('Histogram of weight')
        self.weight_ax.hist(weight_list_herb, bins=10, histtype='step', color='g')
        self.weight_ax.hist(weight_list_carn, bins=10, histtype='step', color='r')




if __name__ == "__main__":
    v = Visualization()
    v.graphics_setup()
    plt.show()
