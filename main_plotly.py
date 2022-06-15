import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ---------------------- CONFIGS ----------------------
PICTURES_PATH = os.path.join("data", "foto_sample.csv")
MILAN_COORDS = {"lat": 45.464664,
                "lon": 9.188540}
COLORS = {"Wall Painting": 'blue',
          "Monument": 'red'}
COLUMNS_TO_DISPLAY = ["NAME", "TYPE", "ADDRESS", "DATE"]
df = pd.read_csv(PICTURES_PATH)

fig = px.scatter_mapbox(df,
                        lat="LAT", lon="LON",
                        hover_name="NAME",
                        hover_data=["TYPE", "DATE"],
                        color="TYPE",
                        center=MILAN_COORDS,
                        color_discrete_map=COLORS,
                        mapbox_style="open-street-map",
                        zoom=11)

fig.update_layout(margin={"r": 0, "t": 0,
                          "l": 0, "b": 0})
fig.update_traces(marker={'size': 15})

st.plotly_chart(fig)

# fig = go.Figure(go.Scattermapbox(
#         lat=df["LAT"],
#         lon=df["LON"],
#         mode='markers',
#         marker=go.scattermapbox.Marker(
#             size=14,
#             color=df["TYPE"].map({n: i+1 for i, n in enumerate(COLORS)}).values
#         ),
#         text=df["NAME"],
#     ))
#
# fig.update_layout(
#     hovermode='closest',
#     margin={"r": 0, "t": 0,
#             "l": 0, "b": 0},
#     mapbox=dict(
#         style="open-street-map",
#         bearing=0,
#         center=go.layout.mapbox.Center(
#             lat=MILAN_COORDS["lat"],
#             lon=MILAN_COORDS["lon"]
#         ),
#         pitch=0,
#         zoom=11
#     )
# )
