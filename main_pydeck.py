# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# ---------------------- CONFIGS ----------------------
PICTURES_PATH = os.path.join("data", "foto_sample.csv")
MILAN_COORDS = {"lat": 45.464664,
                "lon": 9.188540}
COLORS = {"Wall Painting": '[200, 30, 0, 160]',
          "Monument": '[0, 50, 200, 160]'}
COLUMNS_TO_DISPLAY = ["NAME", "TYPE", "ADDRESS", "DATE"]
df = pd.read_csv(PICTURES_PATH)

# initial view of the map, centered in Milan
initialView = pdk.ViewState(
        latitude=MILAN_COORDS["lat"],
        longitude=MILAN_COORDS["lon"],
        zoom=11,
        pitch=0,
    )
# points of different colors by type
scatterplotLayers = [pdk.Layer(
        'ScatterplotLayer',
        data=df[df["TYPE"] == t],
        get_position='[LON,LAT]',
        get_fill_color=v,
        get_radius=10,
        radiusMinPixels=5,
        pickable=True
    ) for t, v in COLORS.items()]

# html that is displayed when hovering over points on the map
tooltipHTML = '<pre><b>Name: </b>{NAME}\n' \
              '<b>Address: </b>{ADDRESS}\n' \
              '<b>Type: </b>{TYPE} </pre>' \
              '<img src="{URL}" alt="picture">'

mapStyle = 'mapbox://styles/mapbox/light-v9'

# ---------------------- DISPLAYED DATA ----------------------
st.write("Map of Milan wall paintings and monuments, created using ```pydeck```")
st.pydeck_chart(pdk.Deck(
    layers=scatterplotLayers,
    map_style=mapStyle,
    initial_view_state=initialView,
    tooltip={"html": tooltipHTML}
))

st.dataframe(df[COLUMNS_TO_DISPLAY].set_index("NAME"))
