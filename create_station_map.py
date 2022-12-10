import matplotlib.pyplot as plt
import PIL.Image as img
from array import *

def plot_stations():
    ## Array of station locations and names for the Red Line
    red_stations = [ [413, 99, 'Shadyside'],
                     [312, 168, 'Herron Ave'],
                     [268, 168, 'Swissvale'],
                     [226, 202, 'Penn Station'],
                     [226, 320, 'Steel Plaza'],
                     [226, 420, 'First Ave'],
                     [161, 484, 'Station Square'],
                     [55, 359, 'South Hills Junction'] ]

    ## Array of station locations and names for the Green Line
    green_stations = [ [256, 47, 'Pioneer'],
                       [335, 32, 'Edgebrook'],
                       [149, 19, 'Station'],
                       [94, 102, 'Whited'],
                       [94, 192, 'South Bank'],
                       [150, 264, 'Central'],
                       [237, 264, 'Inglewood'],
                       [306, 264, 'Overbrook'], 
                       [456, 359, 'Glenbury'],
                       [403, 605, 'Dormont'],
                       [235, 608, 'Mt Lebanon'],
                       [89, 608, 'Poplar'],
                       [48, 534, 'Castle Shannon'] ]

    ## Plot stations on empty image
    # Red line stations plot
    red_rows = len(red_stations)
    for i in range(red_rows):
        plt.plot(red_stations[i][0], red_stations[i][1], color = 'red', marker = 'o')

    # Green line stations plot
    green_rows = len(green_stations)
    for i in range(green_rows):
        plt.plot(green_stations[i][0], green_stations[i][1], color = 'green', marker = 'o')
