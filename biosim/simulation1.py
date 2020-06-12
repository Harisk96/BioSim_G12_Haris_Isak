#Denne koden er ikke satt inn riktig


from biosim.landscape import Cell, Sea, Desert, Highland, Lowland
from biosim.animals import Animals, Herbivore, Carnivore


import textwrap
import matplotlib.pyplot as plt

""" Compatibility check for BioSim simulations.
This script shall function with biosim packages written for the INF200 project June 2020. 
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"

if __name__ == ’__main__’:
    plt.ion()

    geogr = """\ 
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
    ini_herbs = [{’loc’: (10, 10),
        ’pop’: [{’species’: ’Herbivore’,
        ’age’: 5,
        ’weight’: 20}
    for _ in range(150)]}]
