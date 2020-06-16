# Denne koden er ikke satt inn riktig


from biosim.landscape import Cell, Sea, Desert, Highland, Lowland
from biosim.animals import Animals, Herbivore, Carnivore
from biosim.island import Island

import textwrap
import matplotlib.pyplot as plt
import os
import numpy as np
import pandas as pd

""" Compatibility check for BioSim simulations.
This script shall function with biosim packages written for the INF200 project June 2020. 
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"


geogr = """
WWWWWWWWWWWWWWWWWWWWW
WWWWWWWWHWWWWLLLLLLLW
WHHHHHLLLLWWLLLLLLLWW
WHHHHHHHHHWWLLLLLLWWW
WHHHHHLLLLLLLLLLLLWWW
WHHHHHLLLDDLLLHLLLWWW
WHHLLLLLDDDLLLHHHHWWW
WWHHHHLLLDDLLLHWWWWWW
WHHHLLLLLDDLLLLLLLWWW
WHHHHLLLLDDLLLLWWWWWW
WWHHHHLLLLLLLLWWWWWWW
WWWHHHHLLLLLLLWWWWWWW
WWWWWWWWWWWWWWWWWWWWW"""

geogr = textwrap.dedent(geogr)

default_population = [
    {'loc': (10, 10),
     'pop': [{'species': 'Herbivore',
              'age': 5,
              'weight': 20}
             for _ in range(150)], },
    {'loc': (10, 10),
     'pop': [{'species': 'Carnivore',
              'age': 5,
              'weight': 20}
             for _ in range(40)], }
]


class BBioSim:

    def __init__(self, island_map, ini_pop, seed=1,
    ymax_animals=None, cmax_animals=None, hist_specs=None,
    img_base=None, img_fmt="png"):

        self._year = 0
        self._final_year = None
        self.island = Island(island_map, ini_pop)

        if ymax_animals is None:
            ymax_animals = 20000
        self._ymax = ymax_animals

        if cmax_animals is None:
            cmax_herb = 200
            cmax_carn = 200
        else:
            cmax_herb = cmax_animals['Herbivore']
            cmax_carn = cmax_animals['Carnivore']

        self._cmax_herb = cmax_herb
        self._cmax_carn = cmax_carn
        self.vis_years = None


    #WILL BE INITIATED BY _VISUALS_SETUP FUNCTION:
        self._nested_list = None
        self._fig_window = None
        self._map_ax = None
        self._map_axis_ = None
        self._map_code_ax = None
        self._map_code_axis = None
        self._graph_ax = None
        self._herb_line = None
        self._carn_line = None
        self._heat_map_carn_ax = None
        self._heat_map_carn_axis = None
        self._heat_map_herb_ax = None
        self._heat_map_herb_axis = None


    """
    :param island_map: Multi-line string specifying island geography
    :param ini_pop: List of dictionaries specifying initial population
    :param seed: Integer used as random number seed
    :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
    :param cmax_animals: Dict specifying color-code limits for animal densities
    :param hist_specs: Specifications for histograms, see below
    :param img_base: String with beginning of file name for figures, including path
    :param img_fmt: String with file type for figures, e.g. ’png’

    If ymax_animals is None, the y-axis limit should be adjusted automatically.

    If cmax_animals is None, sensible, fixed default values should be used.
    cmax_animals is a dict mapping species names to numbers, e.g.,
    {’Herbivore’: 50, ’Carnivore’: 20}


    hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
    For each property, a dictionary providing the maximum value and the bin width must be
    given, e.g.,
    {’weight’: {’max’: 80, ’delta’: 2}, ’fitness’: {’max’: 1.0, ’delta’: 0.05}}
    Permitted properties are ’weight’, ’age’, ’fitness’.


    If img_base is None, no figures are written to file.
    Filenames are formed as

    ’{}_{:05d}.{}’.format(img_base, img_no, img_fmt)

    where img_no are consecutive image numbers starting from 0.
    img_base should contain a path and beginning of a file name.
    """

    #todo
    #@staticmethod
    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == 'Herbivore':
            Herbivore.set_params(params)

        if species == 'Carnivore':
            Carnivore.set_params(params)


    #todo Fikse set_set parameters i landscape
    #@staticmethod
    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        cell_types = {'H': Highland,
                      'L': Lowland,
                      'D': Desert,
                      'W': Sea}
        cell_types[landscape].set_parameters(**params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self.vis_years = vis_years

        self._final_year = self._year + num_years
        self._visuals_setup()

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self.update_visual()

            if self._year % img_years == 0:
                self._save_file()

            self.island.run_function_one_year()
            self._year += 1
        self.update_visual()

    def create_rgb_map(self):
        colored_map = self.nested_coordinates_list
        map_list = self.island.check_map(geogr)

        for x, cell_row in enumerate(map_list):
            for y, cell_code in enumerate(cell_row):

                if cell_code == 'W':
                    colored_map[x][y] = (0,0,250)

                if cell_code == 'L':
                    colored_map[x][y] = (0,100,0)

                if cell_code == 'H':
                    colored_map[x][y] = (51,255,51)

                if cell_code == 'D':
                    colored_map[x][y] = (255,255,51)

        return colored_map


    def _visuals_setup(self):
        self._nested_list = self.nested_coordinates_list

        #Creating figure window:

        if self._fig_window is None:
            self._fig_window = plt.figure(constrained_layout=True, figsize=(16,12))
            gs = self._fig_window.add_gridspec(8,24)

        #Map subplot:

        if self._map_ax is None:
            self._map_ax = self._fig_window.add_subplot(gs[:4, 0:10])
            self._map_ax.set_title('Island')

        if self._map_axis_ is None:
            the_map = self.create_rgb_map()
            self._map_axis_ = self._map_ax.imshow(the_map)
            self._map_ax.get_xaxis().set_visible(False)
            self._map_ax.get_yaxis().set_visible(False)

        # Subplot map codes
        if self._map_code_ax is None:
            self._map_code_ax = self._fig_window.add_subplot(gs[:4, 10:14])
            cell_codes_color = [[(0,0,250)],
                                [(0,100,0)],
                                [(51,255,51)],
                                [(255,255,51)]]

            self._map_code_axis = self._map_code_ax.imshow(cell_codes_color)
            codes = ['', 'Water','Lowland', 'Highland','Desert']
            self._map_code_ax.set_yticklabels(codes)
            self._map_code_ax.get_xaxis().set_visible(False)

        # Subplot graph:
        if self._graph_ax is None:
            self._graph_ax = self._fig_window.add_subplot(gs[:2, 14:])
            self._graph_ax.set_xlim(0, self._final_year + 1)
            self._graph_ax.set_ylim(0, self._ymax)
            self._graph_ax.set(xlabel='year', ylabel='population')
        else:
            self._graph_ax.set_xlim(0, self._ymax)
            self._graph_ax.set_ylim(0, self._final_year + 1)

        # Init total number of herbivores graph:
        if self._herb_line is None:
            herb_graph = self._graph_ax.plot(np.arange(0, self._final_year + 1),
                                             np.full(self._final_year + 1, np.nan))
            self.herb_line = herb_graph[0]
        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, self._final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        # Init total number of carnivores graph
        if self._carn_line is None:
            carn_graph = self._graph_ax.plot(np.arange(0, self._final_year + 1),
                                             np.full(self._final_year + 1, np.nan))
            self.carn_line = carn_graph[0]
        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, self._final_year + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        # legend:

        self._graph_ax.legend((self._herb_line, self._carn_line),
                              ('Herbivores', 'Carnivores'),
                              loc='upper left')

        # Subplot heatmap:
        if self._heat_map_herb_ax is None:
            self._heat_map_herb_ax = self._fig_window.add_subplot(gs[4:, 12:])
            self._heat_map_herb_axis = None
#            self._heat_map_herb_ax.set_title('Herbivore locations')

        if self._heat_map_carn_ax is None:
            self._heat_map_carn_ax = self._fig_window.add_subplot(gs[4:, 12:])
            self._heat_map_carn_axis = None

#            self._heat_map_carn_ax.set_title('Carnivore locations')


    def update_visual(self):
#        self._fig_window.subtitle(f'Year: {self.year}', fontsize=30)
        self.update_heatmap()
        self.update_graphs()
        plt.pause(0.01)



    def update_heatmap(self):

        data_map = self.create_population_heatmap()
        data_map_herb, data_map_carn = data_map

        if self._heat_map_herb_axis is None:
            self._heat_map_herb_axis.set_data(data_map_herb)
        else:
            self._heat_map_herb_axis = self._heat_map_herb_ax.imshow(
                data_map_herb,
                interpolation='nearest',
                vmin=0,
                vmax=self._cmax_herb
            )
            plt.colorbar(self._heat_map_herb_axis,
                         ax=self._heat_map_herb_ax,
                         orientation='vertical')

        if self._heat_map_carn_axis is None:
            self._heat_map_carn_axis.set_data(data_map_carn)
        else:
            self._heat_map_carn_axis = self._heat_map_carn_ax.imshow(
                data_map_carn,
                interpolation='nearest',
                vmin=0,
                vmax=self._cmax_carn
            )
            plt.colorbar(self._heat_map_carn_axis,
                         ax=self._heat_map_carn_ax,
                         orientation='vertical')

    def create_population_heatmap(self):

        df = self.animal_distribution
        df.set_index(['Row','Col'], inplace=True)
        herb_array = np.asarray(df['Herbivore'])#gjøre om df til array der jeg bare tar med herbivores, samme med carn
        carn_array = np.asarray(df['Carnivore'])
        print(herb_array)


        herb_pop_list = self.nested_coordinates_list

        for x, list_ in enumerate(herb_pop_list):
            for y, _ in enumerate(list_):
                herb_pop = herb_array[x*y]
                herb_pop_list[x][y] = herb_pop

        carn_pop_list = self.nested_coordinates_list

        for x, list_ in enumerate(carn_pop_list):
            for y, _ in enumerate(list_):
                carn_pop = carn_array[x*y] #endret her
                carn_pop_list[x][y] = carn_pop
        print(herb_pop_list)
        return herb_pop_list, carn_pop_list



    def update_graphs(self):

        data_dict = self.num_animals_per_species
        total_herb = data_dict['Herbivore']
        total_carn = data_dict['Carnivore']

        herb_data = self._herb_line.get_ydata()
        herb_data[self._year] = total_herb
        if self.vis_years != 1:
            herb_data = self.interpolate_gaps(herb_data)

        carn_data = self._carn_line.get_ydata()
        carn_data[self._year] = total_carn
        if self.vis_years != 1:
            carn_data = self.interpolate_gaps(carn_data)

        self._herb_line.set_ydata(carn_data)
        self._carn_line.set_ydata(herb_data)

    def interpolate_gaps(self, values):

        limit = self.vis_years
        values = np.asarray(values)
        i = np.arange(values.size)
        valid = np.isfinite(Values)
        filled = np.interp(i, i[valid, values[valid]])

        if limit is not None:
            invalid = ~valid
            for n in range(1, limit + 1):
                invalid[:-n] &= invalid[n:]
                filled[invalid] = np.nan
        return filled


    @property
    def animal_distribution(self):
        data_dict = {'Row': [], 'Col': [], 'Herbivore': [], 'Carnivore': []}
        for loc, cell in self.island.map.items():
            x, y = loc
            data_dict['Row'].append(x)
            data_dict['Col'].append(y)
            data_dict['Herbivore'].append(cell.n_herbivores)
            data_dict['Carnivore'].append(cell.n_carnivores)
        df = pd.DataFrame.from_dict(data_dict)
        print(df)
        return df



    @property
    def nested_coordinates_list(self):
        self._nested_list = []
        map_size = self.island.map_size()
        x, y = map_size
        for x_index in range(x):
            self._nested_list.append([])
            for _ in range(y):
                self._nested_list[x_index].append(None)
        return self._nested_list



    def _save_file(self):
        pass

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """
        self.island.place_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.island.year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.num_animals_per_species

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved"""
        pass

if __name__ == "__main__":
    plt.ion()
    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]
    default_population = ini_herbs + ini_carns

    default_maps = """
    WWWWWWWWWWWWWWWWWWWWW
    WWWWWWWWHWWWWLLLLLLLW
    WHHHHHLLLLWWLLLLLLLWW
    WHHHHHHHHHWWLLLLLLWWW
    WHHHHHLLLLLLLLLLLLWWW
    WHHHHHLLLDDLLLHLLLWWW
    WHHLLLLLDDDLLLHHHHWWW
    WWHHHHLLLDDLLLHWWWWWW
    WHHHLLLLLDDLLLLLLLWWW
    WHHHHLLLLDDLLLLWWWWWW
    WWHHHHLLLLLLLLWWWWWWW
    WWWHHHHLLLLLLLWWWWWWW
    WWWWWWWWWWWWWWWWWWWWW"""

    default_maps = textwrap.dedent(default_maps)

    bio = BioSim(default_maps, default_population)
    bio.create_population_heatmap()
