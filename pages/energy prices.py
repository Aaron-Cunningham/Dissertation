from utils.input_components import *
from utils.create_graphs import create_map
from data_processing.energy_prices_processing import *

# registers the page so can be accessed referenced from https://dash.plotly.com/urls
dash.register_page(__name__, path="/energy-prices", name="Energy Prices")

trade_data = load_trade_data()

electricity_data = load_electricity_data()

# loads Fuel data filtering #
fuel_data = load_fuel_cleaned()


# Dash app setup code adapted from
# 1) https://www.youtube.com/watch?v=d9SmpNfMg7U&ab_channel=CharmingData
# 2) https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
layout = html.Div(
    [
        dbc.Card(
            html.Div(
                [
                    # range slider for the fuel line chart
                    create_range_slider(
                        trade_data,
                        "range-slider",
                        "for The Fuel Prices Line Chart's",
                        width="100%",
                    ),
                ],
            ),
            style={"width": "100%", "max-width": "800px", "margin": "10px auto"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                # line chart for fual
                                dcc.Graph(
                                    "line-chart-fuel",
                                    config=CONFIG_GRAPH,
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                dcc.Graph(
                                    "line-chart-electric",
                                    config=CONFIG_GRAPH,
                                ),
                            ]
                        ),
                    ),
                    width="auto",
                ),
            ],
            justify="center",
            className="g-3",
        ),
        dbc.Card(
            html.Div(
                [
                    create_dropdown(
                        "fuel-dropdown",  # id of the dropdown
                        "Petrol",  # default value
                        ["Petrol", "Diesel"],  # options
                        "Select Fuel Type",  # label
                    ),
                    create_slider(
                        trade_data,
                        "range-slider-map",
                        "The Choropleth Map's",
                        width="500px",
                    ),
                ],
                className="d-flex justify-content-center align-items-center gap-3",
                style={"background-color": "#F0F0F0"},
            ),
            style={"width": "100%", "max-width": "800px", "margin": "10px auto"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [
                                dcc.Graph(id="fuel-map", config={"scrollZoom": True}),
                            ]
                        ),
                    ),
                    width="auto",
                ),
                dbc.Col(
                    dbc.Card(
                        html.Div(
                            [dcc.Graph("electricity-map", config={"scrollZoom": True})]
                        ),
                    ),
                    width="auto",
                ),
            ],
            justify="center",
            className="g-3 mb-3",
        ),
    ]
)


@dash.callback(
    [
        Output("line-chart-electric", "figure"),
    ],
    [
        Input("range-slider", "value"),
    ],
)
@cache.memoize()
def electricity_graph_line(range_slider_electric):
    # Data processing for electricity data #
    # retrieves the filtered data and the percentage change
    electricity_data_filtered, percentage_change = electricity_line_chart_processing(
        electricity_data, range_slider_electric
    )

    # creates a line graph
    electricity_line = px.line(
        electricity_data_filtered,
        x="Year",
        y="Price",
        text="Price",
        markers=True,
        title=f"Average Yearly Electricity Prices for EU Households (Excl. Taxes & Levies, {range_slider_electric[0]} - {range_slider_electric[1]})",
        labels={"Price": "Electricity Price (Euros per kWh)"},  # labels for the graph
    )

    # configures the line graph
    configure_line_graph(
        electricity_line,
        percentage_change,
        "Year: %{x}<br>" + "Price (Per kWh): €%{y:,.2f}<br>",
        "€%{text:,.2f}",
        legend_title=None,
        tickprefix="€",
    )

    return [electricity_line]


@dash.callback(
    [
        Output("line-chart-fuel", "figure"),
    ],
    [
        Input("range-slider", "value"),
    ],
)
@cache.memoize()
def fuel_graph_line(range_slider_fuel):

    # Data processing for fuel data #
    # retrieves the filtered data and the percentage change
    fuel_data_processed, percentage_text = fuel_line_chart_processing(
        fuel_data, range_slider_fuel
    )
    # calculate change overtime
    fuel_line = px.line(
        fuel_data_processed,
        x="Year",
        y=["Petrol", "Diesel"],
        markers=True,
        title=f"Average Yearly Fuel Prices for the EU (Excl. Taxes & Duties, {range_slider_fuel[0]} - {range_slider_fuel[1]})",
        labels={"value": "Fuel Price (Euros per Litre)"},
    )

    # configures the linegraph
    configure_line_graph(
        fuel_line,
        percentage_text,
        "Year: %{x}<br>" + "Price (Per 1 litre): €%{y:,.2f}<br>",
        "€%{text:,.0f}",
        legend_title="Type of Fuel",
        tickprefix="€",
    )

    return [fuel_line]


@dash.callback(
    [
        Output("fuel-map", "figure"),
    ],
    [Input("range-slider-map", "value"), Input("fuel-dropdown", "value")],
)
@cache.memoize()
def fuel_choropleth_map(years_map, fuel_dropdown):
    data_filtered_pie = fuel_map_processing(fuel_data, years_map, fuel_dropdown)
    # finds minimum value for the shared colour range using 10th percentile for minimum
    minimum_colour = fuel_data["Price"].quantile(0.10) / 1000
    # finds maximum value for the shared colour range using 90th percentile for maximum
    maximum_colour = fuel_data["Price"].quantile(0.90) / 1000

    # creates a choropleth map
    fuel_map = create_map(
        data_filtered_pie,
        "Price",  # column to be used for colouring
        custom_data=["Price", "Country", "Fuel"],  # custom data for hover
        color_range=[minimum_colour, maximum_colour],
        locations="countryISO",
        center={"lat": 54.706772, "lon": 12.207891},  # center of the map
        zoom=1.6,
    )

    # configures the map
    fuel_map = configure_map(
        fuel_map,
        hovertemplate="<b>%{customdata[1]}</b><br>"
        + "<br>"
        + "Value in Euro: €%{customdata[0]:,.2f} <br>"
        + "Fuel: %{customdata[2]}",
        title_text=f"Average {fuel_dropdown} Fuel Prices in Europe (Excl. Taxes & Duties, {years_map}) <br><sup>Measured in Euros Per 1 Litre of Fuel </sup>",
        coloraxis_colorbar_title="Value Per Litre in €",
        height=350,
        prefix="€",
    )

    return [fuel_map]


@dash.callback(
    [Output("electricity-map", "figure")],
    [Input("range-slider-map", "value")],
)
@cache.memoize()
def electricity_choropleth_map(years_map):
    # retrieves the filtered data
    electricity_data_filtered = electricity_data[
        (electricity_data["Year"] == years_map)
    ]
    # finds minimum value for the shared colour range
    minimum_colour = electricity_data["Price"].quantile(0.10)
    # finds maximum value for the shared colour range
    maximum_colour = electricity_data["Price"].quantile(0.90)
    # creates a choropleth map
    electricity_map = create_map(
        electricity_data_filtered,
        "Price",
        custom_data=["Price", "Country"],
        color_range=[minimum_colour, maximum_colour],
        locations="countryISO",
        center={"lat": 54.706772, "lon": 12.207891},
        zoom=1.6,
    )
    # configures the map
    electricity_map = configure_map(
        electricity_map,
        hovertemplate="<b>%{customdata[1]}</b><br>"
        + "<br>"
        + "Value in Euro: €%{customdata[0]:,.2f} <br>",
        title_text=f"Average Electricity Prices in Households in Europe (Excl. Taxes & Levies, {years_map}) <sup><br>Measured in Euros Per kWh</sup>",
        coloraxis_colorbar_title="Value Per kWh in €",
        height=350,
        prefix="€",
    )
    return [electricity_map]
