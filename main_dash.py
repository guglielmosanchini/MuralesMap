# https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb

from dash import Dash, dcc, html, Input, Output, no_update, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import os

# ---------------------- CONFIGS ----------------------
PICTURES_PATH = os.path.join("data", "foto_sample.csv")
MILAN_COORDS = {"lat": 45.464664,
                "lon": 9.188540}
COLORS = {"Wall Painting": 'blue',
          "Monument": 'red'}
COLUMNS_TO_DISPLAY = ["NAME", "TYPE", "ADDRESS", "DATE"]
EXTERNAL_STYLE = [dbc.themes.CERULEAN]

df = pd.read_csv(PICTURES_PATH)

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLE)


def create_graph(df):

    # initial view of the map, centered in Milan
    fig = go.Figure(go.Scattermapbox(
        lat=df["LAT"],
        lon=df["LON"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14,
            color=df["TYPE"].map({n: i+1 for i, n in enumerate(COLORS)}).values
        ),
        # text=df["URL"],
        # hovertemplate = tooltipHTML
    ))

    fig.update_layout(
        # hovermode='closest',
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0,
                "l": 0, "b": 0},
        mapbox=dict(
            center=go.layout.mapbox.Center(
                lat=MILAN_COORDS["lat"],
                lon=MILAN_COORDS["lon"]
            ),
            pitch=0,
            zoom=11)
    )

    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig


header = dbc.Col(
    [html.H1(children='Murales Milano with Dash')
     ]  # ,className="navbar navbar-expand-lg navbar-dark bg-primary"
)

Col_1_Row_1 = dbc.Col(
    [
        html.Div(dcc.Graph(
            id='example-graph',
            figure=create_graph(df),
            style={'width': '90vh', 'height': '90vh'}
        ), id="map-container"),
        dcc.Tooltip(id="graph-tooltip")
    ],
    # id="col1_row1",
    align="start"
)

Col_2_Row_1 = dbc.Col(
    [dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": col, "id": col, "deletable": False, "selectable": True} for col in COLUMNS_TO_DISPLAY#df.columns
        ],
        data=df.to_dict('records'),
        # hidden_columns=[col for col in df.columns if col not in COLUMNS_TO_DISPLAY],
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable=False,
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[i for i in range(len(df))],
        page_action="native",
        page_current=0,
        page_size=10,
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


# Callbacks
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


@app.callback(
    Output('example-graph', "figure"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)
    if len(derived_virtual_selected_rows) != 0:
        dff = dff.loc[derived_virtual_selected_rows]

    return create_graph(dff)


@app.callback(
    Output('example-graph', 'clickData'),
    Input('map-container', 'n_clicks'))
def reset_clickData(n_clicks):
    return None


if __name__ == '__main__':
    app.run_server(debug=True)
