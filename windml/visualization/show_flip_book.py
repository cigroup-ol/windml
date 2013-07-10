import matplotlib.pyplot as plt
import numpy as np
import datetime
import time
import math
from mpl_toolkits.basemap import Basemap, shiftgrid, cm

def show_flip_book(windpark, num_plots, start_time, diff_time, show=True):
    """Plots a flip book of a given windpark

    Parameters
    ----------
    windpark : Windpark
               The windpark for the flip book.

    num_plots: int
               Amount of plots, either 4, 9 or 16.

    start_time: int
                Element position of time series.

    diff_time: int
               Temporal distance between plots.
    """

    plt.clf()

    mills = windpark.get_windmills()
    target = windpark.get_target()
    radius = windpark.get_radius()

    number_of_plots = num_plots
    start_measurement = start_time
    time_diff_between_plot = diff_time

    #pack latitude and longitude in lists
    rel_input_lat = []
    rel_input_lon = []
    rel_input_speed_array = [[0 for col in range(number_of_plots)] for row in range(len(mills))]

    # For labeling the plot with a timestamp
    unix_timestamps = []
    timestamps_known = 0

    row_act = 0
    for row in mills:   # Target inside !!!!
        rel_input_lat.append(np.float64(row.latitude))
        rel_input_lon.append(np.float64(row.longitude))
        time = start_measurement
        for measurement in range(number_of_plots):
            rel_input_speed_array[row_act][measurement] = row.measurements[time][2]
            time += time_diff_between_plot

        if (timestamps_known == 0):
            time = start_measurement
            for measurement in range(number_of_plots):
                unix_timestamps.append(row.measurements[time][0])
                time += time_diff_between_plot
            timestamps_known = 1

        row_act += 1

    targetcoord = [0.0, 0.0]
    targetcoord[0] = np.float64(target.latitude)
    targetcoord[1] = np.float64(target.longitude)

    # Topographic Map with farms
    #see: http://matplotlib.org/basemap/users/examples.html
    # Basemap
    graddiff = (radius/111.0) + 0.1  # degree in km

    m = Basemap(projection='stere', lon_0=targetcoord[1], lat_0=targetcoord[0],\
        llcrnrlon = targetcoord[1]-graddiff, llcrnrlat = targetcoord[0]-graddiff ,\
        urcrnrlon = targetcoord[1]+graddiff, urcrnrlat = targetcoord[0]+graddiff ,\
        rsphere=6371200., resolution = 'l', area_thresh=1000)

    # Target
    #x_target,y_target = m(targetcoord[1],targetcoord[0])
    # Input Farms
    rel_inputs_lon, rel_inputs_lat = m(rel_input_lon, rel_input_lat)

    plot_dim = math.sqrt(number_of_plots)
    figure = plt.figure(figsize=(15, 10))
    plt.title("Flip - Book")
    for i in range(1, (number_of_plots+1)):
        plot = plt.subplot(plot_dim, plot_dim, i)
        zlist = []
        for z in range(len(mills)):
            zlist.append(rel_input_speed_array[z][i-1])
        parallels = np.arange(int(targetcoord[0]-3), int(targetcoord[0]+3), 1.)
        m.drawparallels(parallels,labels=[True,False,False,False])
        meridians = np.arange(int(targetcoord[1]-3), int(targetcoord[1]+3), 1.)
        m.drawmeridians(meridians,labels=[True,False,False,True])
        m.shadedrelief()
        m.drawcoastlines
        m.scatter(rel_inputs_lon, rel_inputs_lat, c = zlist, s = 35, vmin = 0.0, vmax = 35)
        plt.title(datetime.datetime.fromtimestamp(unix_timestamps[i-1]).strftime('%Y-%m-%d %H:%M:%S'))
        plt.colorbar()

    if(show):
        plt.show()


