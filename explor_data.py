from plotly.graph_objects import Scattergeo, Layout, Figure
from plotly import offline
from helper_functions import get_earthquake_data, get_featurs_lists, create_figure


if __name__ == '__main__':

    # specify the request url as described in the documentation
    f = r"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=1"

    #get the data in json format
    data = get_earthquake_data(f)

    # extract the features from the json file
    features = data["features"]

    # extract the information about the location and magnitude of each erthquake 
    mags, places, lons, lats, alert = get_featurs_lists(features=features)

    # create a plotly figure and plot it 
    fig = create_figure(mags, places, lons, lats, alert)
    offline.plot(fig,filename="global_erthquakes.html")