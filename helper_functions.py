import requests
import numpy as np
import json
from plotly.graph_objects import Scattergeo, Layout, Figure
from plotly import offline



def get_earthquake_data(f):
    
    """ Get the data from the request url and load it as a json file

    Args:
        f (string): The request url

    Returns:
        dictionary: Return the data in json format
    """
    
    data = requests.get(f)
    data = json.loads(data.text)
    return data

def get_featurs_lists(features):
    """
    get the information about the location, alert level and magnitude of each erthquake

    Args:
        features (dict): A dictionry of dictionaries containing the features of the erthquakes 

    Returns:
        mags (list): A list containing the magnitude of each erthquqke 
        places (list): A list containing the textual description of named geographic region near to the event
        lons (list): A list containing the longitude coordinates of each erthquake 
        lats (list): A list containing the latitude coordinates of each erthquake
        alert (list): A list containing the alert level of each erthquake
    """
    
    # these are the features we will be interested in
    mags = [] # the magnitude of the event 
    places = [] # the place at which the event took place
    lons, lats = [],[] # the longitude and latitude of the event
    alert = []

    for feature in features:

        mag = feature["properties"]["mag"]
        place = feature["properties"]["place"]
        alert_level = feature["properties"]["alert"]
    
        lon = feature["geometry"]["coordinates"][0]
        lat = feature["geometry"]["coordinates"][1]
    
        if alert_level and place:
            alert.append(alert_level) 
            places.append(place+"--"+"allert level:"+alert_level)
        else: 
            alert.append("grey")
            places.append(place)
        
        mags.append(mag)
        lons.append(lon)
        lats.append(lat)
        
    return mags, places, lons, lats, alert
     
def create_figure(mags, places, lons, lats, alert):
    """ 
    create a geographical figure containg the locations of each erthquake site 
    based on its location and magnitude. 

    Args:
        mags (_type_): _description_
        places (_type_): _description_
        lons (_type_): _description_
        lats (_type_): _description_
        alert (_type_): _description_

    Returns:
        _type_: _description_
    """
    # map the erthquakes 
    geo_data = [{
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": places,
        # we create a marker that will change its size based on the magnitude of the erthquake
        "marker": {
            "size": [4*mag for mag in mags],
            "color": mags,
            "line": {"width": 1.5, "color": alert,}, # change the color of the ring around the point based on its alert level
            "colorscale": "Magma",
            "reversescale": True,
            "colorbar": {"title": "Magnitude"},
      },
    }]
    
    layout = Layout(title="Global Erthquakes",)

    fig =  Figure(data=geo_data, layout=layout)  
    fig.update_geos(
        resolution=50,
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue",
        showrivers=True, rivercolor="Blue"
    )
    
    return fig