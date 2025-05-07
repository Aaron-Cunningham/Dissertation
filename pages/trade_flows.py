from utils.input_components import *
from utils.create_graphs import create_sankey_diagram
import dash_deck
from data_processing.trade_flows_processing import *

mapbox_token = os.getenv("MAPBOX_ACCESS_TOKEN")

# Code adpapted from https://github.com/plotly/dash-deck/blob/master/demos/usage-bootstrap.py
TOOLTIP_TEXT_MAP = {
    "html": '<span style="color: #EE4B2B">{exporter} → {importer}</span><br>Value: ${value (US$)}<br>Resource: {resource}<br>Year: {year}'
}
# registers the page so can be accessed referenced from https://dash.plotly.com/urls
dash.register_page(__name__, path="/", name="Trade Flows")
# loads the data
trade_data = load_trade_data()

merge_coordinates_partner = map_data_processing()


# Dash app setup code adapted from
# 1) https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
# 2) https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
layout = html.Div(
    [
        dbc.Card(
            html.Div(
                [
                    # Fossil Fuel Dropdown
                    create_dropdown(
                        dropdown_id="resource-dropdown",
                        default_value="Oil",
                        options=[
                            {"label": "Oil", "value": "Oil"},
                            {"label": "Coal", "value": "Coal"},
                            {"label": "Gas", "value": "Gas"},
                        ],
                        label_text="Select Fossil Fuel",
                    ),
                    create_dropdown(
                        dropdown_id="map-year-slider",
                        default_value=2017,
                        options=[2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
                        label_text="Select Years for the Map",
                    ),
                    create_slider_nums(
                        "flow-amount-slider",
                        min=10,
                        max=70,
                        step=5,
                        value=10,
                        label_text="Select Number of Trade Flows to Display",
                        max_width="500px",
                    ),
                ],
                className="d-flex flex-column flex-lg-row justify-content-center align-items-center gap-3",
                style={
                    "background-color": "#F0F0F0",
                },
            ),
            style={"width": "100%", "max-width": "1000px", "margin": "10px auto"},
        ),
        dbc.Card(
            [  # title and subtitle for the map
                html.H3(
                    "Flow Map showing the top trade flows to Europe for the selected fossil fuel",
                    style={
                        "text-align": "center",
                        "font-family": "'Open Sans', Verdana, Arial, sans-serif",
                        "font-weight": "bold",
                        "font-size": "15px",
                    },
                ),
                html.H3(
                    "Exporter (Green) → Importer (Blue)",
                    style={
                        "text-align": "center",
                        "font-family": "'Open Sans', Verdana, Arial, sans-serif",
                        "font-size": "13px",
                    },
                ),
                html.Div(
                    # dash deck code referenced https://community.plotly.com/t/initial-release-of-dash-deck-a-library-for-rendering-webgl-3d-maps-with-pydeck-and-deck-gl-in-dash/44528/5
                    dash_deck.DeckGL(
                        id="trade-flow-map",
                        tooltip=TOOLTIP_TEXT_MAP,
                        mapboxKey=mapbox_token,
                    ),
                    style={
                        "position": "relative",
                        "height": "400px",
                        "overflow": "hidden",
                        "margin": "0px auto",
                        "width": "100%",
                        "max-width": "1480px",
                    },
                ),
            ],
            style={"width": "100%", "max-width": "1480px", "margin": "10px auto"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # sankey diagram post war
                                dcc.Graph(id="sankey-diagram-pre", config=CONFIG_GRAPH),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # sankey diagram for pre-war
                                dcc.Graph(
                                    id="sankey-diagram-post", config=CONFIG_GRAPH
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                    className="mb-5",
                ),
            ],
            justify="center",
            className="mt-3 gap-3",
        ),
    ],
)


# Callback to update all the graphs
@dash.callback(
    [
        Output("sankey-diagram-pre", "figure"),
        Output("sankey-diagram-post", "figure"),
    ],
    [
        Input("resource-dropdown", "value"),
        Input("flow-amount-slider", "value"),
    ],
)
@cache.memoize()
def update_sankey_graph_pre(fossil_fuel, num_of_trade_flows):

    # processes the data pre war
    top_flows_sankey_pre = sankey_data_processing(
        fossil_fuel, 2019, 2021, num_of_trade_flows
    )

    # creates the pre war diagram
    sankey_diagram_pre_war = create_sankey_diagram(
        top_flows_sankey_pre,
        fossil_fuel,
        text="Pre-War (2019 - 2021)",
        num_of_flows=num_of_trade_flows,
    )

    # processes the data post war
    top_flows_sankey_post = sankey_data_processing(
        fossil_fuel, 2022, 2024, num_of_trade_flows
    )

    # creates the post war diagram
    sankey_diagram_post_war = create_sankey_diagram(
        top_flows_sankey_post,
        fossil_fuel,
        text="Since the War (2022 - 2024)",
        num_of_flows=num_of_trade_flows,
    )

    return sankey_diagram_pre_war, sankey_diagram_post_war


# Callback to update all the graphs
@dash.callback(
    [
        Output("trade-flow-map", "data"),
    ],
    [
        Input("resource-dropdown", "value"),
        Input("map-year-slider", "value"),
        Input("flow-amount-slider", "value"),
    ],
)
@cache.memoize()
def update_map(fossil_fuel, map_years, num_of_trade_flows):
    # Filters the data based off user input for MAP
    input_filtered_map = merge_coordinates_partner[
        (merge_coordinates_partner["year"] == map_years)
        & (merge_coordinates_partner["resource"] == fossil_fuel)
    ]
    # extracts the top n after filtering based on value
    top_flows = input_filtered_map.nlargest(num_of_trade_flows, "value (US$)")
    low = (
        top_flows["value (US$)"].astype(float).quantile(0.50)
    )  # values below get width 1
    medium = (
        top_flows["value (US$)"].astype(float).quantile(0.90)
    )  # values below get width 3

    # function to assign a width to a line on flow map
    def assign_width(value):
        if value < low:
            return 1
        elif value < medium:
            return 3
        else:
            return 5

    # assign widths
    top_flows["width"] = top_flows["value (US$)"].astype(float).apply(assign_width)

    # formats the value results
    top_flows["value (US$)"] = top_flows["value (US$)"].apply("{:,.0f}".format)
    # converts top_flows to json
    map_json = top_flows.to_json(orient="records")
    map_data = json.loads(map_json)

    # Code adapted from
    # 1) https://deckgl.readthedocs.io/en/latest/gallery/great_circle_layer.html
    # 2) https://github.com/plotly/dash-deck/tree/master/demos
    layer = pdk.Layer(
        "GreatCircleLayer",
        map_data,
        pickable=True,
        get_source_position=["exporter_lon", "exporter_lat"],
        get_target_position=["importer_lon", "importer_lat"],
        get_source_color=[64, 255, 0],
        get_target_color=[0, 128, 200],
        auto_highlight=True,
        get_width="width",
    )

    # creates the map
    trade_flow_map = pdk.Deck(
        layers=[layer],
        initial_view_state={  # initial view state of the map
            "latitude": 35.266926,
            "longitude": 10.181365,
            "zoom": 1,
            "pitch": 30,
        },
        map_style="light",  # style of the map
        tooltip=TOOLTIP_TEXT_MAP,  # tooltip text
    )

    trade_flow_map.picking_radius = 10
    trade_flow_map = trade_flow_map.to_json()  # converts the map to json

    return [trade_flow_map]
