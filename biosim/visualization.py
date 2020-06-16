import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Sea, Highland, Desert
from biosim.animals import Herbivore, Carnivore

class Visualization:

    def __init__(self):
        self.steps = 0

    def graphics_setup(self, rgb_map=None, herb_hist=None, carn_hist=None):
        self.fig_win = plt.figure(figsize=(16, 10))
        plt.axis('off')

        # self.fitness_ax = self.fig_win.add_subplot(6, 3, 16)
        # self.fitness_ax.title.set_text('Histogram fitness')
        # self.fitness_axis = None
        # self.age_ax = self.fig_win.add_subplot(6, 3, 17)
        # self.age_ax.title.set_text('Histogram age')
        # self.weight_ax = self.fig_win.add_subplot(6, 3, 18)
        # self.weight_ax.title.set_text('Histogram weight')

        #Setting up heatmap
        self.heatmap_herbies_ax = self.fig_win.add_axes([0.1, 0.1, 0.3, 0.3])
        self.herbies_axis = None
        self.heatmap_herbies_ax.title.set_text('Heatmap of Herbivores')
        self.heatmap_herbies_ax.set_yticklabels([])
        self.heatmap_herbies_ax.set_xticklabels([])

        self.heatmap_carnies_ax = self.fig_win.add_axes([0.5, 0.1, 0.3, 0.3])
        self.carnies_axis = None
        self.heatmap_carnies_ax.title.set_text('Heatmap of Herbivores')
        self.heatmap_carnies_ax.set_yticklabels([])
        self.heatmap_carnies_ax.set_xticklabels([])

        # The island map
        self.island_map_ax = self.fig_win.add_axes([0.1, 0.55, 0.4, 0.3])  # llx, lly, w, h
        self.island_map_ax.title.set_text('Island Map')
        self.island_map_ax.set_yticklabels([])
        self.island_map_ax.set_xticklabels([])
        # Let us create island at the beginning since it is constant
        self.island_map_ax.imshow(rgb_map)

        #Line graphs
        self.linegraph_ax = self.fig_win.add_axes([0.5, 0.55, 0.4, 0.3])


        plt.pause(1)

    def update_graphics(self, distribution=None, total_anim=None):
        self.steps += 1

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
        plt.pause(1e-6)



if __name__ == "__main__":
    v = Visualization()
    v.graphics_setup()
    plt.show()
