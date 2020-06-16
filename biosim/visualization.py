import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Sea, Highland, Desert
from biosim.animals import Herbivore, Carnivore

class Visualization:


    def graphics_setup(self, rgb_map=None, herb_hist=None, carn_hist=None):
        self.fig_win = plt.figure(figsize=(30, 15))
        plt.axis('off')

        self.fitness_ax = self.fig_win.add_subplot(6, 3, 16)
        self.fitness_ax.title.set_text('Histogram fitness')
        self.fitness_axis = None
        self.age_ax = self.fig_win.add_subplot(6, 3, 17)
        self.age_ax.title.set_text('Histogram age')
        self.weight_ax = self.fig_win.add_subplot(6, 3, 18)
        self.weight_ax.title.set_text('Histogram weight')

        #Setting up heatmap
        self.heatmap_herbies_ax = self.fig_win.add_axes([0.2, 0.4, 0.15, 0.3])
        self.herbies_axis = None
        self.heatmap_herbies_ax.title.set_text('Heatmap of Herbivores')
        self.heatmap_herbies_ax.set_yticklabels([])
        self.heatmap_herbies_ax.set_xticklabels([])

        self.heatmap_carnies_ax = self.fig_win.add_axes([0.6, 0.4, 0.15, 0.3])
        self.carnies_axis = None
        self.heatmap_carnies_ax.title.set_text('Heatmap of Herbivores')
        self.heatmap_carnies_ax.set_yticklabels([])
        self.heatmap_carnies_ax.set_xticklabels([])

        plt.pause(5)

        def update_graphics(self, distribution=None, total_anim=None):
            self.steps += 1

            self.changing_year_text.set_text('Year:' + str(self.steps))

        #Heatmap update
            if self.herbies_axis is None:
                self.herbies_axis = self.heatmap_herbies_ax.imshow(distribution['Herbivore'],
                                                                   interpolation='nearest',
                                                                   cmap='Greens', vmin=0, vmax=50)
                self.heatmap_herbies_ax.figure.colorbar(self.herbies_axis,
                                                        ax=self.heatmap_herbies_ax,
                                                        orientation='horizontal',
                                                        fraction=0.07, pad=0.04)
            else:
                self.herbies_axis.set_data(distribution['Herbivore'])

            if self.carnies_axis is None:
                self.carnies_axis = self.heatmap_carnies_ax.imshow(distribution['Carnivore'],
                                                                   interpolation='nearest',
                                                                   cmap='Greens', vmin=0, vmax=50)
                self.heatmap_carnies_ax.figure.colorbar(self.carnies_axis,
                                                        ax=self.heatmap_carnies_ax,
                                                        orientation='horizontal',
                                                        fraction=0.07, pad=0.04)
            else:
                self.carnies_axis.set_data(distribution['Carnivore'])



if __name__ == "__main__":
    v = Visualization()
    v.graphics_setup()
    plt.show()
