# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

from dash import Dash, dcc,html, Input, Output, no_update, dash_table
import dash_bootstrap_components as dbc
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os


# ---------------------- CONFIGS ----------------------
PICTURES_PATH = os.path.join("data", "foto_sample.csv")
MILAN_COORDS = {"lat": 45.464664,
                "lon": 9.188540}
COLORS = {"Wall Painting": '[200, 30, 0, 160]',
          "Monument": '[0, 50, 200, 160]'}
COLUMNS_TO_DISPLAY = ["NAME", "TYPE", "ADDRESS", "DATE"]
EXTERNAL_STYLE = [dbc.themes.CERULEAN]


df = pd.read_csv(PICTURES_PATH)

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLE)

# initial view of the map, centered in Milan
fig = go.Figure(go.Scattermapbox(
        lat=df["LAT"],
        lon=df["LON"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
        text=df["URL"],
        #hovertemplate = tooltipHTML
    ))

fig.update_layout(
    #hovermode='closest',
    mapbox_style = "open-street-map",
    mapbox=dict(
        #bearing=0,
        center=go.layout.mapbox.Center(
            lat=MILAN_COORDS["lat"],
            lon=MILAN_COORDS["lon"]
        ),
        pitch = 0,
        zoom = 10)
)

fig.update_traces(hoverinfo="none", hovertemplate=None)

# app.layout = html.Div(children=[
#     dcc.Graph(
#         id='example-graph',
#         figure=fig,
#         style = {'width': '90vh', 'height': '90vh'}
#     ),
#     dcc.Tooltip(id="graph-tooltip"),

#     dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

# ])

header =  dbc.Col(
                [   html.H1(children='Murales Milano with Dash')
                ]#,className="navbar navbar-expand-lg navbar-dark bg-primary"
)

Col_1_Row_1 = dbc.Col(
                [
                    dcc.Graph(
                            id='example-graph',
                            figure=fig,
                            style = {'width': '90vh', 'height': '90vh'}
                            ),
                    dcc.Tooltip(id="graph-tooltip")
                ]
            , align = "start"
            )

Col_2_Row_1 = dbc.Col(
                [dash_table.DataTable(
                                    df[["NAME","ADDRESS"]].to_dict('records'), [{"name": i, "id": i} for i in df[["NAME","ADDRESS"]].columns]
                                    )
                ],
                align="center"
            )


body = dbc.Container(
        dbc.Card(
    [   
        dbc.Row([header]),
        dbc.Row(
            [
            Col_1_Row_1,
            Col_2_Row_1
            ]
        )
    ]
        ),
        fluid=True
)

app.layout = html.Div([body])



#Callbacks

@app.callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("example-graph", "clickData"),
)
def display_hover(clickData):
    if clickData is None:
        return False, no_update, no_update

    pt = clickData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]
    df_row = df.iloc[num]
    img_src = df_row['URL']
    name = df_row['NAME']
    form = df_row['ADDRESS']
    desc = df_row['DATE']

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{name}", style={"color": "darkblue"}),
            html.P(f"{form}"),
            html.P(f"{desc}"),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]

    return True, bbox, children

if __name__ == '__main__':
    app.run_server(debug=True)
