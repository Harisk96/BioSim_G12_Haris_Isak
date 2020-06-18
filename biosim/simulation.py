import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Sea, Highland, Desert
from biosim.animals import Herbivore, Carnivore
from biosim.visualization import Visualization
import pandas as pd
import os
import subprocess

_FFMPEG_BINARY = 'ffmpeg'
_CONVERT_BINARY = 'magick'

_DEFAULT_GRAPHICS_DIR = os.path.join('results/')
_DEFAULT_GRAPHICS_NAME = 'bs'
_DEFAULT_MOVIE_FORMAT = 'mp4'


class BioSim:
    """
    This is the main interface class
    """

    def __init__(self, island_map, ini_pop, seed=1,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt="png"):
        """
        Init for biosim class.
        :param island_map:
        :param ini_pop:
        :param seed:
        :param ymax_animals:
        :param cmax_animals:
        :param hist_specs:
        :param img_base:
        :param img_fmt:
        """

        np.random.seed(seed)
        self._year = 0
        self._final_year = None
        self.inserted_map = island_map
        self.island = Island(island_map, ini_pop)
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_ctr = 0
        self.hist_specs = hist_specs

        if img_base is None:
            self.img_base = _DEFAULT_GRAPHICS_DIR+_DEFAULT_GRAPHICS_NAME

        if ymax_animals is None:
            ymax_animals = 20000
        self._ymax = ymax_animals

        if cmax_animals is None:
            cmax_herb = 20000
            cmax_carn = 20000
        else:
            cmax_herb = cmax_animals['Herbivore']
            cmax_carn = cmax_animals['Carnivore']

        self._cmax_herb = cmax_herb
        self._cmax_carn = cmax_carn
    #    self.vis_years = None

        # set up graphics
        self.visualization = Visualization()
        self.visualization.graphics_setup(rgb_map=self.create_rgb_map(island_map))
        # self.visualization.histogram_updates(self.island.fitness_list())

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        The simulate function runs through the whole simulation for num_years,
        and calls all the methods necessary in order to simulate and plot.
        :param num_years: Number of years we want to simulate
        :param vis_years: Interval plot updates
        :param img_years: Interval save photos
        :return: None
        """

        for i in range(num_years):
            self._year += 1
            self.island.run_function_one_year()
            self.visualization.update_graphics(self.create_population_heatmap(),
                                               self.island.num_animals_per_species)
            self.visualization.histogram_fitness_updates(self.island.fitness_list()[0],
                                                         self.island.fitness_list()[1],
                                                         self.hist_specs)
            self.visualization.histogram_age_updates(self.island.age_list()[0],
                                                     self.island.age_list()[1],
                                                     self.hist_specs)
            self.visualization.histogram_weight_updates(self.island.weight_list()[0],
                                                        self.island.weight_list()[1],
                                                        self.hist_specs)
            self.save_graphics(img_years)

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == 'Herbivore':
            Herbivore.set_params(params)

        if species == 'Carnivore':
            Carnivore.set_params(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

        cell_types = {'H': Highland,
                      'L': Lowland,
                      'D': Desert,
                      'W': Sea}
        cell_types[landscape].set_params(params)

    @property
    def year(self):
        """
        last year simulated
        :return: int
        """
        return self._year

    @property
    def num_animals(self):
        """
        umber og total animals in map
        :return: int, positive integer, number of animals currently on the island.
        """
        return self.island.num_animals

    @property
    def num_animals_per_species(self):
        """
        Returns a dictionary with number of herbivores and carnivores.
        :return: dict
        """
        return self.island.num_animals_per_species

    def length_of_map(self):
        """
        This function takes the island simulated and finds the width and height of the map.
        The width and height being the number of cells
        horizontally and vertically of the map simulated.
        :returns: int, positive integers, width and height of map.
        """
        lines = self.inserted_map.strip()
        lines = lines.split('\n')
        lenx_map = len(lines[0])
        leny_map = len(lines)
        return lenx_map, leny_map

    @staticmethod
    def create_rgb_map(input_raw_string):
        """
        Creates the rgb map that will be used to plot the island map on the final plot.
        :param input_raw_string:
        :return: rgb map
        """
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in input_raw_string.splitlines()]

        return kart_rgb

    @property
    def animal_distribution(self):
        """
        Used pandas to make a dataframe with the size 4x273.
        The 4 columns contain Row, Column, number of herbivores, number of carnivores.
        :return: pandas dataframe
        """
        data_dict = {'Row': [], 'Col': [], 'Herbivore': [], 'Carnivore': []}
        for loc, cell in self.island.map.items():
            x, y = loc
            data_dict['Row'].append(x)
            data_dict['Col'].append(y)
            data_dict['Herbivore'].append(cell.n_herbivores)
            data_dict['Carnivore'].append(cell.n_carnivores)
        df = pd.DataFrame.from_dict(data_dict)
        return df

    def add_population(self, population):
        """
        This function places the initial population on to the island.
        :param population:
        :return: None
        """
        self.island.place_population(population)

    def create_population_heatmap(self):
        """
        This function creates a two dimensional array that will be used further to plot the
        concentration on the heatmaps for herbivores and carnivores.

        The dataframe from animal distribution is used. The Herbivore and Carnivore columns are
        extracted and converted into a 1x273 one dimensional numpy array, the array is then
        reshaped into a two dimensional numpy array which tells us how many animals are in each
        cell. The two dimensional array resembles the map.

        x_len and y_len are the length and width of the map, which is used to reshape the arrays.
        :returns: 2D numpy arrays
        """

        x_len, y_len = self.length_of_map()

        df = self.animal_distribution
        df.set_index(['Row', 'Col'], inplace=True)
        herb_array = np.asarray(df['Herbivore']).reshape(y_len, x_len)
        carn_array = np.asarray(df['Carnivore']).reshape(y_len, x_len)

        return herb_array, carn_array

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Make movie function in case we want to try to make a video automatically withh ffmpeg.
        :param movie_fmt:
        :return: None
        """

        if self.img_base is None:
            raise RuntimeError('No filename is defined')

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{_%05d.png'.format(self.img_base),
                                       '-y', 'profile:v', 'baseline',
                                       '-level', 'yuv420p',
                                       '{}-{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'. format(err))

    def save_graphics(self, img_years):
        """
        Function used to make photos of the plot.
        :return: None
        """
        if img_years is None:
            return

        if self.img_base is None:
            return

        if self._year % img_years == 0:

            plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                         num=self.img_ctr,
                                                         type=self.img_fmt))
            self.img_ctr += 1
