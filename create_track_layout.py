import matplotlib.pyplot as plt
from array import *

from create_station_map import plot_stations
from trace_track_map import trace_track

def create_track_map():
    ## Trace the track layout
    trace_track()

    ## PLot the stations on both lines
    plot_stations()

    plt.axis([0, 500, 700, 0])
    plt.axis('off')
    plt.show()