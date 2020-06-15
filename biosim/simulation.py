# Denne koden er ikke satt inn riktig


from biosim.landscape import Cell, Sea, Desert, Highland, Lowland
from biosim.animals import Animals, Herbivore, Carnivore
from biosim.island import Island

import textwrap
import matplotlib.pyplot as plt
import os
import numpy as np

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


class BioSim:

    def __init__(self, island_map, ini_pop, seed=1,
    ymax_animals=None, cmax_animals=None, hist_specs=None,
    img_base=None, img_fmt=’png’):

        self._year = 0
        self._final_year = None
        self.island = Island(island_map, ini_pop)

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
    def set_animal_parameters(self, species , params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

        if species == 'Herbivore':
            Herbivore.set_params(**params)

        if species == 'Carnivore':
            Carnivore.set_params(**params)


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
        self._visualization_setup()

        while self._year < self._final_year:

            if self._year % vis_years == 0:
                self._update_visuals()

            if self._year % img_years == 0:
                self._save_file()

            self.island.run_function_one_year()
            self._year += 1
        self._update_visuals()

    def _visuals_setup(self):
        pass

    def _update_visuals(self):
        pass

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