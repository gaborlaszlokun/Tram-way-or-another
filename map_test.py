# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 12:17:56 2021

@author: lgabor
"""

import plotly.graph_objects as go
import pandas as pd


tram_stations = pd.read_csv("tram_stations.csv")
lines = list(set(tram_stations['line']))

colors = ['red', 'blue', 'green', 'pink', 'yellow', 'black', 'purple', 'brown', 'orange', 'gray', 'olive', 'cyan', 
          'springgreen', 'sandybrown','darkmagenta','tan','navy','lime','khaki','lightcoral','darkorange','teal',
          'paleturquoise','cornflowerblue','silver', 'aqua']


routes = []

for i in range(len(lines)):
    slice_df = tram_stations[tram_stations.line==lines[i]]
    routes.append(go.Scattermapbox(
    mode = "text+lines+markers",
    marker=go.scattermapbox.Marker(
            size=10
        ),
    lon = list(slice_df['long']), lat = list(slice_df['lat']),
    text = list(slice_df['station']),textposition = "bottom right", name =str(lines[i]),
    line=dict(width=2, color=colors[i])))
 
fig = go.Figure(data=routes)  

fig.update_layout(mapbox_style="stamen-terrain",  mapbox=dict(center=dict(
            lat=47.5,
            lon=19
        ),zoom=10))
fig.update_geos(fitbounds="locations")
fig.write_html("tram_map_full.html")