import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.landscape import Lowland, Sea, Highland, Desert
from biosim.animals import Herbivore, Carnivore
from biosim.visualization import Visualization
import textwrap
import pandas as pd

class BioSim:

    def __init__(self, island_map, ini_pop, seed=1,
                 ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_base=None, img_fmt="png"):
        self._year = 0
        self._final_year = None
        # self.island = Island(island_map, ini_pop)
        self.inserted_map = island_map
        self.island = Island(island_map, ini_pop)


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


        #set up graphics
        self.visualization = Visualization()
        self.visualization.graphics_setup(rgb_map=self.create_rgb_map(island_map))

    def simulate(self, num_years, vis_years=1, img_years=None):


        for i in range(num_years):
            self.island.run_function_one_year()
            self.visualization.update_graphics( self.create_population_heatmap() )
            #call the cycle



    def length_of_map(self):
        lines = self.inserted_map.strip()
        lines = lines.split('\n')
        lenx_map = len(lines[0])
        leny_map = len(lines)
        print(leny_map)
        print(lenx_map)
        return lenx_map, leny_map



    def create_rgb_map(self, input_raw_string):
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in input_raw_string.splitlines()]

        return kart_rgb
        # colored_map = self.nested_coordinates_list
        # #map_list returns nested list with strings of the map.
        # map_list = self.island.check_map(island_map)
        #
        # for x, cell_row in enumerate(map_list):
        #     for y, cell_code in enumerate(cell_row):
        #
        #         if cell_code == 'W':
        #             colored_map[x][y] = (0,0,250)
        #
        #         if cell_code == 'L':
        #             colored_map[x][y] = (0,100,0)
        #
        #         if cell_code == 'H':
        #             colored_map[x][y] = (51,255,51)
        #
        #         if cell_code == 'D':
        #             colored_map[x][y] = (255,255,51)

        # return colored_map

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
        return df

    def create_population_heatmap(self):

        x_len, y_len = self.length_of_map()

        df = self.animal_distribution
        df.set_index(['Row', 'Col'], inplace=True)
        herb_array = np.asarray(df['Herbivore']).reshape(y_len, x_len)  # gjøre om df til array der jeg bare tar med herbivores, samme med carn
        carn_array = np.asarray(df['Carnivore']).reshape(y_len, x_len)
        print(herb_array)
        print(carn_array)

        return herb_array, carn_array



if __name__ == '__main__':
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
    bio.length_of_map()
    bio.create_population_heatmap()
