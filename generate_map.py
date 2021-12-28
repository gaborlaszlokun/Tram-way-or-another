# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:17:56 2021
@author: lgabor
"""

import plotly.graph_objects as go
import pandas as pd

tram_stations = pd.read_csv("tram_stations.csv")
# tram_stations = pd.read_csv("tram_stations_reduced_v3.csv")

lines = sorted(list(set(tram_stations['line'])))

colors = ['blue', 'red', 'green', 'pink', 'yellow', 'black', 'purple', 'brown', 'orange', 'gray', 'olive', 'cyan', 
          'springgreen', 'sandybrown','darkmagenta','tan','navy','lime','khaki','lightcoral','darkorange','teal',
          'paleturquoise','cornflowerblue','red', 'aqua','black']

routes = []

for i in range(len(lines)):
    slice_df = tram_stations[tram_stations.line==lines[i]]
    routes.append(go.Scattermapbox(
    mode = "text+lines+markers",
    marker=go.scattermapbox.Marker(
            size=15
        ),
    lon = list(slice_df['long']), lat = list(slice_df['lat']),
    text = list(slice_df['station']+" -- " + slice_df['direction']),textposition = "bottom right", name =str(lines[i]),
    line=dict(width=2, color=colors[i])))
 
fig = go.Figure(data=routes)  

fig.update_layout(mapbox_style="stamen-terrain",  mapbox=dict(center=dict(
            lat=47.5,
            lon=19
        ),zoom=10))
fig.update_geos(fitbounds="locations")

fig.write_html("tram_map_full.html")
# fig.write_html("tram_map_full_reduced.html")